# Depillagos

## O Negócio

Centro de estética fundado em **2008 por Luciene Freitas** em Araruama/RJ (Região dos Lagos). Começou como estúdio de depilação a cera e cresceu para um centro completo com 2 unidades, 25 profissionais e 26K+ clientes cadastrados. CNPJ: 09.223.558/0001-00.

**Filosofia:** "A beleza vem em todas as formas, tamanhos e cores." Atendimento acolhedor, sem hora marcada, preços acessíveis. O relacionamento de confiança com o cliente é o centro de tudo.

**Público:** majoritariamente feminino, classe B/C, cidade de ~140K habitantes. Cultura de walk-in (chega e é atendido), WhatsApp como canal principal. Concorrência local fraca em laser e estética avançada.

**Modelo de negócio:** equipe própria cuida da depilação (cera e laser). Profissionais parceiros (MEIs) fazem manicure, pedicure, sobrancelha, escova, etc. no espaço do salão. Valores divididos via **rateio** (geralmente 50/50, com exceções como banho de gel 40/60). Isso gera NFS-e com cota parte que precisa ir pro contador todo mês.

**Unidades:**
- **Araruama** (matriz): Rua Francisco A. da Silva, 120 — todos os serviços
- **Bacaxá** (filial): Rua Prof. Francisco Fonseca, 177 — apenas depilação (cera e laser)

**Serviços (10 categorias, 153 no catálogo):**
- Depilação a laser — diferencial principal: laser 4D alemão com 4 comprimentos de onda, primeiro da Região dos Lagos, atende todos os fototipos incluindo peles bronzeadas
- Depilação a cera (feminina e masculina) e na linha
- Manicure e pedicure (exclusivo Araruama, feito por parceiras MEI)
- Estética facial e corporal (exclusivo Araruama)
- Design de sobrancelha (exclusivo Araruama)
- Cabeleireiro — escova, corte, coloração (exclusivo Araruama)

**Contato:** WhatsApp (22) 99235-4970 | [depillagos.com.br](https://depillagos.com.br) | @depillagosararuama (Instagram e Facebook)

## Operação

**Trinks** é o sistema de gestão (POS) usado no dia a dia do salão: cadastro de clientes, catálogo de serviços, agendamentos, registro de atendimentos e pagamentos, gestão de profissionais. É a fonte de verdade dos dados operacionais. API REST disponível (docs: https://trinks.readme.io/reference/introducao).

**Notas fiscais:** cada atendimento gera uma NFS-e emitida pelo município. Quando há rateio com parceiro MEI, a nota descreve a divisão de valores. Todo mês o Daniel precisa extrair essas notas e mandar pro contador.

**Clube Depillagos** é o programa de fidelidade do salão, integrado ao app:
- Pontos: 1 ponto por R$1 gasto, com bônus de 20% pra quem usa o app e bônus por streak (frequência semanal)
- Punch card: 10 visitas = 1 serviço grátis (até R$50)
- Indicações: código único por cliente, 200pts por indicação
- Vouchers: troca de pontos por descontos (200pts→R$10, 500pts→R$30, 1000pts→serviço grátis)
- Pontos calculados automaticamente a partir das transações registradas no Trinks

## Projetos do Daniel

### App do salão (`depillagos_app_v2/`, repo separado)
App mobile + web para clientes. Catálogo de serviços, login por telefone (verificado contra o Trinks), Clube Depillagos (fidelidade), push notifications com sugestões inteligentes via IA, painel admin. WhatsApp como canal de contato (sem agendamento online no MVP).
- Stack: NestJS + React Native/Expo + PostgreSQL + TypeScript
- Repo: `git@github-personal:danielbrasilrj/depillagos_app_v2.git`
- Path local: `/Users/danielcarmo/Env/Projects/personal/depillagos_app_v2`

### Extração de notas fiscais (`depillagos_notas_fiscais/`, neste repo)
Script Python que puxa NFS-e da API nacional, identifica notas com rateio de parceiros, e gera CSV/XLSX mensal pro contador. Usa certificado digital A1 com mTLS.
- Detalhes técnicos em `depillagos_notas_fiscais/CLAUDE.md` e `REGRAS_EXTRACAO_NOTAS.md`

### Contrato de locação — Araruama (`docs/`)
Imóvel da matriz locado há ~18 anos. Locador mudou de pessoa física (Sr. Nilço Henrique de Paiva) para PJ (Paiva Administradora de Bens Próprios Ltda). Novo contrato de 60 meses (jan/2025–jan/2030) ainda **não assinado** — aguardando Daniel ir ao Brasil.

O "contrato" é a Declaração de Recebimento + Vistoria preparada pelo escritório Mayren S. Guimarães (advogadas). Não existe documento separado de "contrato de locação" — a Declaração+Vistoria é o documento a ser assinado. As "cláusulas 8ª e 9ª" referenciadas no texto são do contrato anterior (36 meses).

**Originais em `docs/`:**
- `Mayren S. Guimarães.pdf` / `(1).pdf` — Declaração+Vistoria original (6 págs, scan do escritório)
- `CamScanner 11-02-2026 16.21.pdf` — Declaração anterior (Sr. Nilço, 36 meses)

**Gerados em `outputs/`:**
- `Analise_Juridica_Depillagos.pdf` — análise jurídica completa (8 págs)
- `Declaracao_Vistoria_Contraproposta_Depillagos.pdf` — versão com alterações marcadas [ALTERADO]
- `Declaracao_Vistoria_Final_Depillagos.pdf` — versão limpa pronta para apresentar à locadora

**Script:** `gerar_contrato_final.py` — Python (reportlab) que gera o PDF final

**Pontos críticos identificados na análise:** transferência indevida de responsabilidade do telhado, proibição de acesso ao telhado, vistoria como armadilha de devolução, ausência de reconhecimento das benfeitorias, restrição à fachada, telhas de amianto nas laterais.

### Tráfego pago (`trafego_pago/`, neste repo)
Ainda sem implementação.

## Regras de desenvolvimento

- Sempre carregar skill `tdd` antes de escrever código
- TDD em vertical slices (teste + código juntos, nunca separados)
- Nunca commitar `.env`, certificados ou senhas
- Mercado brasileiro: pt-BR, WhatsApp-first, formatos BR (vírgula decimal, DD/MM/AAAA)
