# Câmeras de Monitoramento — Depillagos Araruama

## Apresentação

https://camerasmonitoramento.vercel.app

## Objetivo

Sistema de monitoramento inteligente para o salão com contagem de clientes/funcionários em tempo real, gravação em cloud, e dashboard remoto.

## MVP — Funcionalidades

| Feature | Status |
|---|---|
| Contagem entrada/saída (tempo real) | MVP |
| Identificação automática de funcionários (face rec, ~25 rostos) | MVP |
| Clientes = total dentro - funcionários (automático) | MVP |
| Gravação local com buffer no SSD | MVP |
| Armazenamento de rostos (pra uso futuro) | MVP |
| Dashboard remoto (web) | MVP |
| Áudio (câmeras com mic) | MVP |
| Reconhecimento facial de clientes | Post-MVP |
| Integração com Trinks | Post-MVP |
| Alertas WhatsApp | Post-MVP |
| Mapa de calor | Post-MVP |
| Clube Depillagos (check-in por facial) | Post-MVP |

## Arquitetura

```
Câmera interna ── Ethernet (PoE) ──┐
                                    ├── Switch PoE ── Ethernet ── Mini PC ── USB ── SSD
Câmera externa ── Ethernet (PoE) ──┘                                │
                                                                    │ internet
                                                                    ▼
                                                          Oracle Cloud (SP)
                                                            ├── PostgreSQL
                                                            ├── Dashboard (Next.js)
                                                            └── API
```

### Processamento local (Mini PC no salão)

- **Contagem de pessoas:** YOLOv8 + line crossing detection
- **Reconhecimento facial:** identificação automática de funcionários (~25 rostos cadastrados)
- **Buffer de vídeo:** SSD externo USB armazena gravações temporárias. Dados essenciais (contagens, rostos, histórico) sincronizados com a cloud
- **Relay mínimo:** se internet cai, o SSD guarda o vídeo; quando volta, sincroniza

**Por que local e não cloud:** processamento de vídeo 24/7 na cloud (AWS EC2/GPU) custaria R$1.100–2.500/mês. Localmente custa ~R$75/mês após investimento inicial de ~R$2.700. Break-even em menos de 3 meses.

### Cloud — Oracle Cloud Free Tier (Data Center São Paulo)

Servidor definitivo do projeto. Free tier permanente (não expira após 12 meses).

- **Instância:** VM.Standard.A1.Flex — 4 vCPU ARM (Ampere), 24GB RAM, 200GB storage
- **Sistema:** Ubuntu 22.04 ARM
- **Dashboard web:** Next.js acessível de qualquer lugar
- **Banco de dados:** PostgreSQL rodando na mesma instância
- **API:** FastAPI recebendo dados do mini PC no salão
- **Custo:** R$0/mês (free tier permanente)
- **Localização:** Data center em São Paulo (sa-saopaulo-1) — baixa latência, dados no Brasil (LGPD)
- **Rede:** 480 Mbps de bandwidth incluído no free tier, IP público gratuito

## Decisão: PoE em vez de Wi-Fi

**Escolhemos PoE (Power over Ethernet) em vez de Wi-Fi para as câmeras.**

Motivo principal: câmeras Wi-Fi ainda precisam de um cabo elétrico para energia (ou bateria que acaba). Ou seja, Wi-Fi só elimina o cabo de rede, mas adiciona outro problema — instabilidade de conexão.

Com PoE, **um único cabo Ethernet resolve rede + energia**:
- Sem necessidade de tomada próxima à câmera
- Conexão estável 24/7 (sem interferência, queda ou latência de Wi-Fi)
- Instalação mais limpa (um cabo por câmera)
- Mais confiável para stream contínuo de vídeo

## Setup Físico

### Câmeras

- **Câmera interna:** apontada para a porta de entrada (de dentro pra fora), com microfone embutido
- **Câmera externa:** apontada para a porta de entrada (de fora pra dentro), IP67 (resistente a chuva)
- Ambas 1080p, H.265, com suporte a RTSP

### Rede no salão

```
Câmera interna ── cabo Ethernet Cat6 ──┐
                                        ├── Switch PoE (4 portas) ── Ethernet ── Mini PC
Câmera externa ── cabo Ethernet Cat6 ──┘                                            │
       (cabo outdoor se exposto)                                                USB ── SSD 1TB
```

Tudo cabe dentro de um armário/rack pequeno trancado.

### Internet

Plano empresarial com pelo menos **15-20 Mbps de upload**. O consumo estimado é ~6-9 Mbps (sync de dados + acesso remoto), mas margem é importante.

## Stack Técnica

| Componente | Tecnologia |
|---|---|
| Câmeras | 2x IP PoE, 1080p, H.265, RTSP, mic embutido, IP67 (externa) |
| Switch PoE | TP-Link ou similar, 4 portas |
| Mini PC | Intel N100, 16GB RAM, 512GB SSD interno |
| SSD externo | 1TB USB 3.0 (buffer de vídeo) |
| Acelerador IA | Google Coral USB TPU (obrigatório — offload de inferência IA) |
| Contagem de pessoas | YOLOv8 + line crossing |
| Face recognition | InsightFace (funcionários) |
| Backend | Python (FastAPI) |
| Banco de dados | PostgreSQL (Oracle Cloud) |
| Dashboard | React (Next.js) |
| Cloud | Oracle Cloud Free Tier (São Paulo) |

## Custos

### Investimento inicial (one-time)

| Item | Preço estimado |
|---|---|
| 2x Câmeras IP PoE com mic | ~R$1.200–2.000 |
| Switch PoE 4 portas | ~R$250 |
| Mini PC Intel N100 16GB | ~R$1.800 |
| SSD externo 1TB | ~R$400 |
| Google Coral USB TPU | ~R$500 |
| Cabos Ethernet Cat6 + instalação | ~R$200–400 |
| **Total** | **~R$4.350–5.350** |

### Custo mensal

| Item | Custo |
|---|---|
| Oracle Cloud Free Tier | R$0 |
| Eletricidade (mini PC + switch) | ~R$15–30 |
| Internet (já existente no salão) | R$0 adicional* |
| **Total** | **~R$15–30/mês** |

*Se precisar upgrade de internet pra garantir upload, custo adicional varia por provedor.

## Decisão: SSD externo em vez de SSD interno maior

**Escolhemos Mini PC 512GB + SSD externo 1TB em vez de um SSD interno único de 2TB.**

Duas câmeras 1080p H.265 24/7 geram ~20-25 GB/dia (~700 GB/mês). O SSD interno de 512GB não comporta vídeo + sistema operacional.

A vantagem do SSD externo não é performance (USB 3.0 é rápido o suficiente), é **isolamento**:
- Se o disco de vídeo enche → sistema operacional continua rodando normal, só para de gravar
- Se o SSD externo falha → mini PC continua funcionando, troca o SSD e volta
- Se o disco do sistema falha → vídeo no SSD externo sobrevive

Com SSD interno único, qualquer problema (disco cheio, falha) derruba tudo junto.
