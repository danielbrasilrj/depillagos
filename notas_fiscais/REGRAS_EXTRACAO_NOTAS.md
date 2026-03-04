# Regras de Extração de Notas Fiscais - Depilagos

## Regra: Identificação de Cota Parte de Profissional Parceiro

### Quando TEM rateio (cota parte):

**Via API (XML):** A tag `<xDescServ>` contém `PROFISSIONAL-PARCEIRO`:

```
SERVIÇO      R$ valor
SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$[COTA_SALAO]
PROFISSIONAL-PARCEIRO: [CNPJ_PARCEIRO] COTA-PARTE R$[COTA_PARCEIRO]
```

**Via PDF:** A descrição contém a palavra `"Rateio"`:

```
Rateio referente a Salao/Profissional parceiro:
- CNPJ: 09223558000100 CENTRO DE ESTETICA DEPILAGOS LTDA - R$ [COTA_SALAO]
- CNPJ: [CNPJ_PARCEIRO] [NOME_PARCEIRO] - R$ [COTA_PARCEIRO]
```

### Quando NÃO tem rateio:

- **API:** `xDescServ` contém apenas `SALAO-PARCEIRO` (100% para o salão).
- **PDF:** A descrição não contém `"Rateio"` e `Valor Dedução/Descontos` = 0.

## Padrão por Tipo de Serviço

### Serviços que GERALMENTE TÊM rateio (profissional parceiro):
- MANICURE / MANICURE EXPRESS
- PEDICURE / PEDICURE FRANCESINHA / SPA DO PÉ
- PÉ E MÃO
- BANHO DE GEL / ACRIGEL / UNHA ENCAPSULADA
- DESIGN COM HENNA
- ESCOVA (quando feita por parceiro)

### Serviços que GERALMENTE NÃO TÊM rateio (equipe Depilagos):
- Depilação: VIRILHA TOTAL, VIRILHA TOTAL COM ANUS, PERNA INTEIRA, MEIA PERNA, AXILA, BUCO, QUEIXO, FAIXA
- Todos os serviços marcados com sufixo **DF** (Depilação Feminina)

**Conclusão:** O rateio NÃO depende apenas do tipo de serviço, mas sim de **quem executou**. A presença de `PROFISSIONAL-PARCEIRO` (API) ou `"Rateio"` (PDF) é o indicador definitivo.

## Estrutura do Rateio

### Divisão de valores:
- O CNPJ `09223558000100` é sempre a **Depilagos** (cota do salão).
- Qualquer outro CNPJ é o **profissional parceiro**.
- Geralmente a divisão é **50/50**, mas existem exceções (ex: Banho de Gel = 40% salão / 60% parceiro).

### Notas com múltiplos parceiros:
- Uma mesma NFS-e pode ter **múltiplos serviços** com **parceiros diferentes**.
- Nesse caso, gera **uma linha no CSV por parceiro**.

### Notas com múltiplos serviços e mesmo parceiro:
- Uma NFS-e pode ter vários serviços, todos rateados com o mesmo parceiro.
- Nesse caso, as cotas são somadas em **uma única linha no CSV**.

## Profissionais Parceiros Conhecidos

| CNPJ | Nome |
|------|------|
| 22.042.775/0001-62 | (identificar) |
| 22.408.001/0001-02 | (identificar) |
| 30.446.566/0001-02 | (identificar) |
| 30.599.290/0001-00 | ISABELLA SANTOS DE LIMA |
| 31.447.884/0001-50 | JOSIANE MARINHO DA CRUZ |
| 33.252.419/0001-90 | CAMILA CARVALHO DOS SANTOS (MEI) |
| 43.800.664/0001-48 | (identificar) |
| 48.215.165/0001-07 | JHENNIFER ROZA DA SILVA |
| 51.509.111/0001-69 | WASHILLA LEMOS DA SILVA |
| 52.486.563/0001-35 | (identificar) |
| 56.877.185/0001-71 | ITACIANA FEITOSA PINTO |

## Formato de Saída (CSV)

- **Delimitador:** `;` (ponto-e-vírgula) — necessário porque valores usam vírgula decimal.
- **Formato de valores:** vírgula como separador decimal (ex: `17,50`).
- **Datas:** formato DD/MM/AAAA.
- **Colunas:**

```
data servico;data emissao;NUMERO DA NOTA;CNPJ PROFISSIONAL PARCEIRO;COTA PARTE SALÃO PARCEIRO;COTA PARTE PROFISSIONAL-PARCEIRO
```

## Notas SEM Cota Parte (excluídas do CSV)

O CSV gerado contém **apenas** notas com rateio (cota parte de profissional parceiro). As notas abaixo são corretamente excluídas pelo script.

### Tipo 1: Notas com apenas SALAO-PARCEIRO (sem PROFISSIONAL-PARCEIRO)

São notas onde o serviço foi executado por um profissional parceiro, mas 100% do valor ficou com o salão (sem divisão). Na descrição XML aparece apenas `SALAO-PARCEIRO` sem `PROFISSIONAL-PARCEIRO`.

Serviços mais comuns nessa categoria:
- MANICURE (50x em fev/2026)
- PÉ E MÃO (44x)
- PEDICURE FRANCESINHA (21x)
- PEDICURE (19x)
- MANICURE EXPRESS (7x)
- ESCOVA (5x)
- DESIGN COM HENNA (4x)

### Tipo 2: Notas sem nenhum texto de rateio (equipe interna Depilagos)

São notas de serviços executados pela equipe própria da Depilagos (não por parceiros MEI). A descrição XML não contém nem `SALAO-PARCEIRO` nem `Rateio referente`.

Serviços nessa categoria (todos com sufixo **DF** = Depilação Feminina):
- VIRILHA TOTAL COM ANUS DF (94x em fev/2026)
- AXILA DF (39x)
- BUCO DF (35x)
- MEIA PERNA DF (27x)
- VIRILHA TOTAL DF (25x)
- PERNA INTEIRA DF (19x)
- QUEIXO DF (12x)
- FAIXA DF (6x)
- Outros serviços de depilação

### Regra do script

O script `extrair_notas.py` já exclui corretamente essas notas:
- **Formato 1 (série 49999):** Só inclui se encontrar `PROFISSIONAL-PARCEIRO` no regex.
- **Formato 2 (série 1):** Só inclui se encontrar `Rateio referente` E um CNPJ diferente de `09223558000100` (Depilagos).

**Importante:** O mesmo tipo de serviço (ex: MANICURE) pode aparecer COM ou SEM rateio, dependendo de quem executou. A presença de `PROFISSIONAL-PARCEIRO` ou `Rateio referente` com CNPJ de parceiro é o único indicador definitivo.

## Extração via API (método principal)

### Regex para extrair cotas do XML:
```
(SALAO-PARCEIRO|PROFISSIONAL-PARCEIRO):\s*(\d{11,14})\s+COTA-PARTE\s+R\$([\d.]+(?:,\d+)?)
```

### Campos do XML:
| Campo XML | Dado |
|-----------|------|
| `<nNFSe>` | Número da NFS-e |
| `<dCompet>` | Data do serviço (YYYY-MM-DD) |
| `<dhProc>` | Data de emissão (YYYY-MM-DDThh:mm:ss) |
| `<vServ>` | Valor total do serviço |
| `<xDescServ>` | Descrição com dados do rateio |
| Namespace | `http://www.sped.fazenda.gov.br/nfse` |

### Passos:
1. Autenticar com certificado A1 (.pfx) via mTLS
2. Consultar `GET /DFe/{NSU}?cnpjConsulta=09223558000100&lote=true` começando do NSU 1
3. Decodificar XML de cada documento (GZip + Base64)
4. Extrair cotas com regex acima
5. Separar `SALAO-PARCEIRO` (cota salão) de `PROFISSIONAL-PARCEIRO` (cota parceiro)
6. Agrupar por parceiro, gerar uma linha CSV por parceiro
7. Incrementar NSU e repetir até `NENHUM_DOCUMENTO_LOCALIZADO`

## Extração via PDF (método legado)

### Regex para extrair cotas do PDF:
```
CNPJ:\s*(\d{11,14})\b.{1,150}?R\$\s*([\d]+[.,][\d]+)
```

### Passos:
1. Converter PDF com `pdftotext arquivo.pdf /tmp/output.txt`
2. Separar notas por `"Nota Fiscal de Serviço Eletrônica"`
3. Para cada nota, verificar presença de `"Rateio"` no texto
4. Se tem rateio, extrair pares CNPJ/valor com regex acima
5. Separar CNPJ Depilagos dos parceiros
6. Somar cotas por parceiro, gerar uma linha CSV por parceiro
