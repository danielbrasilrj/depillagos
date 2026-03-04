# Depilagos - Extração de Notas Fiscais

Extrai dados de NFS-e com **cota parte de profissional parceiro** (rateio) emitidas pelo Centro de Estética Depilagos e gera CSV para envio ao contador.

## Pré-requisitos

- Python 3
- OpenSSL
- curl
- Certificado digital A1 (.pfx) em `certificado/`

## Setup após checkout

1. Colocar o certificado digital A1 (.pfx) em `certificado/`
2. Criar o arquivo `.env` na raiz do projeto:

```bash
echo "DEPILAGOS_PFX_PASSWORD=SUA_SENHA_AQUI" > .env
```

O `.env` está no `.gitignore` — nunca será commitado.

## Estrutura

```
├── scripts/
│   ├── extrair_notas.py      # Script principal de extração
│   ├── verificar_notas.py    # Verifica completude do CSV (delay da API)
│   └── test_extrair_notas.py # Testes unitários
├── certificado/              # Certificado digital A1 (.pfx) - NÃO commitado
├── docs/                     # PDFs de referência e documentos auxiliares
├── output/                   # CSVs gerados pelo script
├── REGRAS_EXTRACAO_NOTAS.md  # Regras de extração e padrões
└── CLAUDE.md                 # Contexto técnico do projeto
```

## Uso

```bash
# Carregar senha do .env
export $(cat .env | xargs)

# Extrair todas as notas com rateio
python3 scripts/extrair_notas.py

# Filtrar por mês
python3 scripts/extrair_notas.py --periodo 2026-02

# Salvar em arquivo específico
python3 scripts/extrair_notas.py --output output/fev2026.csv

# Verificar se há notas novas (delay da API)
python3 scripts/verificar_notas.py --periodo 2026-02

# Usar PDFs específicos como complemento
python3 scripts/extrair_notas.py --pdf docs/Notas\ \(1\).pdf
```

## Saída

CSV com delimitador `;` e formato brasileiro (vírgula decimal, datas DD/MM/AAAA):

```
data servico;data emissao;NUMERO DA NOTA;CNPJ PROFISSIONAL PARCEIRO;COTA PARTE SALÃO PARCEIRO;COTA PARTE PROFISSIONAL-PARCEIRO
```

## Como funciona

1. Autentica na API NFS-e Nacional (ADN) via mTLS com certificado A1
2. Baixa todas as NFS-e em lotes de 50 (por NSU)
3. Decodifica XML (GZip + Base64) e identifica notas com rateio
4. Complementa com PDFs locais (para notas ainda não distribuídas no ADN)
5. Gera CSV com uma linha por parceiro por nota
