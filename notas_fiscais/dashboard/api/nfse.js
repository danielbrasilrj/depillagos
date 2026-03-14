const API_KEY = process.env.TRINKS_API_KEY;
const ESTABLISHMENT_ID = process.env.TRINKS_ESTABLISHMENT_ID || "243726";
const BASE_URL = "https://api.trinks.com/v1";

// Payment methods that do NOT generate NFS-e
const EXCLUDE_METHODS = new Set(["Dinheiro"]);

async function fetchPage(dataInicio, dataFim, page) {
  const url = `${BASE_URL}/transacoes?dataInicio=${dataInicio}&dataFim=${dataFim}&page=${page}&pageSize=50`;
  const res = await fetch(url, {
    headers: {
      "X-Api-Key": API_KEY,
      estabelecimentoId: ESTABLISHMENT_ID,
    },
  });
  if (!res.ok) throw new Error(`Trinks API ${res.status}`);
  return res.json();
}

export default async function handler(req, res) {
  const periodo = req.query.periodo; // YYYY-MM
  if (!periodo || !/^\d{4}-\d{2}$/.test(periodo)) {
    return res.status(400).json({ error: "periodo must be YYYY-MM" });
  }

  const [year, month] = periodo.split("-").map(Number);
  const dataInicio = `${periodo}-01`;
  const nextMonth =
    month === 12 ? `${year + 1}-01-01` : `${year}-${String(month + 1).padStart(2, "0")}-01`;

  // Fetch first page to get total
  const first = await fetchPage(dataInicio, nextMonth, 1);
  const totalPages = first.totalPages || 0;
  let allRecords = first.data || [];

  // Fetch remaining pages
  const promises = [];
  for (let p = 2; p <= totalPages; p++) {
    promises.push(fetchPage(dataInicio, nextMonth, p));
  }
  const pages = await Promise.all(promises);
  for (const page of pages) {
    allRecords = allRecords.concat(page.data || []);
  }

  // Aggregate
  const porDia = {};
  const porMetodo = {};
  let totalNfse = 0;
  let countNfse = 0;
  let totalGeral = 0;
  let countGeral = 0;

  for (const t of allRecords) {
    const dia = t.dataHora.slice(0, 10);
    const valor = t.totalPagar;
    totalGeral += valor;
    countGeral++;

    // Check if this transaction generates NFS-e (has any card/PIX payment)
    const pagamentos = t.formasPagamentos || [];
    let valorNfse = 0;
    let geraNfse = false;

    for (const p of pagamentos) {
      const nome = p.nome;
      if (!EXCLUDE_METHODS.has(nome)) {
        valorNfse += p.valor;
        geraNfse = true;
        porMetodo[nome] = (porMetodo[nome] || 0) + p.valor;
      }
    }

    if (geraNfse) {
      totalNfse += valor;
      countNfse++;
      if (!porDia[dia]) porDia[dia] = { valor: 0, count: 0 };
      porDia[dia].valor += valor;
      porDia[dia].count++;
    }
  }

  // Sort days
  const dias = Object.entries(porDia)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([data, d]) => ({
      data,
      valor: Math.round(d.valor * 100) / 100,
      notas: d.count,
    }));

  // Sort methods by value desc
  const metodos = Object.entries(porMetodo)
    .sort(([, a], [, b]) => b - a)
    .map(([nome, valor]) => ({ nome, valor: Math.round(valor * 100) / 100 }));

  // Best day
  const melhorDia = dias.reduce(
    (best, d) => (d.valor > best.valor ? d : best),
    { data: "-", valor: 0, notas: 0 }
  );

  const diasUteis = dias.length;
  const mediaDiaria = diasUteis > 0 ? totalNfse / diasUteis : 0;

  res.setHeader("Cache-Control", "s-maxage=300, stale-while-revalidate=60");
  return res.status(200).json({
    periodo,
    totalNfse: Math.round(totalNfse * 100) / 100,
    countNfse,
    totalGeral: Math.round(totalGeral * 100) / 100,
    countGeral,
    diasUteis,
    mediaDiaria: Math.round(mediaDiaria * 100) / 100,
    melhorDia,
    porDia: dias,
    porMetodo: metodos,
    geradoEm: new Date().toISOString(),
  });
}
