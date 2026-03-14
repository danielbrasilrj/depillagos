# Projeto Depilagos - Notas Fiscais

## Contexto

Este projeto gerencia Notas Fiscais de Serviço Eletrônicas (NFS-e) do **CENTRO DE ESTETICA DEPILAGOS LTDA** (CNPJ: 09.223.558/0001-00), Araruama/RJ. Duas funções principais:

1. **Dashboard NFS-e** — painel web que mostra o total de NFS-e emitidas no mês em tempo real
2. **Extração mensal** — gera CSV com notas de cota parte (rateio MEI) para o contador

## O que é o rateio

A Depilagos trabalha com profissionais parceiros (MEIs com CNPJ próprio) que prestam serviços no espaço do salão. Quando um serviço é feito por um parceiro, o valor é dividido entre o salão e o profissional. Essa divisão é chamada de **rateio** e aparece descrita no corpo da NFS-e.

## Estrutura do projeto

```
├── dashboard/                 # Dashboard web NFS-e (Vercel)
│   ├── api/
│   │   └── nfse.js           # Serverless: busca Trinks, filtra cartão/PIX
│   ├── public/
│   │   └── index.html        # Frontend single-page (dark theme)
│   ├── vercel.json
│   └── package.json
├── scripts/
│   ├── extrair_notas.py      # Extração mensal via ADN (cota parte MEI)
│   ├── conciliar_fev.py      # Conciliação NFS-e vs Trinks (fev/2026)
│   └── conciliar.py          # Conciliação genérica (requer ADN online)
├── tests/
│   ├── conftest.py           # Configura sys.path para imports
│   ├── test_extrair_notas.py # Testes unitários (extração)
│   └── test_resumo_notas.py  # Testes unitários (resumo, comparação, histórico)
├── certificado/              # Certificado digital A1 (.pfx) - NÃO commitado
├── docs/                     # PDFs de referência e documentos auxiliares
├── output/                   # CSVs, resumos e JSONs gerados
├── REGRAS_EXTRACAO_NOTAS.md  # Regras de extração e padrões
└── CLAUDE.md
```

## Método principal: API NFS-e Nacional (ADN)

### Pré-requisitos
- Python 3
- OpenSSL (para extrair cert/key do .pfx)
- curl
- Certificado digital A1 (.pfx) da Depilagos

### Como executar

```bash
# Extrair TODAS as notas com rateio
python3 scripts/extrair_notas.py

# Filtrar por período (gera CSV + resumo .txt)
python3 scripts/extrair_notas.py --periodo 2026-02

# Dias depois, verificar se tem notas novas (mesmo comando!)
python3 scripts/extrair_notas.py --periodo 2026-02

# Salvar em arquivo específico
python3 scripts/extrair_notas.py --output resultado.csv
```

Quando `--periodo` é passado:
- **Auto-output:** sem `--output`, o CSV vai para `output/{mes_abrev}{ano}.csv` (ex: `output/fev2026.csv`)
- **Se CSV já existe:** compara com a nova extração e só sobrescreve se houver notas novas
- **Resumo:** gera `output/resumo_{mes_abrev}{ano}.txt` com status, totais, breakdown e histórico de atualizações
- **Histórico:** cada execução registra uma entrada no resumo (primeira extração, atualização, ou verificação)

### API NFS-e Nacional

- **Base URL:** `https://adn.nfse.gov.br/contribuintes`
- **Autenticação:** mTLS com certificado A1 ICP-Brasil
- **Swagger/Docs:** `https://adn.nfse.gov.br/contribuintes/docs/index.html`
- **Spec OpenAPI:** `https://adn.nfse.gov.br/contribuintes/swagger/v1/swagger.json`

#### Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/DFe/{NSU}?cnpjConsulta={CNPJ}&lote=true` | Distribuição de documentos por NSU (lote de 50) |
| GET | `/NFSe/{ChaveAcesso}/Eventos` | Eventos vinculados a uma NFS-e |

#### Como funciona a distribuição por NSU
- A API retorna lotes de até 50 documentos a partir de um NSU (Número Sequencial Único).
- Cada documento contém o XML da NFS-e compactado (GZip + Base64).
- Para buscar tudo: começar do NSU 1 e ir incrementando até receber `NENHUM_DOCUMENTO_LOCALIZADO`.
- O XML contém os dados do rateio no campo `<xDescServ>`.

### Estrutura do XML da NFS-e

```xml
<xDescServ>
  SERVIÇO R$ valor
  SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$valor_salao
  PROFISSIONAL-PARCEIRO: CNPJ_PARCEIRO COTA-PARTE R$valor_parceiro
</xDescServ>
```

**Campos importantes no XML:**
- `<nNFSe>` - Número da NFS-e
- `<dCompet>` - Data de competência (data do serviço) formato YYYY-MM-DD
- `<dhProc>` - Data de processamento (emissão) formato YYYY-MM-DDThh:mm:ss
- `<vServ>` - Valor total do serviço
- `<xDescServ>` - Descrição com dados do rateio
- `<CNPJ>` em `<emit>` - CNPJ do emissor (Depilagos)
- `<CPF>` ou `<CNPJ>` em `<toma>` - CPF/CNPJ do tomador (cliente)
- Namespace: `http://www.sped.fazenda.gov.br/nfse`

### Identificação de rateio no XML
- **TEM rateio:** `xDescServ` contém `PROFISSIONAL-PARCEIRO`
- **NÃO tem rateio:** `xDescServ` contém apenas `SALAO-PARCEIRO` (cota 100% salão)
- Regex para extrair cotas: `(SALAO-PARCEIRO|PROFISSIONAL-PARCEIRO):\s*(\d{11,14})\s+COTA-PARTE\s+R\$([\d.]+(?:,\d+)?)`

## Certificado Digital

- **Tipo:** A1 (.pfx)
- **Titular:** CENTRO DE ESTETICA DEPILAGOS LTDA
- **e-CNPJ:** 09.223.558/0001-00
- **Validade:** até 21/07/2026
- **Arquivo:** `certificado/DEPILAGOS MATRIZ 2025.pfx` (não commitado)
- **Senha:** informada via `--senha`, variável `DEPILAGOS_PFX_PASSWORD` ou input interativo (nunca commitada)

## Formato do CSV de saída

- **Delimitador:** `;` (ponto-e-vírgula)
- **Valores:** vírgula como separador decimal
- **Colunas:**

```
data servico;data emissao;NUMERO DA NOTA;CNPJ PROFISSIONAL PARCEIRO;COTA PARTE SALÃO PARCEIRO;COTA PARTE PROFISSIONAL-PARCEIRO
```

## Delay da API e verificação de completude

A API NFS-e Nacional (ADN) tem um **delay entre a emissão da nota pelo município e a disponibilização via distribuição por NSU**. Isso significa que ao rodar `extrair_notas.py` no fim do mês, as notas dos últimos dias podem ainda não estar disponíveis. Esse delay varia, mas pode ser de 1 a 3 dias.

### Como verificar se o CSV está completo

Basta rodar o mesmo comando de extração novamente:

```bash
# Primeira extração do mês
python3 scripts/extrair_notas.py --periodo 2026-02

# 2-3 dias depois, verificar se tem notas novas
python3 scripts/extrair_notas.py --periodo 2026-02
```

O script automaticamente:
1. Detecta o CSV existente (`output/fev2026.csv`)
2. Consulta a API e compara com o CSV
3. **Sem diferença** → não sobrescreve, registra "Verificação" no histórico
4. **Com notas novas** → atualiza CSV e resumo, registra "Atualização: X → Y"

**Recomendação:** após a extração mensal, rodar o mesmo comando 2-3 dias depois para capturar notas com delay.

## Dashboard NFS-e

**URL:** https://dashboard-topaz-ten-65.vercel.app
**Diretório:** `dashboard/`
**Deploy:** `cd dashboard && VERCEL_SCOPE=daniels-projects-548066da npx --yes vercel@latest deploy . --yes --prod`
**Env vars (Vercel):** `TRINKS_API_KEY`

### Funções do dashboard

1. **Total NFS-e emitidas no mês** (KPI principal)
   - Fonte: Trinks API (`/transacoes`), filtrado por cartão + PIX
   - Precisão: ~97,6% vs prefeitura (validado fev/2026)
   - Atualização: tempo real (cache 5 min no Vercel)
   - Métricas: total, média diária, melhor dia, breakdown por forma de pagamento, tabela diária

2. **Extração mensal cota parte MEI** (planilha pro contador) — *a implementar no dashboard*
   - Hoje: `python3 scripts/extrair_notas.py --periodo YYYY-MM`
   - Gera CSV com notas que têm rateio entre salão e profissional parceiro
   - Futuro: integrar no dashboard para download direto

### Lógica de emissão de NFS-e

O objetivo é emitir no mínimo o valor rastreável pela Receita (maquininha + PIX).

Quando a recepcionista pergunta "quanto de notas já foram emitidas este mês", quer saber o **total de NFS-e emitidas pelo Trinks**. O dashboard responde isso em tempo real.

### Fontes de dados e precisão

| Fonte | O que retorna                 | Precisão | Latência |
|-------|-------------------------------|----------|----------|
| **Trinks API** (dashboard) | Todas as transacoes          | ~97,6% | Tempo real |
| **ADN/prefeitura** (script) | NFS-e autorizadas (cstat=100) | 100% | Delay 1-3 dias |

A diferença de ~2,4% entre Trinks e ADN se deve a: notas emitidas em lote retroativo (competem pelo mesmo match), descontos no Trinks que alteram o valor vs NFS-e, e valores muito comuns (ex: R$ 35 pedicure) que geram ambiguidade.

### Conciliação Trinks vs Prefeitura

Match por **data + valor** (tolerância ±5 dias, ±R$ 0,02). Não é possível comparar por número de nota (Trinks não expõe). O endpoint `/transacoes/notas-fiscais` existe na documentação Trinks mas retorna 404 — confirmado via Swagger e testes diretos.

**Resultado fev/2026:** 536/549 notas com rateio bateram (97,6%). 482 mesmo dia, 54 com shift. 13 sem match (lote retroativo ou divergência de desconto).

Scripts: `scripts/conciliar_fev.py` | Resultado: `output/conciliacao_202602.json`

## Método legado: Extração de PDF

Consultar `REGRAS_EXTRACAO_NOTAS.md` para as regras de extração via PDF (usado antes da integração com a API). Requer `poppler` (`brew install poppler`).

## Regras gerais

- O CNPJ da Depilagos é `09223558000100`.
- CNPJs de parceiros devem ser formatados como `XX.XXX.XXX/XXXX-XX` no CSV.
- Datas no CSV em formato DD/MM/AAAA.
- Notas com múltiplos parceiros geram uma linha CSV por parceiro.
- Notas com múltiplos serviços do mesmo parceiro têm cotas somadas em uma única linha.
