# Contador Inteligente — Reorganização Tributária Depillagos

## Objetivo

Estudar e planejar uma reorganização tributária legal para a Depillagos, reduzindo carga fiscal sem perder controle operacional (agenda, clientes, marca, financeiro centralizado).

**Meta:** reduzir os ~R$10.000/mês de impostos em 20-40% através de estruturação jurídica e fiscal adequada.

---

## Contexto da Empresa

- **18 anos de operação** | Araruama-RJ | ~1.000 atendimentos/mês
- **Regime atual:** Simples Nacional | ~R$10.000/mês de impostos
- **Equipe CLT:** 4 depiladoras, 2 recepcionistas, 1 aux. limpeza
- **Parceiros MEI:** 10 manicures (50/50), 2 cabeleireiras (50/50)
- **Esteticista laser:** MEI, fixa R$2.300/mês (recusou CLT)
- **Fluxo atual:** cliente paga à clínica → clínica repassa % ao profissional

---

## Fases do Projeto

### Fase 1 — Diagnóstico Fiscal (Levantamento de Dados)

**Objetivo:** Entender exatamente quanto se paga de imposto e sobre o quê.

Tarefas:
- [ ] **1.1** Levantar faturamento bruto mensal via Trinks (últimos 6 meses)
- [ ] **1.2** Separar faturamento por categoria: laser, cera, manicure, cabelo, estética
- [ ] **1.3** Identificar quanto do faturamento bruto é repasse a parceiros MEI
- [ ] **1.4** Verificar: imposto está sendo pago sobre faturamento total ou só sobre receita líquida da empresa?
- [ ] **1.5** Levantar DAS mensal (Simples Nacional) — faixa de alíquota atual
- [ ] **1.6** Mapear todas as despesas operacionais fixas e variáveis (usar dados do `controle_financeiro/`)
- [ ] **1.7** Identificar faturamento total vs. receita real da Depillagos (descontando repasses)

**Pergunta-chave a responder:** A Depillagos está pagando imposto sobre R$X de faturamento bruto quando deveria pagar sobre R$Y de receita real?

**Fontes de dados:**
- Trinks MCP: `/v1/lancamentos`, `/v1/atendimentos`, `/v1/profissionais`
- `controle_financeiro/quadro_financeiro_jan2026_analise.md`
- DAS e guias de pagamento (pedir ao Daniel)

### Fase 2 — Análise de Ineficiências Tributárias

**Objetivo:** Identificar onde se paga imposto desnecessário.

Tarefas:
- [ ] **2.1** Calcular imposto pago sobre repasses a parceiros (erro clássico dos 80% dos salões)
- [ ] **2.2** Verificar se a Lei do Salão Parceiro (13.352/2016) está sendo aplicada corretamente
  - NFS-e com cota parte está correta?
  - O valor de repasse está sendo deduzido da base de cálculo do Simples?
- [ ] **2.3** Analisar situação da esteticista laser (MEI com remuneração fixa = risco trabalhista + ineficiência fiscal)
- [ ] **2.4** Verificar enquadramento CNAE atual e se há CNAEs mais vantajosos
- [ ] **2.5** Calcular quanto se economizaria só com a aplicação correta do Salão-Parceiro

### Fase 3 — Modelagem de Cenários

**Objetivo:** Simular diferentes estruturas e calcular economia real de cada uma.

#### Cenário A — Salão-Parceiro Otimizado (menor mudança)
- [ ] **3A.1** Aplicar corretamente a Lei 13.352/2016 para todos os MEIs
- [ ] **3A.2** Garantir que repasses não entram na base de cálculo do Simples
- [ ] **3A.3** Revisar contratos de parceria existentes
- [ ] **3A.4** Calcular economia estimada

#### Cenário B — Coworking Estético (mudança média)
- [ ] **3B.1** Modelar estrutura: profissionais pagam taxa fixa de uso do espaço
- [ ] **3B.2** Salão fatura sobre taxa de uso, não sobre serviço total
- [ ] **3B.3** Definir valores de taxa (fixa vs. % do faturamento)
- [ ] **3B.4** Analisar impacto no controle operacional (agenda, clientes)
- [ ] **3B.5** Calcular economia estimada
- [ ] **3B.6** Mapear riscos (perda de controle, risco trabalhista reverso)

#### Cenário C — Modelo Híbrido (recomendado para grandes)
- [ ] **3C.1** Combinar Salão-Parceiro + aluguel de espaço + comissão administrativa
- [ ] **3C.2** Definir quais profissionais entram em qual modelo
- [ ] **3C.3** Calcular economia estimada
- [ ] **3C.4** Mapear complexidade contábil adicional

#### Cenário D — Holding Operacional / Divisão de Empresas (maior mudança)
- [ ] **3D.1** Modelar Empresa 1 (operacional: serviços) + Empresa 2 (estrutura: aluguel/marca/equipamentos)
- [ ] **3D.2** Definir como dividir faturamento entre empresas
- [ ] **3D.3** Verificar viabilidade no Simples Nacional para ambas
- [ ] **3D.4** Calcular economia vs. custo de manter 2 CNPJs
- [ ] **3D.5** Analisar riscos de planejamento tributário abusivo (simulação/fraude)

### Fase 4 — Matriz de Decisão

**Objetivo:** Comparar cenários de forma objetiva.

- [ ] **4.1** Montar tabela comparativa:

| Critério | Cenário A | Cenário B | Cenário C | Cenário D |
|----------|-----------|-----------|-----------|-----------|
| Economia mensal estimada | | | | |
| Complexidade de implementação | | | | |
| Custo de transição | | | | |
| Risco trabalhista | | | | |
| Risco fiscal (Receita Federal) | | | | |
| Impacto operacional | | | | |
| Controle mantido? | | | | |
| Necessidade de novo contador? | | | | |

- [ ] **4.2** Recomendar cenário ideal (provavelmente A+C combinados)

### Fase 5 — Plano de Implementação

**Objetivo:** Criar roadmap de transição sem quebrar operação.

- [ ] **5.1** Definir estrutura jurídica escolhida
- [ ] **5.2** Listar contratos necessários:
  - Contrato de parceria (Lei 13.352)
  - Contrato de locação de espaço/cadeira
  - Contrato de prestação de serviço administrativo
  - Contrato de licenciamento de marca (se Cenário D)
- [ ] **5.3** Definir cronograma de transição (sugestão: 3-6 meses)
- [ ] **5.4** Criar checklist para contador:
  - Ajuste de NFS-e e cota parte
  - Reclassificação de receitas no Simples
  - Novos CNAEs se necessário
- [ ] **5.5** Definir como manter controle operacional em cada modelo:
  - Agenda via Trinks continua centralizada
  - Clientes permanecem na base da Depillagos
  - Marca é da Depillagos independente do modelo
- [ ] **5.6** Plano de comunicação com profissionais parceiras

### Fase 6 — Documentação e Entregáveis

- [ ] **6.1** Documento final: "Reorganização Tributária Depillagos"
- [ ] **6.2** Modelos de contrato (rascunho para advogado revisar)
- [ ] **6.3** Planilha de simulação fiscal (comparativo antes/depois)
- [ ] **6.4** Checklist para reunião com contador
- [ ] **6.5** FAQ para profissionais parceiras

---

## Riscos e Alertas

### Riscos Trabalhistas
- **Esteticista laser com remuneração fixa:** mesmo sendo MEI, se há subordinação + habitualidade + pessoalidade + onerosidade, pode configurar vínculo empregatício. Precisa atenção.
- **Manicures e cabeleireiras:** a Lei do Salão-Parceiro protege, MAS exige contrato formal e autonomia real da profissional.

### Riscos Fiscais
- **Planejamento tributário abusivo:** se a Receita entender que a divisão de empresas é artificial (sem propósito negocial), pode autuar. Cenário D exige justificativa econômica real.
- **Coworking:** precisa ficar claro que o profissional tem autonomia real, não é empregado disfarçado.

### O que NÃO mudar
- Controle da agenda (Trinks)
- Relacionamento com clientes (base é da Depillagos)
- Marca e posicionamento
- Qualidade e padronização dos serviços

---

## Dependências

- **Dados do Trinks:** faturamento, atendimentos, repasses (Trinks MCP disponível)
- **Dados do contador:** DAS mensal, alíquota atual, faixa do Simples
- **Dados financeiros:** `controle_financeiro/` (quadro financeiro mensal)
- **Consulta jurídica:** contratos devem ser revisados por advogado trabalhista/tributário
- **Decisão do Daniel:** qual cenário implementar

---

## Regras deste Projeto

- Tudo em pt-BR
- Valores em R$ com vírgula decimal
- Não dar conselho jurídico definitivo — sempre recomendar validação com advogado/contador
- Usar dados reais do Trinks sempre que possível
- Priorizar modelos que mantenham controle operacional centralizado
- Considerar a realidade de cidade pequena (Araruama, 140K hab) — estruturas muito complexas podem não compensar
