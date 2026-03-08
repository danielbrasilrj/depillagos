# Depillagos Site

Novo site institucional depillagos.com.br — estático, rápido, com preços reais do Trinks.
Substitui o WordPress atual (lento, desatualizado, sem preços, Bacaxá ainda listada, links 404).

## Skills

Before plans/code: ALWAYS read `BACKLOG.md` + `PRD.md`.
Design reference → `../depillagos_hair/public/index.html` (usar como base de estilo).
Service data → Trinks MCP (`list_services`, `list_professionals`).
Brand colors → `../depillagos_app_v2/apps/mobile/src/theme/tokens.ts`.

## Interaction

- EXTREMELY concise. No polite filler.
- Execute without asking. Only confirm destructive ops.
- **Never commit or push** unless explicitly asked.
- Before every commit: update `BACKLOG.md` (status → done) + `PRD.md` (Delivered Tasks).

## Non-Negotiable Rules

- **100% estático.** HTML + CSS + JS inline. Zero framework, zero build, zero npm.
- **Mobile-first.** Público acessa majoritariamente por celular.
- **Preços reais.** Todos os 153 serviços com preços do Trinks. Nunca inventar preço.
- **pt-BR nativo.** Vírgula decimal, DD/MM/AAAA, linguagem natural brasileira.
- **Schema.org + Open Graph** em todas as páginas. Ver SEO Strategy no PRD.md para técnicas explícitas.
- **WhatsApp como CTA principal.** (22) 99235-4970 — `wa.me/5522992354970`.
- **Acessibilidade.** Contraste AA, alt em imagens, semântica HTML5.

## Scope Guards

- **Araruama only.** Bacaxá fechou. Sem seletor de unidade.
- **Walk-in first.** Laser = WhatsApp booking. Demais = sem hora marcada.
- **Sem backend.** Site 100% estático. Preços hardcoded (atualizados manualmente via Trinks MCP).
- **Sem formulário de contato.** WhatsApp é o canal. Sem SMTP, sem backend.
- **Blog migrado = estático.** Posts relevantes viram seções/FAQ, não CMS.
- **Banners sazonais.** Home tem carousel. Banner 1 = promo sazonal (atualmente: Mês das Mães, maio). Trocar conforme campanha.

## Architecture

```
site/
├── public/
│   ├── index.html              ← home
│   ├── servicos.html           ← catálogo completo com preços
│   ├── depilacao-a-laser.html  ← laser (diferencial principal)
│   ├── quem-somos.html         ← história + equipe
│   ├── contato.html            ← mapa + WhatsApp + horários
│   ├── favicon.png
│   ├── imagens/
│   │   ├── hero/               ← salão, ambiente
│   │   └── servicos/           ← por categoria (copiar do app)
│   └── logos/                  ← marcas parceiras
├── CLAUDE.md
├── PRD.md
└── BACKLOG.md
```

## Reference Data

**Contato:** Rua Francisco A. da Silva, 120, Araruama/RJ | WhatsApp (22) 99235-4970 | @_depillagos
**CNPJ:** 09.223.558/0001-00
**Google Maps:** Place ID `0x97693e540ec145:0x49b27925cdc5928f`
**Horários:** Seg–Sex 9h–19h, Sáb 9h–17h. Cabelo: Ter–Sex (não abre segunda).

**Cores:**
```css
--primary: #c81773;  --primary-light: #e065a8;  --primary-dark: #c2185b;
--bg: #fdf2f8;  --bg-dark: #fce7f3;
```

**Assets disponíveis (copiar, não linkar):**
- `depillagos_app_v2/apps/mobile/assets/categories/hero/` — 8 fotos de categorias
- `depillagos_app_v2/apps/mobile/assets/services/hero/` — 15 fotos de serviços
- `depillagos_app_v2/apps/mobile/assets/favicon.png` — ícone boneca rosa
- `depillagos_hair/public/imagens/` — fotos cabeleireiras, salão
- `depillagos_hair/public/logos/` — L'Oréal, Wella, Truss, Alfaparf, Aneethun

## Deploy

- **Produção:** Hostinger → `public_html/` (substitui WordPress)
- **Staging:** Vercel → `depillagos-site.vercel.app`
- Deploy: `cd site && npx --yes vercel@latest --yes --prod --scope daniels-projects-548066da`
- Hostinger: zip de `public/` → File Manager → `public_html/` → extrair com `.`
