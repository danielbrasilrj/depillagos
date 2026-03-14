const API_KEY = process.env.TRINKS_API_KEY;
const ESTABLISHMENT_ID = process.env.TRINKS_ESTABLISHMENT_ID || "243726";

export default async function handler(req, res) {
  const q = (req.query.q || "").trim();
  if (q.length < 2) {
    return res.status(400).json({ error: "Busca deve ter pelo menos 2 caracteres" });
  }

  try {
    const url = `https://api.trinks.com/v1/clientes?nome=${encodeURIComponent(q)}&pageSize=15`;
    const response = await fetch(url, {
      headers: {
        "X-Api-Key": API_KEY,
        estabelecimentoId: ESTABLISHMENT_ID,
      },
    });

    if (!response.ok) {
      return res.status(502).json({ error: "Erro ao buscar no Trinks" });
    }

    const data = await response.json();
    const clientes = (data.data || []).map((c) => ({
      id: c.id,
      nome: c.nome,
      telefones: (c.telefones || []).map((t) => `(${t.ddd}) ${t.telefone}`),
      email: c.email || null,
    }));

    res.setHeader("Cache-Control", "no-cache");
    return res.status(200).json({ clientes });
  } catch (err) {
    return res.status(500).json({ error: "Erro interno ao buscar cliente" });
  }
}
