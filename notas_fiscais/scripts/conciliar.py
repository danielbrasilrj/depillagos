"""
Conciliação NFS-e (ADN) vs Trinks (API) para um mês.

Uso:
  python3 scripts/conciliar.py --periodo 2026-02 --senha PASSWORD

Fluxo:
1. Extrai TODAS as NFS-e do período via ADN (número, data, valor)
2. Busca TODAS as transações do Trinks no mesmo período
3. Cruza por valor + data (com tolerância de até 5 dias)
4. Reporta matches, divergências de valor, e não-encontrados
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timedelta

# Add parent dir to path so we can import extraction functions
sys.path.insert(0, os.path.dirname(__file__))
from extrair_notas import (
    extrair_cert_key,
    consultar_lote,
    extrair_dados_nota,
)

TRINKS_API_KEY = os.environ.get("TRINKS_API_KEY", "agLy1iUwVR2uKgeln9Rb47IpHuE6ZpZ04u3PFmO1")
TRINKS_ESTABLISHMENT_ID = "243726"
CURL = "/opt/local/bin/curl"


def fetch_all_nfse(cert_path, key_path, periodo):
    """Baixa TODAS as NFS-e e filtra pelo período."""
    todas_notas = []
    nsu_atual = 1
    total_docs = 0

    while True:
        print(f"  NSU {nsu_atual}...", end="\r")
        resposta = consultar_lote(cert_path, key_path, nsu_atual)

        if resposta is None:
            break

        status = resposta.get("StatusProcessamento")
        if status == "NENHUM_DOCUMENTO_LOCALIZADO":
            break
        if status == "REJEICAO":
            break

        lote = resposta.get("LoteDFe", [])
        if not lote:
            break

        total_docs += len(lote)
        max_nsu_lote = max(d["NSU"] for d in lote)

        for doc in lote:
            if doc.get("TipoDocumento") != "NFSE":
                continue
            try:
                nota = extrair_dados_nota(doc)
                nota["nsu"] = doc["NSU"]
                todas_notas.append(nota)
            except Exception:
                pass

        nsu_atual = max_nsu_lote + 1

    print(f"\n  Total docs baixados: {total_docs}")
    print(f"  Total NFS-e: {len(todas_notas)}")

    # Filtrar por período
    notas_periodo = [n for n in todas_notas if n["data_servico"].startswith(periodo)]
    # Apenas autorizadas (cstat=100)
    notas_ok = [n for n in notas_periodo if n.get("cstat") == "100"]
    print(f"  No período {periodo}: {len(notas_periodo)} (autorizadas: {len(notas_ok)})")

    return notas_ok


def fetch_trinks_transactions(data_inicio, data_fim):
    """Busca TODAS as transações do Trinks no período."""
    all_records = []
    page = 1

    # First get total
    result = _trinks_get(data_inicio, data_fim, 1, 1)
    total = result.get("totalRecords", 0)
    total_pages = result.get("totalPages", 0)
    print(f"  Trinks: {total} transações em {total_pages} páginas")

    while page <= total_pages:
        result = _trinks_get(data_inicio, data_fim, page, 50)
        records = result.get("data", [])
        all_records.extend(records)
        page += 1

    print(f"  Trinks: {len(all_records)} transações baixadas")
    return all_records


def _trinks_get(data_inicio, data_fim, page, page_size):
    url = (
        f"https://api.trinks.com/v1/transacoes"
        f"?dataInicio={data_inicio}&dataFim={data_fim}"
        f"&page={page}&pageSize={page_size}"
    )
    cmd = [
        CURL, "-s",
        "-H", f"X-Api-Key: {TRINKS_API_KEY}",
        "-H", f"estabelecimentoId: {TRINKS_ESTABLISHMENT_ID}",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)


def conciliar(nfse_list, trinks_list):
    """
    Cruza NFS-e com Trinks por valor + data.
    Retorna: matched, nfse_only, trinks_only
    """
    # Index Trinks by date -> list of records
    trinks_by_date = defaultdict(list)
    for t in trinks_list:
        # Use dataHora date (payment date)
        day = t["dataHora"][:10]
        trinks_by_date[day].append({
            "id": t["id"],
            "data": day,
            "valor": t["totalPagar"],
            "cliente": t["cliente"]["nome"],
            "matched": False,
        })

    matched = []
    nfse_unmatched = []

    for nota in nfse_list:
        nfse_date = nota["data_servico"]  # YYYY-MM-DD
        nfse_valor = nota["valor_total"]
        nfse_num = nota["nfse"]

        found = False
        # Try same day, then -1 to -5 days, then +1 to +5 days
        for delta in [0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5]:
            try:
                check_date = (datetime.strptime(nfse_date, "%Y-%m-%d") + timedelta(days=delta)).strftime("%Y-%m-%d")
            except ValueError:
                continue

            candidates = trinks_by_date.get(check_date, [])
            for c in candidates:
                if c["matched"]:
                    continue
                # Match by value (with small tolerance for rounding)
                if abs(c["valor"] - nfse_valor) < 0.02:
                    c["matched"] = True
                    valor_ok = abs(c["valor"] - nfse_valor) < 0.01
                    matched.append({
                        "nfse_num": nfse_num,
                        "nfse_data": nfse_date,
                        "nfse_valor": nfse_valor,
                        "trinks_id": c["id"],
                        "trinks_data": c["data"],
                        "trinks_valor": c["valor"],
                        "trinks_cliente": c["cliente"],
                        "delta_dias": delta,
                        "valor_ok": valor_ok,
                    })
                    found = True
                    break
            if found:
                break

        if not found:
            nfse_unmatched.append({
                "nfse_num": nfse_num,
                "nfse_data": nfse_date,
                "nfse_valor": nfse_valor,
            })

    # Trinks unmatched
    trinks_unmatched = []
    for day_records in trinks_by_date.values():
        for c in day_records:
            if not c["matched"]:
                trinks_unmatched.append(c)

    return matched, nfse_unmatched, trinks_unmatched


def main():
    parser = argparse.ArgumentParser(description="Conciliação NFS-e vs Trinks")
    parser.add_argument("--periodo", required=True, help="Período YYYY-MM")
    parser.add_argument("--senha", help="Senha do certificado .pfx")
    args = parser.parse_args()

    periodo = args.periodo  # e.g. "2026-02"

    # Determine Trinks date range
    year, month = map(int, periodo.split("-"))
    if month == 12:
        next_month = f"{year + 1}-01-01"
    else:
        next_month = f"{year}-{month + 1:02d}-01"
    trinks_start = f"{periodo}-01"
    trinks_end = next_month

    # Step 1: Extract NFS-e
    print("=" * 60)
    print("ETAPA 1: Extraindo NFS-e da ADN...")
    print("=" * 60)

    pfx_path = os.path.join(os.path.dirname(__file__), "..", "certificado", "DEPILAGOS MATRIZ 2025.pfx")
    senha = args.senha or os.environ.get("DEPILAGOS_PFX_PASSWORD")
    if not senha:
        print("ERRO: senha do certificado necessária (--senha ou DEPILAGOS_PFX_PASSWORD)")
        sys.exit(1)

    cert_path, key_path = extrair_cert_key(pfx_path, senha)
    nfse_list = fetch_all_nfse(cert_path, key_path, periodo)

    # Step 2: Fetch Trinks
    print()
    print("=" * 60)
    print("ETAPA 2: Buscando transações do Trinks...")
    print("=" * 60)

    trinks_list = fetch_trinks_transactions(trinks_start, trinks_end)

    # Step 3: Match
    print()
    print("=" * 60)
    print("ETAPA 3: Conciliando...")
    print("=" * 60)

    matched, nfse_only, trinks_only = conciliar(nfse_list, trinks_list)

    # Stats
    same_day = sum(1 for m in matched if m["delta_dias"] == 0)
    shifted = sum(1 for m in matched if m["delta_dias"] != 0)
    valor_diverge = sum(1 for m in matched if not m["valor_ok"])

    total_nfse_valor = sum(n["valor_total"] for n in nfse_list)
    total_trinks_valor = sum(t["totalPagar"] for t in trinks_list)
    matched_nfse_valor = sum(m["nfse_valor"] for m in matched)
    matched_trinks_valor = sum(m["trinks_valor"] for m in matched)

    print(f"\n{'=' * 60}")
    print(f"RESULTADO DA CONCILIAÇÃO - {periodo}")
    print(f"{'=' * 60}")
    print(f"\n  NFS-e (ADN):        {len(nfse_list):>6} notas    R$ {total_nfse_valor:>12,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    print(f"  Trinks:             {len(trinks_list):>6} transaç. R$ {total_trinks_valor:>12,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    print(f"\n  MATCHES:")
    print(f"    Mesmo dia:        {same_day:>6}")
    print(f"    Com shift (±5d):  {shifted:>6}")
    print(f"    Total matched:    {len(matched):>6}  R$ {matched_nfse_valor:>12,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    if valor_diverge:
        print(f"    Valor divergente: {valor_diverge:>6}")

    print(f"\n  SEM MATCH:")
    print(f"    Só na NFS-e:      {len(nfse_only):>6}  R$ {sum(n['nfse_valor'] for n in nfse_only):>12,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    print(f"    Só no Trinks:     {len(trinks_only):>6}  R$ {sum(t['valor'] for t in trinks_only):>12,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Show shift distribution
    if shifted:
        print(f"\n  DISTRIBUIÇÃO DE SHIFTS:")
        shift_dist = defaultdict(int)
        for m in matched:
            if m["delta_dias"] != 0:
                shift_dist[m["delta_dias"]] += 1
        for delta in sorted(shift_dist.keys()):
            label = f"+{delta}" if delta > 0 else str(delta)
            print(f"    {label} dias: {shift_dist[delta]}")

    # Show some unmatched NFS-e
    if nfse_only:
        print(f"\n  AMOSTRA: NFS-e sem match no Trinks (primeiras 20):")
        for n in sorted(nfse_only, key=lambda x: x["nfse_data"])[:20]:
            print(f"    Nota {n['nfse_num']:<6} | {n['nfse_data']} | R$ {n['nfse_valor']:>8,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Show some unmatched Trinks
    if trinks_only:
        print(f"\n  AMOSTRA: Trinks sem match na NFS-e (primeiras 20):")
        for t in sorted(trinks_only, key=lambda x: x["data"])[:20]:
            print(f"    ID {t['id']:<12} | {t['data']} | R$ {t['valor']:>8,.2f} | {t['cliente']}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Save full results to JSON
    output_path = os.path.join(os.path.dirname(__file__), "..", "output", f"conciliacao_{periodo.replace('-', '')}.json")
    with open(output_path, "w") as f:
        json.dump({
            "periodo": periodo,
            "resumo": {
                "nfse_total": len(nfse_list),
                "nfse_valor": total_nfse_valor,
                "trinks_total": len(trinks_list),
                "trinks_valor": total_trinks_valor,
                "matched": len(matched),
                "matched_same_day": same_day,
                "matched_shifted": shifted,
                "nfse_only": len(nfse_only),
                "trinks_only": len(trinks_only),
            },
            "matched": matched,
            "nfse_only": nfse_only,
            "trinks_only": trinks_only,
        }, f, indent=2, ensure_ascii=False)
    print(f"\n  Detalhes salvos em: {output_path}")


if __name__ == "__main__":
    main()
