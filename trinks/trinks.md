
# Trinks API Integration

## Documentation
https://trinks.readme.io/reference/introducao

## Authentication
- **API Key Header:** `X-Api-Key: <token>`
- Token is stored in `.env` as `TRINKS_API_KEY`

## Base URL
```
https://api.trinks.com/v1
```

## Required Headers
All endpoints (except `/estabelecimentos`) require:
- `X-Api-Key` — API authentication token
- `estabelecimentoId` — Establishment ID (see below)

## Establishment
- **Nome:** Depillagos
- **ID:** 243726
- **CNPJ:** 09223558000100

## Known Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/estabelecimentos` | List establishments (only needs X-Api-Key) |
| GET | `/v1/clientes` | List clients (paginated) |
| GET | `/v1/clientes/{clienteId}` | Get client details |
| PUT | `/v1/clientes/{clienteId}` | Update client (see restrictions below) |
| POST | `/v1/clientes/{clienteId}/telefones` | Add phone to client |
| DELETE | `/v1/clientes/{clienteId}/telefones/{telefoneId}` | Remove phone from client |
| POST | `/v1/clientes/{clienteId}/creditos` | Add credit to client |
| POST | `/v1/clientes/{clienteId}/etiquetas/{etiquetaId}` | Assign tag to client |
| DELETE | `/v1/clientes/{clienteId}/etiquetas/{etiquetaId}` | Remove tag from client |
| POST | `/v1/clientes/{clienteId}/valespresentes` | Create gift voucher |
| GET | `/v1/servicos` | List all services (paginated, 50 per page) |
| GET | `/v1/servicos/{id}/promocoes` | List promotions for a service |

## Pagination
Responses include: `page`, `pageSize`, `totalPages`, `totalRecords`

## PUT /v1/clientes/{clienteId} — Field Restrictions

A Trinks diferencia **cliente web** (se cadastrou pela plataforma) de **cliente manual** (cadastrado pelo estabelecimento). Isso afeta quais campos podem ser alterados via API.

| Campo | Cliente Web | Cliente Manual |
|-------|:-----------:|:--------------:|
| `nome` | Bloqueado | Aceita |
| `email` | Bloqueado | Aceita |
| `cpf` | Bloqueado | Aceita (sem máscara, ex: `52998224725`) |
| `sexo` | Bloqueado | Aceita |
| `dataNascimento` | Aceita | Aceita |
| `observacoes` | Aceita | Aceita |
| `endereco` | Aceita | Aceita |
| `bairro` | Aceita | Aceita |
| `cidade` | Aceita | Aceita |
| `estado` | Aceita | Aceita |
| `cep` | Aceita | Aceita |

> **Nota:** CPF deve ser enviado sem pontuação (somente dígitos). Campos bloqueados retornam erro `"Não é possível alterar o {campo} de um cliente web."`
