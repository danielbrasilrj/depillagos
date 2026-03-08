# Depillagos

## O Negócio

Centro de estética fundado em **2008 por Luciene Freitas** em Araruama/RJ (Região dos Lagos). Começou como estúdio de depilação a cera e cresceu para um centro completo com 2 unidades, 25 profissionais e 26K+ clientes cadastrados. CNPJ: 09.223.558/0001-00.

**Filosofia:** "A beleza vem em todas as formas, tamanhos e cores." Atendimento acolhedor, sem hora marcada, preços acessíveis. O relacionamento de confiança com o cliente é o centro de tudo.

**Público:** majoritariamente feminino, classe B/C, cidade de ~140K habitantes. Cultura de walk-in (chega e é atendido), WhatsApp como canal principal. Concorrência local fraca em laser e estética avançada.

**Modelo de negócio:** equipe própria cuida da depilação (cera e laser). Profissionais parceiros (MEIs) fazem manicure, pedicure, sobrancelha, escova, etc. no espaço do salão. Valores divididos via **rateio** (geralmente 50/50, com exceções como banho de gel 40/60). Isso gera NFS-e com cota parte que precisa ir pro contador todo mês.

**Unidades:**
- **Araruama** (matriz): Rua Francisco A. da Silva, 120 — todos os serviços

**Serviços (10 categorias, 153 no catálogo):**
- Depilação a laser — diferencial principal: laser 4D alemão com 4 comprimentos de onda, primeiro da Região dos Lagos, atende todos os fototipos incluindo peles bronzeadas
- Depilação a cera (feminina e masculina) e na linha
- Manicure e pedicure (exclusivo Araruama, feito por parceiras MEI)
- Estética facial e corporal (exclusivo Araruama)
- Design de sobrancelha (exclusivo Araruama)
- Cabeleireiro — escova, corte, coloração (exclusivo Araruama)

**Contato:** WhatsApp (22) 99235-4970 | [depillagos.com.br](https://depillagos.com.br) | @depillagosararuama (Facebook) | @_depillagos (Instagram)

## Operação

**Trinks** é o sistema de gestão (POS) usado no dia a dia do salão: cadastro de clientes, catálogo de serviços, agendamentos, registro de atendimentos e pagamentos, gestão de profissionais. É a fonte de verdade dos dados operacionais. API REST disponível (docs: https://trinks.readme.io/reference/introducao).
Utilize o Trinks MCP para extrair dados de clientes, serviços, atendimentos e pagamentos conforme necessário para os projetos.

**Notas fiscais:** cada atendimento gera uma NFS-e emitida pelo município. Quando há rateio com parceiro MEI, a nota descreve a divisão de valores. Todo mês o Daniel precisa extrair essas notas e mandar pro contador.

**Clube Depillagos** é o programa de fidelidade do salão, integrado ao app:
- Pontos: 1 ponto por R$1 gasto, com bônus de 20% pra quem usa o app e bônus por streak (frequência semanal)
- Punch card: 10 visitas = 1 serviço grátis (até R$50)
- Indicações: código único por cliente, 200pts por indicação
- Vouchers: troca de pontos por descontos (200pts→R$10, 500pts→R$30, 1000pts→serviço grátis)
- Pontos calculados automaticamente a partir das transações registradas no Trinks

## Projetos do Daniel

### App do salão (`depillagos_app_v2/`, repo separado)
App mobile + web para clientes: catálogo, fidelidade (Clube Depillagos), push notifications com IA.
- Stack: NestJS + React Native/Expo + PostgreSQL + TypeScript
- Path: `/Users/danielcarmo/Env/Projects/personal/depillagos_app_v2`

### Extração de notas fiscais (`depillagos_notas_fiscais/`)
Script Python que puxa NFS-e e gera relatório mensal pro contador. Certificado A1 com mTLS.
- Detalhes em `depillagos_notas_fiscais/CLAUDE.md`

### Contrato de locação (`contrato_locacao/`)
Análise jurídica e contraproposta do contrato de locação do imóvel da matriz.
- Detalhes em `contrato_locacao/CLAUDE.md`

### Controle financeiro (`controle_financeiro/`)
Cruzamento do quadro financeiro mensal (Miro) com dados do Trinks e Avec. Corte semanal aos sábados.

### Câmeras de monitoramento (`cameras_monitoramento/`)
Monitoramento inteligente com contagem de clientes via IA e reconhecimento facial. Câmeras PoE + Mini PC local + Oracle Cloud.
- Detalhes em `cameras_monitoramento/CLAUDE.md`

### Depillagos Hair (`depillagos_hair/`)
Landing page estática do setor de cabeleireiro. Tema sazonal, campanha Mês da Mulher (mar/2026). Vercel + Hostinger.
- Detalhes em `depillagos_hair/CLAUDE.md`

### Novo site institucional (`site/`)
Novo depillagos.com.br — site estático com preços reais do Trinks, substituindo o WordPress atual (lento, desatualizado).
- Detalhes em `site/CLAUDE.md`

### Tráfego pago (`trafego_pago/`)
Ainda sem implementação.

## Regras de desenvolvimento

- Sempre carregar skill `tdd` antes de escrever código
- TDD em vertical slices (teste + código juntos, nunca separados)
- Nunca commitar `.env`, certificados ou senhas
- Mercado brasileiro: pt-BR, WhatsApp-first, formatos BR (vírgula decimal, DD/MM/AAAA)
