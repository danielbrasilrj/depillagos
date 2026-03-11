# Contador Inteligente — Reorganização Tributária Depillagos

## O que é

Estudo de reorganização tributária da Depillagos. Entregável principal: apresentação HTML estática com diagnóstico fiscal, cenários e plano de ação.

**URL:** https://contadorinteligente.vercel.app
**Arquivo:** `index.html` (copiar para `public/index.html` antes de deploy)

---

## Números Reais (já levantados)

### Faturamento e impostos
- **Faturamento bruto:** ~R$100.000/mês (maquininha)
- **Impostos totais:** R$11.420/mês (Simples R$7.715 + INSS R$1.129 + FGTS R$1.045 + outros R$1.531)
- **Regime:** Simples Nacional, ~10% de alíquota efetiva

### Comissões MEI (Avec 2025 — dados reais)
- **Total 2025:** R$355.693 | **Média:** R$29.641/mês
- **Manicure:** R$23.749/mês (80%) — 13 profissionais
- **Cabeleireiro:** R$5.789/mês (20%) — Priscila, Jacqueline, Noemi
- **Sazonalidade:** jan R$21.730 (vale) → dez R$45.533 (pico)
- **Top:** Jhennifer R$3.345/mês, Priscila R$2.970/mês, Camila R$2.809/mês
- **Fonte:** `docs/comissoes_pagas_2025_avec.xlsx` (559 pagamentos, 20 profissionais)

### Base de cálculo real do Simples
- Faturamento bruto R$100K - cota parte R$29.641 = **base ~R$70.359/mês**
- A cota parte JÁ está sendo deduzida corretamente (Lei 13.352/2016)

---

## Equipe (corrigido)

### CLT (8 profissionais)
- **Depiladoras:** Ana Carolina, Daiane, Patricia, Yasmin M.
- **Recepção:** Yasmin (recepção), Simone
- **Esteticista/Laser:** Caroline (CLT, não MEI)
- **Limpeza:** Renata

### MEI Parceiras (16+ via Avec)
- **Manicure:** Jhennifer, Dalleti, Itaciana, Camila, Jari, Washilla, Monica, Isabella, Josiane, Thays, Sabrina, Amanda, Eychila
- **Cabeleireiras:** Priscila, Jacqueline, Noemi
- **Modelo:** rateio 50/50 com cota parte na NFS-e
- **Contratos:** maioria formalizada, faltam 2-3 profissionais novas

---

## Conclusões do Diagnóstico

### O que já funciona
- Salão-Parceiro (Lei 13.352) aplicado corretamente com cota parte
- Cota parte deduzida da NFS-e = Simples incide sobre ~R$70K, não R$100K
- Contratos de parceria quase 100% formalizados

### Cenário B (Coworking) — DESCARTADO
Matematicamente desvantajoso: taxa de uso (ex: R$20) < cota parte atual (R$32,50 num serviço de R$65). Salão perderia receita.

### Cenário D (Holding) — ANALISADO, risco/retorno questionável
- Economia líquida estimada: R$300-2.000/mês (depende da faixa do Simples)
- Custo extra: ~R$700/mês (2o contador + taxas)
- Pior caso fiscal (5 anos, R$15K/mês): multa ~R$170K
- Para Araruama (140K hab, faturamento R$100K): baixo radar, mas risco de denúncia em cidade pequena

### Próximos passos pendentes
1. **Confirmar faixa exata do Simples** com o contador (DAS últimos 12 meses)
2. **Formalizar contratos** das 2-3 MEIs novas
3. **Garantir NFS-e de cada MEI** — 3 opções documentadas na apresentação
4. **Reunião com contador** levando o diagnóstico
5. **Decisão:** Cenário A (otimizar o que já tem) vs Cenário C/D (holding)

---

## Problema NFS-e das MEIs

Cada MEI precisa emitir nota da sua cota parte. Hoje não acontece consistentemente.

**3 opções documentadas:**
1. **Recepção emite** com procuração (recomendado para começar)
2. **MEIs emitem** pelo app NFS-e Mobile (pouco confiável)
3. **Automação via API** NFS-e Nacional (futuro) — Trinks fornece DADOS, NFS-e Nacional faz a EMISSÃO. Reaproveitar projeto `depillagos_notas_fiscais/`.

---

## Fontes de Dados

| Fonte | O que tem | Status |
|-------|-----------|--------|
| Trinks MCP | Atendimentos, lançamentos, profissionais, serviços | Usado |
| Avec 2025 (`docs/comissoes_pagas_2025_avec.xlsx`) | Comissões MEI mensais (559 pagamentos) | Analisado |
| `controle_financeiro/quadro_financeiro_jan2026_analise.md` | Cruzamento Trinks vs PDF jan/2026 | Referência |
| DAS/guias do contador | Faixa exata do Simples | **Pendente** |

---

## Regras

- Tudo em pt-BR, valores em R$ com vírgula decimal
- Não dar conselho jurídico definitivo — recomendar validação com advogado/contador
- Priorizar modelos que mantenham controle operacional centralizado
- Considerar realidade de cidade pequena (Araruama)
