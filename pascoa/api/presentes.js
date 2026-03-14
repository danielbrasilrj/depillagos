import Redis from "ioredis";

let redis;
function getRedis() {
  if (!redis) redis = new Redis(process.env.REDIS_URL);
  return redis;
}

const STORE_KEY = "pascoa_2026_presentes";

export default async function handler(req, res) {
  try {
    const r = getRedis();

    if (req.method === "GET") {
      const raw = await r.get(STORE_KEY);
      const presentes = raw ? JSON.parse(raw) : [];
      return res.status(200).json({ presentes, total: presentes.length });
    }

    if (req.method === "POST") {
      const { clienteId, clienteNome, clienteTelefone, motivo } = req.body;
      if (!clienteId || !clienteNome || !motivo) {
        return res.status(400).json({ error: "Campos obrigatórios: cliente e motivo" });
      }

      const raw = await r.get(STORE_KEY);
      const presentes = raw ? JSON.parse(raw) : [];

      if (presentes.some((p) => p.clienteId === clienteId)) {
        return res.status(409).json({ error: "Cliente já recebeu o presente" });
      }

      presentes.push({
        id: Date.now().toString(),
        clienteId,
        clienteNome,
        clienteTelefone: clienteTelefone || "",
        motivo,
        dataRegistro: new Date().toISOString(),
      });

      await r.set(STORE_KEY, JSON.stringify(presentes));
      return res.status(201).json({ ok: true, total: presentes.length });
    }

    if (req.method === "DELETE") {
      const { id } = req.query;
      if (!id) return res.status(400).json({ error: "ID obrigatório" });

      const raw = await r.get(STORE_KEY);
      const presentes = raw ? JSON.parse(raw) : [];
      const filtered = presentes.filter((p) => p.id !== id);

      if (filtered.length === presentes.length) {
        return res.status(404).json({ error: "Presente não encontrado" });
      }

      await r.set(STORE_KEY, JSON.stringify(filtered));
      return res.status(200).json({ ok: true, total: filtered.length });
    }

    return res.status(405).json({ error: "Método não permitido" });
  } catch (err) {
    return res.status(500).json({ error: "Erro interno" });
  }
}
