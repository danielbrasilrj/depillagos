import https from "https";
import { gunzipSync } from "zlib";

const CNPJ_DEPILAGOS = "09223558000100";
const API_BASE = "https://adn.nfse.gov.br/contribuintes";

function makeAgent(pfxBuffer, passphrase) {
  return new https.Agent({ pfx: pfxBuffer, passphrase, rejectUnauthorized: true });
}

function fetchLote(agent, nsu) {
  const url = `${API_BASE}/DFe/${nsu}?cnpjConsulta=${CNPJ_DEPILAGOS}&lote=true`;
  return new Promise((resolve, reject) => {
    const req = https.get(url, { agent, headers: { Accept: "application/json" }, timeout: 15000 }, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          reject(new Error(`Invalid JSON from ADN at NSU ${nsu}`));
        }
      });
    });
    req.on("error", reject);
    req.on("timeout", () => { req.destroy(); reject(new Error(`Timeout NSU ${nsu}`)); });
  });
}

function decodeXml(b64) {
  const buf = Buffer.from(b64, "base64");
  return gunzipSync(buf).toString("utf-8");
}

function xmlText(xml, tag) {
  // Match exact tag name with optional namespace, e.g. <vServ> or <ns:vServ> but NOT <vServPrest>
  const re = new RegExp(`<(?:[\\w]*:)?${tag}>([^<]*)`, "");
  const m = xml.match(re);
  return m ? m[1].trim() : "";
}

function xmlCData(xml, tag) {
  const re = new RegExp(`<[^:>]*:?${tag}[^>]*>([\\s\\S]*?)</[^:>]*:?${tag}>`, "m");
  const m = xml.match(re);
  return m ? m[1].replace(/<!\[CDATA\[|\]\]>/g, "").trim() : "";
}

function extrairDadosNota(doc) {
  const xml = decodeXml(doc.ArquivoXml);
  const nfse = xmlText(xml, "nNFSe");
  const dCompet = xmlText(xml, "dCompet");
  const dhProc = xmlText(xml, "dhProc").slice(0, 10);
  const vServ = parseFloat(xmlText(xml, "vServ")) || 0;
  const cStat = xmlText(xml, "cStat") || "100";
  const desc = xmlCData(xml, "xDescServ");

  const parceiros = {};

  if (desc.includes("COTA-PARTE")) {
    const cotas = [...desc.matchAll(/(SALAO-PARCEIRO|PROFISSIONAL-PARCEIRO):\s*(\d{11,14})\s+COTA-PARTE\s+R\$([\d.]+(?:,\d+)?)/g)];
    let cotaSalaoTotal = 0;
    const parceirosRaw = {};
    for (const [, tipo, cnpj, valor] of cotas) {
      const v = parseFloat(valor.replace(",", "."));
      if (tipo === "SALAO-PARCEIRO") cotaSalaoTotal += v;
      else parceirosRaw[cnpj] = (parceirosRaw[cnpj] || 0) + v;
    }
    const totalParceiros = Object.values(parceirosRaw).reduce((a, b) => a + b, 0);
    for (const [cnpj, cotaP] of Object.entries(parceirosRaw)) {
      const prop = totalParceiros > 0 ? cotaP / totalParceiros : 1;
      parceiros[cnpj] = { cota_parceiro: cotaP, cota_salao: cotaSalaoTotal * prop };
    }
  } else if (desc.includes("Rateio referente")) {
    const blocos = desc.split("Rateio referente a Salao/Profissional parceiro:").slice(1);
    for (const bloco of blocos) {
      const cnpjs = [...bloco.matchAll(/CNPJ:\s*(\d{11,14})\b.{1,150}?R\$\s*([\d]+[.,][\d]+)/g)];
      let cotaSalaoBloco = 0, cnpjParceiro = "", cotaParceiro = 0;
      for (const [, cnpj, valor] of cnpjs) {
        const v = parseFloat(valor.replace(/\./g, "").replace(",", "."));
        if (cnpj === CNPJ_DEPILAGOS) cotaSalaoBloco += v;
        else { cnpjParceiro = cnpj; cotaParceiro += v; }
      }
      if (cnpjParceiro) {
        if (parceiros[cnpjParceiro]) {
          parceiros[cnpjParceiro].cota_parceiro += cotaParceiro;
          parceiros[cnpjParceiro].cota_salao += cotaSalaoBloco;
        } else {
          parceiros[cnpjParceiro] = { cota_parceiro: cotaParceiro, cota_salao: cotaSalaoBloco };
        }
      }
    }
  }

  return { nfse, dCompet, dhProc, vServ, cStat, parceiros, temRateio: Object.keys(parceiros).length > 0 };
}

function formatCnpj(c) {
  c = c.padStart(14, "0");
  return `${c.slice(0, 2)}.${c.slice(2, 5)}.${c.slice(5, 8)}/${c.slice(8, 12)}-${c.slice(12)}`;
}

function formatDateBR(iso) {
  if (!iso || iso.length < 10) return iso || "";
  const [y, m, d] = iso.slice(0, 10).split("-");
  return `${d}/${m}/${y}`;
}

function formatValorBR(v) {
  return v.toFixed(2).replace(".", ",");
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "POST only" });
  }

  const { pfx, senha, periodo, startNsu } = req.body;
  if (!pfx || !senha || !periodo) {
    return res.status(400).json({ error: "pfx (base64), senha, and periodo required" });
  }

  const pfxBuffer = Buffer.from(pfx, "base64");
  let agent;
  try {
    agent = makeAgent(pfxBuffer, senha);
  } catch (e) {
    return res.status(400).json({ error: `Certificado inválido: ${e.message}` });
  }

  // Fetch documents by NSU in chunks (each invocation processes up to ~45s)
  const notas = [];
  let nsu = startNsu || 1;
  let totalDocs = 0;
  let failedNsus = 0;
  const startTime = Date.now();
  const MAX_TIME = 45000; // 45s per chunk, safe margin for 60s limit
  let finished = false;

  while (Date.now() - startTime < MAX_TIME) {
    let resp;
    let retries = 3;
    while (retries > 0) {
      try {
        resp = await fetchLote(agent, nsu);
        break;
      } catch {
        retries--;
        if (retries === 0) resp = null;
      }
    }
    if (!resp) { nsu++; failedNsus++; continue; }

    const status = resp.StatusProcessamento;
    if (status === "NENHUM_DOCUMENTO_LOCALIZADO" || status === "REJEICAO") {
      finished = true;
      break;
    }

    const lote = resp.LoteDFe || [];
    if (!lote.length) { finished = true; break; }

    totalDocs += lote.length;
    const loteMax = Math.max(...lote.map((d) => d.NSU));

    for (const doc of lote) {
      if (doc.TipoDocumento !== "NFSE") continue;
      try {
        const nota = extrairDadosNota(doc);
        nota.nsu = doc.NSU;
        notas.push(nota);
      } catch { /* skip bad docs */ }
    }

    nsu = loteMax + 1;
  }

  const notasMapped = notas.map(n => ({
    nfse: n.nfse, dCompet: n.dCompet, dhProc: n.dhProc,
    vServ: n.vServ, cStat: n.cStat, temRateio: n.temRateio,
    parceiros: n.parceiros,
  }));

  if (!finished) {
    return res.status(200).json({
      done: false,
      nextNsu: nsu,
      totalDocs,
      failedNsus,
      notas: notasMapped,
    });
  }

  return res.status(200).json({
    done: true,
    totalDocs,
    failedNsus,
    notas: notasMapped,
  });
}
