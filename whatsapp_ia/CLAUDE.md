# WhatsApp IA — Agente Automatizado Depillagos

Projeto de automação do WhatsApp da Depillagos com agente de IA para atendimento 24h.

## Contexto

Empresa terceirizada está implementando um agente de IA no WhatsApp (22) 99235-4970 para responder clientes automaticamente: dúvidas, preços, horários, agendamentos e promoções.

## Arquivo Principal

- **`questionario_ia_whatsapp.html`** — Fonte editável com todas as informações do negócio
- **`questionario_ia_whatsapp_depillagos.pdf`** — PDF gerado para enviar à empresa de IA

## Dados Fornecidos ao Agente

### 1. Informações Gerais
- Nome, CNPJ, endereço, contato, redes sociais
- Horários: Seg-Sex 9h-19h, Sáb 9h-17h (cabelo fecha segunda)

### 2. Política de Agendamento
- **Walk-in** para maioria dos serviços (é só chegar)
- **Com agendamento** (via WhatsApp): avaliação laser, fibra de vidro, banho de gel, acrigel, estética (facial e corporal)

### 3. Cancelamento
- 24h de antecedência para serviços agendados
- IA envia lembrete automático antes do horário
- No-show pode exigir pagamento antecipado no próximo agendamento

### 4. Pagamentos
- Dinheiro, PIX, crédito (Visa, Master, Elo, Amex, Diners, Banescard), débito (Visa Electron, Maestro, Elo), Vale-Presente

### 5. Catálogo Completo
- 153 serviços em 10 categorias com preços reais do Trinks
- Depilação cera (fem/masc), laser 4D, linha, cabelo, manicure/pedicure, sobrancelha, estética facial/corporal, micropigmentação

### 6. Promoções Ativas
- Combo 3 áreas depilação: R$129,90 (2ª-4ª, dinheiro/PIX) / R$139,90 (5ª-Sáb)
- Avaliação laser: gratuita
- Mês da Mulher (mar/2026): Escova R$49,90

### 7. FAQ
- Perguntas gerais, laser (10 sessões padrão), cera, cabelo, manicure/pedicure

### 8. Diferenciais
- Pioneira em depilação a cera em Araruama (desde 2008)
- Laser 4D alemão — único na Região dos Lagos, todos os fototipos
- 26K+ clientes, 25 profissionais, 153 serviços

### 9. Instruções Especiais para a IA
- **Programa de fidelidade:** Se perguntarem, responder "Vem novidade por aí! Será exclusivo para clientes. Fique de olho nas nossas redes!" — sem dar detalhes
- **Sessões laser:** Responder 10 sessões. Só mencionar que pode variar se a cliente insistir
- **Atualização de promoções/horários:** Enviar informações atualizadas ao suporte da IA

## Como Atualizar

1. Editar `questionario_ia_whatsapp.html`
2. Regenerar PDF (abrir HTML no browser → Print → Save as PDF, ou via Playwright)
3. Enviar PDF atualizado à empresa de IA
