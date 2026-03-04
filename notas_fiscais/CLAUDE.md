# Projeto Depilagos - Extração de Notas Fiscais

## Contexto

Este projeto processa Notas Fiscais de Serviço Eletrônicas (NFS-e) emitidas pelo **CENTRO DE ESTETICA DEPILAGOS LTDA** (CNPJ: 09.223.558/0001-00), localizado em Araruama/RJ. O objetivo é extrair dados de notas que possuem **cota parte de profissional parceiro** (rateio) e gerar um CSV estruturado.

## O que é o rateio

A Depilagos trabalha com profissionais parceiros (MEIs com CNPJ próprio) que prestam serviços no espaço do salão. Quando um serviço é feito por um parceiro, o valor é dividido entre o salão e o profissional. Essa divisão é chamada de **rateio** e aparece descrita no corpo da NFS-e.

## Estrutura do projeto

```
├── scripts/
│   └── extrair_notas.py      # Script principal de extração e verificação
├── tests/
│   ├── conftest.py           # Configura sys.path para imports
│   ├── test_extrair_notas.py # Testes unitários (extração)
│   └── test_resumo_notas.py  # Testes unitários (resumo, comparação, histórico)
├── certificado/              # Certificado digital A1 (.pfx) - NÃO commitado
├── docs/                     # PDFs de referência e documentos auxiliares
│   ├── Notas (1).pdf
│   ├── Notas (2).pdf
│   └── Notas com deduções ABRIL 2024.xlsx
├── output/                   # CSVs gerados pelo script
├── REGRAS_EXTRACAO_NOTAS.md  # Regras de extração e padrões
└── CLAUDE.md                 # Contexto técnico do projeto
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

## Método legado: Extração de PDF

Consultar `REGRAS_EXTRACAO_NOTAS.md` para as regras de extração via PDF (usado antes da integração com a API). Requer `poppler` (`brew install poppler`).

## Regras gerais

- O CNPJ da Depilagos é `09223558000100`.
- CNPJs de parceiros devem ser formatados como `XX.XXX.XXX/XXXX-XX` no CSV.
- Datas no CSV em formato DD/MM/AAAA.
- Notas com múltiplos parceiros geram uma linha CSV por parceiro.
- Notas com múltiplos serviços do mesmo parceiro têm cotas somadas em uma única linha.
