# Recepção Automática — Agente de IA WhatsApp Depillagos

Automação do atendimento via WhatsApp (22) 99235-4970 com agente de IA 24h, implementado por empresa terceirizada.

## Comandos WhatsApp

Comandos enviados ao número do WhatsApp. A ação é relativa ao contato de quem envia.

| Comando | Ação | Uso |
|---------|------|-----|
| `[limpa]` | Limpa a memória/histórico do agente para aquele contato | Teste: simular conversa como cliente novo, sem contexto de interações anteriores |
| `[libera]` | Desbloqueia o agente com IA para voltar a atender aquele contato | Teste: reativar a IA após ela ter sido pausada por intervenção humana |
| `[atualiza]` | Atualiza a base de conhecimento puxando dados (serviços, produtos...) do Trinks | Produção: forçar refresh após alterar algo no Trinks ou no documento de base |

`[limpa]` e `[libera]` são essencialmente para testes. `[atualiza]` é o único com uso prático no dia a dia.

## O que o Agente Sabe

### Informações Gerais
- **Nome:** Depillagos — Centro de Estética
- **CNPJ:** 09.223.558/0001-00
- **Endereço:** Rua Francisco A. da Silva, 120, Centro, Araruama, RJ — CEP 28970-000
- **WhatsApp:** (22) 99235-4970
- **Site:** depillagos.com.br
- **Instagram:** @_depillagos | **Facebook:** @depillagosararuama

### Horários
- **Depilação, Manicure, Estética, Sobrancelha:** Seg-Sex 9h-19h, Sáb 9h-17h, Dom fechado
- **Cabelo:** Ter-Sex 9h-19h, Sáb 9h-17h, Seg e Dom fechado

### Modelo de Atendimento
- **Walk-in** (sem hora marcada) para: depilação a cera, manicure, pedicure, cabelo, sobrancelha
- **Com agendamento** (via WhatsApp) para: avaliação laser, fibra de vidro, banho de gel, acrigel, estética (facial e corporal)

### Cancelamento
- 24h de antecedência para serviços agendados
- IA envia lembrete automático antes do horário
- No-show pode exigir pagamento antecipado para próximo agendamento

### Pagamentos
Dinheiro, PIX, crédito (Visa, Master, Elo, Amex, Diners, Banescard), débito (Visa Electron, Maestro, Elo), Vale-Presente. Sem depósito/transferência.

### Promoções Ativas
- Combo 3 áreas depilação: R$129,90 (2ª-4ª, dinheiro/PIX) / R$139,90 (5ª-Sáb)
- Avaliação laser: gratuita
- Mês da Mulher (mar/2026): Escova R$49,90 — depillagos.com.br/2026_mar_mes_mulher

### Catálogo
153 serviços em 10 categorias com preços reais do Trinks. Principais:

**Depilação a Cera Feminina:** Virilha total c/ ânus R$82 | Perna inteira R$81 | Virilha cavada c/ ânus R$79 | Virilha total R$68 | Virilha cavada R$64,50 | Braço R$50 | Meia perna R$45 | Axilas R$30 | Buço/Queixo R$20

**Depilação a Cera Masculina:** Virilha total c/ ânus R$92 | Tórax+abdômen R$89 | Perna inteira R$89 | Barba R$64 | Braço R$60

**Laser 4D (alemão, todos os fototipos):** Corpo todo R$299 | Perna completa R$289 | Áreas médias R$149,90 | Áreas pequenas R$79,90 | Áreas mínimas R$59,90 | Avaliação GRÁTIS

**Cabelo:** Maquiagem R$199 | Trat. Wella R$189,90 | Cauterização R$159,90 | Coloração R$155 | Penteado R$130 | Corte estilizado R$105 | Corte R$79 | Escova R$63

**Manicure/Pedicure:** Fibra de vidro R$179 | Acrigel R$162 | Banho de gel R$99 | Pé e mão R$65 | Pedicure R$35 | Manicure R$30

**Design Sobrancelha:** Design c/ henna R$73 | Design R$56 | Henna R$34

**Estética Facial:** Cílios R$169 | Limpeza de pele R$129 | Peeling cristal R$89

**Estética Corporal:** Massagem turbinada R$119 | Drenagem/Massagem relaxante R$99

**Outros:** Micropigmentação R$450 | Experiência Única R$89

### FAQ — Respostas-Chave

- **Preciso agendar?** Maioria não, é só chegar. Agendamento para: laser, fibra, gel, acrigel, estética.
- **Laser em pele bronzeada?** Sim, 4D atende todos os fototipos.
- **Quantas sessões laser?** 10 sessões padrão (só mencionar que pode variar se a cliente insistir).
- **Laser dói?** Resfriamento integrado, muito mais confortável que cera.
- **Laser na gravidez?** Não. Retomar após amamentação.
- **Depilação a cera — frequência?** A cada 25-30 dias.
- **Programa de fidelidade?** "Vem novidade por aí! Será exclusivo para clientes. Fique de olho nas nossas redes!" (sem dar detalhes)

### Diferenciais
1. Especialista e pioneira em depilação a cera em Araruama (desde 2008)
2. Laser 4D alemão — único na Região dos Lagos, todos os fototipos
3. Sem hora marcada — walk-in acolhedor
4. 18 anos de experiência, 26K+ clientes
5. 153 serviços, 25 profissionais
6. Preços acessíveis e transparentes — qualquer pessoa se sente à vontade
7. Produtos premium: L'Oréal, Wella, Truss, Alfaparf, Aneethun

### Equipe (25 profissionais)
**CLT (8):** Ana Carolina, Daiane, Patricia, Yasmin M. (depiladoras) | Caroline (esteticista/laser) | Simone, Yasmin (recepção) | Renata (limpeza)

**MEI (16):** 13 manicures (Jhennifer, Dalleti, Itaciana, Camila, Jari, Washilla, Monica, Isabella, Josiane, Thays, Tauanny, Jessica, Sabrina/Amanda/Eychila) + 3 cabeleireiras (Priscila, Jacqueline, Noemi)

## Arquivos de Referência

- **Questionário completo (HTML):** `docs/questionario_ia_whatsapp.html`
- **Questionário completo (PDF):** `docs/questionario_ia_whatsapp_depillagos.pdf`
- **Google Doc:** https://docs.google.com/document/d/1WxgI5zgrW5mdNpYQhVlv6puWkauRHEju4hVeV11v-PY/edit

## Como Atualizar a Base de Conhecimento

1. **Via comando:** Enviar `[atualiza]` no WhatsApp para puxar dados atualizados do Trinks
2. **Via documento:** Editar `docs/questionario_ia_whatsapp.html`, regenerar PDF e enviar à empresa de IA
3. **Promoções/horários especiais:** Enviar informações atualizadas ao suporte da empresa de IA

## Comportamento da Automação

- Quando a equipe envia mensagem manual para a cliente, a IA pausa e o controle fica com o humano
- A memória do agente **não limpa automaticamente** — persiste entre conversas até enviar `[limpa]`

**Devolver controle para a IA após intervenção humana:**
1. **Esperar** — após 24h sem interação humana, a IA retoma automaticamente
2. **Forçar** — enviar `[libera]` no chat e **apagar a mensagem** em seguida (para a cliente não ver o comando)