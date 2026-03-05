# Quadro Financeiro Janeiro 2026 — Análise Trinks vs PDF

Fonte PDF: `~/Downloads/Depillagos - Quadro financeiro Janeiro 2026.pdf`
Fonte Trinks: API `/v1/lancamentos?DataInicio=2026-01-01&DataFim=2026-01-31` (146 registros)

---

## Cruzamento por bloco

### 1. Passivos (Fora da Operação)

| Item | PDF | Trinks (Empréstimos/Financiamentos) |
|------|-----|--------------------------------------|
| Capital de Giro | R$6.750 | — |
| Pronampe | R$2.649 | — |
| FGE | R$3.140 | — |
| **Total** | **R$12.539** | **R$13.457,35** |

Diferença: +R$918. Trinks agrupa tudo como "Empréstimos / Financiamentos" sem detalhar por linha de crédito.

### 2. Despesas Fixas Operacionais

| Item | PDF | Trinks |
|------|-----|--------|
| Aluguel Bacaxá | R$1.354 | — (Trinks: Aluguel total R$12.197,24) |
| Salários CLT | R$14.846 | R$14.857,13 (Pagamento Profissional) |
| Aluguel Araruama | R$10.500 | — (incluído no total acima) |
| Contador | R$1.300 | R$1.300,00 |
| **Total** | **R$28.000** | **R$28.354,37** |

Diferença: +R$354. Aluguel no PDF soma R$11.854 vs Trinks R$12.197. Salários batem (~R$11 de diferença).

### 3. Insumos Variáveis

| Área | PDF (semanal: 10, 17, 24, 31 jan) | PDF Total |
|------|-------------------------------------|-----------|
| Material Manicure | 2.384 + 25 + 0 + 111 | R$2.520 |
| Material Depilação | 670 + 0 + 177 + 0 | R$847 |
| Material Cabelo | 84 + 0 + 0 + 0 | R$84 |
| Material Estética | 154 + 0 + 0 + 0 | R$154 (~R$50 na semana 24?) |
| Material Laser | 64 + 0 + 0 + 0 | R$64 |
| **Total** | | **R$3.479** |

Trinks (Compra de Produto + Descartáveis): **R$4.603,41**. Diferença: +R$1.124. Trinks pode incluir itens que o PDF não classifica como insumo.

### 4. Despesas Variáveis

| Item | PDF | Trinks |
|------|-----|--------|
| Marketing | R$3.435 | R$3.435,99 |
| Simples | R$10.500 | R$15.165,22 (Imposto) |
| **Total** | **R$13.935** | **R$18.601,21** |

Marketing bate. Imposto no Trinks é R$4.665 maior que o "Simples" do PDF — possível que Trinks inclua impostos adicionais (INSS, ISS, etc.) que o quadro não lista.

### 5. Comissões Variáveis

| Área (%) | Sem 10/jan | Sem 17/jan | Sem 24/jan | Sem 31/jan | PDF Total |
|----------|-----------|-----------|-----------|-----------|-----------|
| Manicure (50%) | R$7.571 | R$6.874 | R$6.116 | R$7.029 | ~R$27.590 |
| Depiladora (4%) | R$932 | R$406 | R$315 | R$365 | ~R$2.018 |
| Cabeleireiras (50%) | R$1.092 | R$5.298 | R$880 | R$650 | ~R$7.920 |
| Estética (2%) | R$10 | R$49 | R$86 | R$14 | ~R$159 |
| Laser (2%) | R$58 | R$6 | R$55 | R$64 | ~R$183 |
| **Total** | **R$9.073** | **R$7.633** | **R$6.431** | **R$8.105** | **R$31.242** |

Trinks "Comissão" total: **R$21.420,16** (por semana: 982 + 8.404 + 6.438 + 5.596)

**Gap de ~R$9.822** — provável que Manicure e Cabeleireiras (parceiras MEI com rateio 50%) venham do relatório **Avec**, não do Trinks. Apenas Depiladora (4%), Estética (2%) e Laser (2%) parecem estar no Trinks.

### 6. Caixa Disponível

| Semana | Caixa Real | Dinheiro Comprometido | Caixa Disponível |
|--------|-----------|----------------------|-----------------|
| 01 jan | R$40.000 | R$49.300 | -R$9.300 |
| 10 jan | R$21.362 | R$31.300 | -R$9.938 |
| 17 jan | R$19.956 | R$19.433 | R$523 |
| 24 jan | R$13.735 | R$7.731 | R$6.004 |
| 31 jan | R$30.006 | R$0 | R$30.006 |

Não validável pelo Trinks (depende de saldo bancário + caixa físico).

---

## Categorias Trinks sem correspondência no PDF

| Grupo > Categoria | Valor |
|-------------------|-------|
| Despesas Variáveis > Manutenção | R$4.255,54 |
| Despesas Variáveis > Luz | R$1.670,23 |
| Pessoal > Passagem/Vale Transporte | R$1.352,40 |
| Despesas Variáveis > Transporte Operacional | R$543,00 |
| Pessoal > Vale/Adiantamento Profissional | R$150,00 |
| Despesas Variáveis > Gás | R$105,00 |
| Despesas Variáveis > Limpeza | R$66,50 |
| Despesas Variáveis > Telefone | R$35,41 |
| **Total não mapeado** | **R$8.178,08** |

---

## Pendências para Fevereiro

1. **Avec**: Preciso do relatório Avec de Fevereiro para comissões de Manicure (50%) e Cabeleireiras (50%)
2. **Impostos**: Confirmar se "Simples" no quadro = todo o grupo "Imposto" no Trinks, ou apenas uma parte
3. **Categorias não mapeadas**: Decidir onde Manutenção, Luz, VT, Gás etc. entram no quadro do Miro
4. **Corte semanal**: Confirmado que é a cada sábado. Sábados de fevereiro 2026: 7, 14, 21, 28
5. **Insumos**: Alinhar quais categorias Trinks compõem "Insumos Variáveis" (Compra de Produto? Descartáveis? Manutenção?)

## Processo para gerar quadro de Fevereiro

1. Puxar `/v1/lancamentos?DataInicio=2026-02-01&DataFim=2026-02-28`
2. Agrupar por semana (sábados: 7, 14, 21, 28 fev)
3. Mapear categorias Trinks → blocos do quadro Miro
4. Complementar comissões Manicure/Cabeleireiras com relatório Avec
5. Caixa disponível: input manual (saldo banco + caixa)
