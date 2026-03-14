"""
Conciliação Fevereiro 2026: NFS-e (CSV existente) vs Trinks (API).

Match por: data + valor total da nota.
O CSV tem apenas notas COM rateio (549 de 1040 total).
"""

import csv
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta

TRINKS_API_KEY = os.environ.get("TRINKS_API_KEY", "agLy1iUwVR2uKgeln9Rb47IpHuE6ZpZ04u3PFmO1")
TRINKS_ESTABLISHMENT_ID = "243726"
CURL = "/opt/local/bin/curl"


def load_nfse_from_csv(csv_path):
    """Carrega notas do CSV e agrupa por número de nota."""
    notas = {}  # nota_num -> {data, valor_total, parceiros}

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            num = row["NUMERO DA NOTA"].strip()
            data_servico = row["data servico"].strip()  # DD/MM/YYYY
            data_emissao = row["data emissao"].strip()
            cnpj = row["CNPJ PROFISSIONAL PARCEIRO"].strip()

            # Parse values (BR format: comma decimal)
            cota_salao = float(row["COTA PARTE SALÃO PARCEIRO"].replace(".", "").replace(",", "."))
            cota_prof = float(row["COTA PARTE PROFISSIONAL-PARCEIRO"].replace(".", "").replace(",", "."))

            if num not in notas:
                # Convert DD/MM/YYYY to YYYY-MM-DD
                parts = data_servico.split("/")
                iso_date = f"{parts[2]}-{parts[1]}-{parts[0]}"
                parts_em = data_emissao.split("/")
                iso_emissao = f"{parts_em[2]}-{parts_em[1]}-{parts_em[0]}"
                notas[num] = {
                    "numero": num,
                    "data_servico": iso_date,
                    "data_emissao": iso_emissao,
                    "valor_total": 0.0,
                    "parceiros": [],
                }

            valor_servico = cota_salao + cota_prof
            notas[num]["valor_total"] += valor_servico
            notas[num]["parceiros"].append({
                "cnpj": cnpj,
                "cota_salao": cota_salao,
                "cota_prof": cota_prof,
            })

    # Round values
    for n in notas.values():
        n["valor_total"] = round(n["valor_total"], 2)

    return list(notas.values())


def fetch_trinks_page(data_inicio, data_fim, page, page_size):
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
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return json.loads(result.stdout)


def fetch_all_trinks(data_inicio, data_fim):
    """Busca todas as transações do Trinks no período."""
    # First get total with proper pageSize
    result = fetch_trinks_page(data_inicio, data_fim, 1, 50)
    total = result.get("totalRecords", 0)
    total_pages = result.get("totalPages", 0)
    all_records = result.get("data", [])
    print(f"  Trinks: {total} transações em {total_pages} páginas")

    for page in range(2, total_pages + 1):
        result = fetch_trinks_page(data_inicio, data_fim, page, 50)
        records = result.get("data", [])
        all_records.extend(records)
        if page % 5 == 0:
            print(f"  Página {page}/{total_pages}...", end="\r")

    print(f"  Trinks: {len(all_records)} transações baixadas")
    return all_records


def conciliar(nfse_list, trinks_list):
    """
    Cruza NFS-e com Trinks por data + valor.
    Usa data_servico da NFS-e vs data do Trinks, com tolerância ±5 dias.
    """
    # Index Trinks by date
    trinks_by_date = defaultdict(list)
    for t in trinks_list:
        day = t["dataHora"][:10]
        trinks_by_date[day].append({
            "id": t["id"],
            "data": day,
            "hora": t["dataHora"][11:],
            "valor": t["totalPagar"],
            "descontos": t.get("descontos", 0),
            "cliente": t["cliente"]["nome"],
            "cliente_id": t["cliente"]["id"],
            "servicos": [s["nome"] for s in t.get("servicos", [])],
            "pagamentos": [f"{p['nome']}:{p['valor']}" for p in t.get("formasPagamentos", [])],
            "matched": False,
        })

    matched = []
    nfse_unmatched = []

    for nota in nfse_list:
        nfse_date = nota["data_servico"]
        nfse_valor = nota["valor_total"]
        nfse_num = nota["numero"]

        found = False
        for delta in [0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5]:
            try:
                check_date = (datetime.strptime(nfse_date, "%Y-%m-%d") + timedelta(days=delta)).strftime("%Y-%m-%d")
            except ValueError:
                continue

            candidates = trinks_by_date.get(check_date, [])
            for c in candidates:
                if c["matched"]:
                    continue
                if abs(c["valor"] - nfse_valor) < 0.02:
                    c["matched"] = True
                    matched.append({
                        "nfse_num": nfse_num,
                        "nfse_data": nfse_date,
                        "nfse_valor": nfse_valor,
                        "trinks_id": c["id"],
                        "trinks_data": c["data"],
                        "trinks_valor": c["valor"],
                        "trinks_cliente": c["cliente"],
                        "trinks_servicos": c["servicos"],
                        "delta_dias": delta,
                        "valor_diff": round(c["valor"] - nfse_valor, 2),
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
                "parceiros": nota["parceiros"],
            })

    trinks_unmatched = []
    for day_records in trinks_by_date.values():
        for c in day_records:
            if not c["matched"]:
                trinks_unmatched.append(c)

    return matched, nfse_unmatched, trinks_unmatched


def main():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "output", "fev2026.csv")
    periodo = "2026-02"

    print("=" * 60)
    print("ETAPA 1: Carregando NFS-e do CSV...")
    print("=" * 60)

    nfse_list = load_nfse_from_csv(csv_path)
    total_nfse_valor = sum(n["valor_total"] for n in nfse_list)
    print(f"  {len(nfse_list)} notas únicas (com rateio)")
    print(f"  Valor total: R$ {total_nfse_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    print()
    print("=" * 60)
    print("ETAPA 2: Buscando transações do Trinks...")
    print("=" * 60)

    trinks_list = fetch_all_trinks("2026-02-01", "2026-03-01")
    total_trinks_valor = sum(t["totalPagar"] for t in trinks_list)
    print(f"  Valor total: R$ {total_trinks_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    print()
    print("=" * 60)
    print("ETAPA 3: Conciliando (data + valor, ±5 dias)...")
    print("=" * 60)

    matched, nfse_only, trinks_only = conciliar(nfse_list, trinks_list)

    same_day = sum(1 for m in matched if m["delta_dias"] == 0)
    shifted = sum(1 for m in matched if m["delta_dias"] != 0)
    matched_nfse_valor = sum(m["nfse_valor"] for m in matched)
    matched_trinks_valor = sum(m["trinks_valor"] for m in matched)

    fmt = lambda v: f"R$ {v:>12,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    print(f"\n{'=' * 60}")
    print(f"RESULTADO DA CONCILIAÇÃO - {periodo}")
    print(f"{'=' * 60}")
    print(f"\n  NFS-e (rateio):     {len(nfse_list):>6} notas    {fmt(total_nfse_valor)}")
    print(f"  Trinks:             {len(trinks_list):>6} transaç. {fmt(total_trinks_valor)}")

    print(f"\n  MATCHES:")
    print(f"    Mesmo dia:        {same_day:>6}")
    print(f"    Com shift (±5d):  {shifted:>6}")
    print(f"    Total matched:    {len(matched):>6}  {fmt(matched_nfse_valor)}")

    # Value divergences
    valor_diffs = [m for m in matched if abs(m["valor_diff"]) >= 0.01]
    if valor_diffs:
        print(f"    Valor divergente: {len(valor_diffs):>6}")

    print(f"\n  SEM MATCH:")
    nfse_only_valor = sum(n["nfse_valor"] for n in nfse_only)
    trinks_only_valor = sum(t["valor"] for t in trinks_only)
    print(f"    Só na NFS-e:      {len(nfse_only):>6}  {fmt(nfse_only_valor)}")
    print(f"    Só no Trinks:     {len(trinks_only):>6}  {fmt(trinks_only_valor)}")
    print(f"    (Trinks inclui notas sem rateio e outros serviços)")

    # Shift distribution
    if shifted:
        print(f"\n  DISTRIBUIÇÃO DE SHIFTS:")
        shift_dist = defaultdict(int)
        for m in matched:
            if m["delta_dias"] != 0:
                shift_dist[m["delta_dias"]] += 1
        for delta in sorted(shift_dist.keys()):
            label = f"+{delta}" if delta > 0 else str(delta)
            print(f"    {label} dias: {shift_dist[delta]}")

    # Unmatched NFS-e
    if nfse_only:
        print(f"\n  NFS-e SEM MATCH (primeiras 30):")
        for n in sorted(nfse_only, key=lambda x: x["nfse_data"])[:30]:
            print(f"    Nota {n['nfse_num']:<6} | {n['nfse_data']} | {fmt(n['nfse_valor'])}")

    # Save JSON
    output_path = os.path.join(os.path.dirname(__file__), "..", "output", "conciliacao_202602.json")
    with open(output_path, "w") as f:
        json.dump({
            "periodo": periodo,
            "nota": "CSV tem apenas notas COM rateio (549 de 1040 total). Trinks tem todas as transações.",
            "resumo": {
                "nfse_rateio": len(nfse_list),
                "nfse_rateio_valor": total_nfse_valor,
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
            "trinks_only": [
                {"id": t["id"], "data": t["data"], "valor": t["valor"],
                 "cliente": t["cliente"], "servicos": t["servicos"]}
                for t in sorted(trinks_only, key=lambda x: x["data"])
            ],
        }, f, indent=2, ensure_ascii=False)
    print(f"\n  Detalhes salvos em: {output_path}")


if __name__ == "__main__":
    main()
