# Depillagos Site — Product Backlog

---

## MVP Definition

**In scope:** Home page, catálogo de serviços com preços (153 do Trinks), página do laser, quem somos, contato, SEO completo, design rosa mobile-first, WhatsApp CTA.

**Out of scope:** CMS, formulário de contato, agendamento online, e-commerce, Bacaxá, blog CMS, multi-idioma, chat widget.

**Key constraints:**

- 100% estático. Zero framework, zero build, zero npm.
- Preços hardcoded do Trinks. Atualização manual.
- WhatsApp é o único canal de contato/agendamento.
- Deploy: Hostinger (produção) + Vercel (staging).

---

## Sprint 1: Foundation + Home

**Goal:** Estrutura do projeto, CSS compartilhado, home page completa. Visitante vê hero, categorias, destaque laser, números, depoimentos e localização.

### S1-01 Project Setup

- **Status:** todo
- **Priority:** P0
- **Size:** S
- **Dependencies:** none
- **Acceptance Criteria:**
  - [ ] Estrutura de diretórios criada (`public/`, `imagens/`, `logos/`)
  - [ ] `favicon.png` copiado do app
  - [ ] `.gitignore` criado
  - [ ] Assets de imagens copiados do app (categorias, serviços)
  - [ ] Logos das marcas copiados do depillagos_hair

### S1-02 CSS Design System

- **Status:** todo
- **Priority:** P0
- **Size:** M
- **Dependencies:** S1-01
- **Acceptance Criteria:**
  - [ ] CSS variables definidas (cores, tipografia, espaçamento)
  - [ ] Reset + base styles
  - [ ] Componentes reutilizáveis: `.card`, `.btn`, `.btn-whatsapp`, `.section`, `.grid`
  - [ ] Responsivo: breakpoints mobile (default), tablet (768px), desktop (1024px)
  - [ ] Header fixo com nav + logo + botão WhatsApp
  - [ ] Footer com links, redes sociais, CNPJ, copyright 2026
  - [ ] Baseado no estilo do `depillagos_hair/public/index.html`

### S1-03 Home Page — Banner Carousel + Categorias

- **Status:** todo
- **Priority:** P0
- **Size:** L
- **Dependencies:** S1-02
- **Acceptance Criteria:**
  - [ ] Banner carousel com 3 slides (autoplay 5s, dots, swipe no mobile)
  - [ ] **Banner 1: Mês das Mães (maio)** — Promoção cabelo. "Presenteie sua mãe com um dia de beleza". Escova + tratamento com preço especial. CTA WhatsApp "Quero agendar". Fundo rosa com flores (inspirado no `banner-promo-seasonal.webp` do app)
  - [ ] **Banner 2: Laser 4D** — "Primeiro laser 4D da Região dos Lagos". Imagem do equipamento (baseado no `banner-promo-laser.webp`). CTA "Avaliação gratuita" → WhatsApp
  - [ ] **Banner 3: Bem-vinda** — "Atendimento sem hora marcada desde 2008". Imagem da recepção (baseado no `banner-welcome.webp`). CTA "Ver serviços" → servicos.html
  - [ ] Grid de 7 categorias com ícones/fotos e link pra servicos.html#categoria
  - [ ] Categorias: Depilação a Laser, Depilação a Cera, Manicure e Pedicure, Cabelo, Design de Sobrancelha, Estética Facial, Estética Corporal
  - [ ] Scroll suave entre seções
  - [ ] Animações fade-in no scroll

### S1-04 Home Page — Laser + Números + Depoimentos

- **Status:** todo
- **Priority:** P0
- **Size:** M
- **Dependencies:** S1-03
- **Acceptance Criteria:**
  - [ ] Seção destaque laser 4D — primeiro da Região dos Lagos, todos os fototipos, CTA avaliação gratuita
  - [ ] Contador: 18+ anos, 26K+ clientes, 25 profissionais
  - [ ] 4–6 depoimentos reais do Google Maps com link pro perfil
  - [ ] Google Maps embed com place ID real
  - [ ] Endereço, horários, WhatsApp

### S1-05 Home Page — SEO On-Page

- **Status:** todo
- **Priority:** P0
- **Size:** M
- **Dependencies:** S1-03
- **Acceptance Criteria:**
  - [ ] `<title>` com keyword primária no início: "Centro de Estética Araruama — Depillagos | Depilação, Laser, Cabelo"
  - [ ] `<meta name="description">` 150-160 chars com CTA: "Centro de estética desde 2008. 153 serviços com preços. Laser 4D, depilação, manicure, cabelo. Sem hora marcada. (22) 99235-4970"
  - [ ] H1 único: "Centro de Estética Depillagos — Araruama"
  - [ ] Schema.org JSON-LD: LocalBusiness + BeautySalon (name, address, geo, telephone, openingHours, priceRange, image, sameAs)
  - [ ] Schema.org JSON-LD: Organization (foundingDate: 2008, founder: Luciene Freitas)
  - [ ] Open Graph: `og:title`, `og:description`, `og:image` (1200x630 do banner), `og:url`, `og:type=website`
  - [ ] Twitter Card: `summary_large_image`
  - [ ] Geo meta tags: `geo.region=BR-RJ`, `geo.placename=Araruama`, `geo.position=-22.8755;-42.3376`
  - [ ] `<link rel="canonical" href="https://depillagos.com.br/">`
  - [ ] Internal links: nav → todas as páginas, categorias → servicos.html#anchor, laser destaque → depilacao-a-laser.html
  - [ ] Todas as imagens com `alt` descritivo + keyword natural, `width`/`height` explícitos, `loading="lazy"` (exceto hero/LCP)
  - [ ] Hero image SEM lazy loading (é o LCP) — `fetchpriority="high"` + `<link rel="preload">`

---

## Sprint 2: Catálogo de Serviços

**Goal:** Página completa com todos os 153 serviços organizados por categoria com preços reais do Trinks.

### S2-01 Serviços — Layout + Navegação

- **Status:** todo
- **Priority:** P0
- **Size:** M
- **Dependencies:** S1-02
- **Acceptance Criteria:**
  - [ ] Nav lateral/superior com 10 categorias (âncoras)
  - [ ] Sticky category nav no mobile
  - [ ] Layout de tabela/cards por categoria
  - [ ] CTA WhatsApp contextual por serviço (mensagem pré-preenchida com nome do serviço)
  - [ ] Busca/filtro de serviços (JS, client-side)

### S2-02 Serviços — Depilação (Cera Feminina + Masculina + Linha)

- **Status:** todo
- **Priority:** P0
- **Size:** M
- **Dependencies:** S2-01
- **Acceptance Criteria:**
  - [ ] ~20 serviços cera feminina com preços
  - [ ] ~15 serviços cera masculina com preços
  - [ ] 3 serviços linha com preços
  - [ ] Promoção 3 áreas destacada (R$129,90 seg–qua / R$139,90 qui–sáb)
  - [ ] Descrição curta quando relevante
  - [ ] Foto hero da categoria

### S2-03 Serviços — Depilação Laser

- **Status:** todo
- **Priority:** P0
- **Size:** M
- **Dependencies:** S2-01
- **Acceptance Criteria:**
  - [ ] ~30 serviços laser com preços por área
  - [ ] Avaliação gratuita destacada
  - [ ] Link pra página dedicada do laser
  - [ ] CTA WhatsApp "Agendar avaliação gratuita"
  - [ ] Foto hero laser

### S2-04 Serviços — Cabelo, Unhas, Sobrancelha, Estética

- **Status:** todo
- **Priority:** P0
- **Size:** L
- **Dependencies:** S2-01
- **Acceptance Criteria:**
  - [ ] ~18 serviços cabelo com preços (sob consulta onde aplicável)
  - [ ] ~25 serviços manicure/pedicure com preços
  - [ ] 4 serviços design sobrancelha com preços
  - [ ] 4 serviços estética facial com preços
  - [ ] 5 serviços estética corporal com preços
  - [ ] Marcas mencionadas (Aneethun, L'Oréal, Wella, Truss, Alfaparf)
  - [ ] Nota: cabelo não abre segunda

### S2-05 Serviços — SEO On-Page

- **Status:** todo
- **Priority:** P0
- **Size:** M
- **Dependencies:** S2-04
- **Acceptance Criteria:**
  - [ ] `<title>`: "Serviços e Preços — Depillagos Araruama | 153 Serviços"
  - [ ] `<meta description>`: "Catálogo completo com preços. Depilação cera, laser, manicure, cabelo, estética. A partir de R$19. Sem hora marcada."
  - [ ] H1: "Serviços e Preços — Depillagos"
  - [ ] H2 por categoria (keyword natural): "Depilação a Cera Feminina", "Depilação a Laser — Preços por Área", etc.
  - [ ] Schema.org Service por categoria (name, description, offers com price + priceCurrency)
  - [ ] Schema.org BreadcrumbList: Home > Serviços
  - [ ] Open Graph com imagem representativa
  - [ ] Internal links: cada categoria linka pra página dedicada quando existir (laser → depilacao-a-laser.html)
  - [ ] Anchor text interno com keywords: "Veja preços de depilação a laser →"
  - [ ] Alt text nas fotos de serviço: "Depilação a cera feminina no Depillagos Araruama"
  - [ ] FAQ section (migrado do blog "Dúvidas sobre depilação a cera") com Schema.org FAQPage

---

## Sprint 3: Laser + Quem Somos + Contato

**Goal:** Páginas secundárias completas. Laser como diferencial principal com FAQ migrado do blog.

### S3-01 Página Laser

- **Status:** todo
- **Priority:** P0
- **Size:** L
- **Dependencies:** S1-02
- **Acceptance Criteria:**
  - [ ] `<title>`: "Depilação a Laser Araruama — Laser 4D | Preços | Depillagos"
  - [ ] `<meta description>`: "Laser 4D alemão com 4 comprimentos de onda. Todos os fototipos, peles bronzeadas. A partir de R$59,90. Avaliação gratuita. (22) 99235-4970"
  - [ ] H1: "Depilação a Laser 4D — Depillagos Araruama"
  - [ ] Hero dedicado laser 4D com `fetchpriority="high"`
  - [ ] Explicação da tecnologia: 4 comprimentos de onda, todos os fototipos, peles bronzeadas
  - [ ] H2: "Preços por Área" — tabela completa (~30 serviços laser do Trinks)
  - [ ] H2: "Laser Masculino" — seção dedicada (migrado do blog post)
  - [ ] H2: "Perguntas Frequentes" — FAQ migrado do blog (foliculite, gravidez, vantagens)
  - [ ] Schema.org FAQPage com Question/Answer pairs
  - [ ] Schema.org Service (name, offers, provider)
  - [ ] Schema.org BreadcrumbList: Home > Depilação a Laser
  - [ ] Open Graph com imagem do laser (1200x630)
  - [ ] Antes/depois (placeholder até ter fotos reais)
  - [ ] CTA avaliação gratuita WhatsApp com mensagem pré-preenchida
  - [ ] Internal links: voltar pra serviços, link pra contato/mapa
  - [ ] Image alt: "Equipamento de depilação a laser 4D no Depillagos Araruama"

### S3-02 Página Quem Somos

- **Status:** todo
- **Priority:** P0
- **Size:** M
- **Dependencies:** S1-02
- **Acceptance Criteria:**
  - [ ] `<title>`: "Quem Somos — Depillagos | Centro de Estética desde 2008"
  - [ ] `<meta description>`: "Fundado em 2008 por Luciene Freitas. 18+ anos cuidando da beleza em Araruama. 26K+ clientes, 25 profissionais. Atendimento acolhedor."
  - [ ] H1: "Quem Somos — Depillagos"
  - [ ] História: Luciene Freitas, 2008, começou com depilação a cera
  - [ ] Filosofia: "A beleza vem em todas as formas, tamanhos e cores"
  - [ ] Diferencial: sem hora marcada, preços acessíveis, acolhimento
  - [ ] Números: 18+ anos, 26K+ clientes, 25 profissionais
  - [ ] Foto do salão/equipe com alt descritivo
  - [ ] Schema.org AboutPage + BreadcrumbList
  - [ ] Open Graph
  - [ ] Internal links: CTA pra serviços, link pra contato

### S3-03 Página Contato

- **Status:** todo
- **Priority:** P0
- **Size:** S
- **Dependencies:** S1-02
- **Acceptance Criteria:**
  - [ ] `<title>`: "Contato e Localização — Depillagos Araruama"
  - [ ] `<meta description>`: "Rua Francisco A. da Silva, 120, Araruama/RJ. Seg–Sex 9h–19h, Sáb 9h–17h. WhatsApp (22) 99235-4970. Atendimento sem hora marcada."
  - [ ] H1: "Contato — Depillagos Araruama"
  - [ ] Google Maps embed (place ID `0x97693e540ec145:0x49b27925cdc5928f`)
  - [ ] Endereço completo com Schema.org PostalAddress
  - [ ] WhatsApp com link direto `wa.me/5522992354970`
  - [ ] Horários por setor (geral: seg–sáb, cabelo: ter–sáb)
  - [ ] Instagram @_depillagos com link
  - [ ] Schema.org ContactPage + BreadcrumbList
  - [ ] Open Graph
  - [ ] Internal links: CTA "Ver serviços", link pra laser

---

## Sprint 4: Polish + Deploy

**Goal:** Refinamento visual, performance, sitemap, deploy em produção.

### S4-01 Performance + Core Web Vitals + Acessibilidade

- **Status:** todo
- **Priority:** P0
- **Size:** M
- **Dependencies:** S3-03
- **Acceptance Criteria:**
  - [ ] Todas as imagens em WebP com fallback, `loading="lazy"` (exceto LCP), `width`/`height` explícitos
  - [ ] `srcset` para imagens hero (mobile 480w, tablet 768w, desktop 1200w)
  - [ ] Hero image: `<link rel="preload" as="image">` + `fetchpriority="high"` (CLS + LCP)
  - [ ] `<link rel="preconnect">` para Google Maps, Instagram
  - [ ] CSS inline no `<head>` (sem request adicional — já é a abordagem do depillagos_hair)
  - [ ] JS minimal, defer/async quando necessário
  - [ ] PageSpeed Insights Mobile 90+ / Desktop 95+
  - [ ] Core Web Vitals: LCP <2.5s, FID <100ms, CLS <0.1
  - [ ] Contraste WCAG AA em todos os textos (verificar com axe-core)
  - [ ] Alt text descritivo em todas as imagens
  - [ ] Semântica HTML5: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`
  - [ ] `<html lang="pt-BR">`, `<meta charset="UTF-8">`

### S4-02 SEO Technical — Sitemap, robots.txt, Redirects, Search Console

- **Status:** todo
- **Priority:** P0
- **Size:** M
- **Dependencies:** S3-03
- **Acceptance Criteria:**
  - [ ] `sitemap.xml` com 5 páginas + `<lastmod>` + `<changefreq>` + `<priority>`
  - [ ] `robots.txt` Allow all + link pro sitemap
  - [ ] `.htaccess` com 301 redirects (URLs antigas WordPress → novas URLs — ver PRD)
  - [ ] Forçar HTTPS via `.htaccess`
  - [ ] Redirect www → non-www (canonical)
  - [ ] Google Search Console: verificar propriedade, submeter sitemap
  - [ ] Google Business Profile: atualizar URL do site
  - [ ] Testar 301 redirects: `/servicos/` → `/servicos.html`, `/blog/*` → páginas corretas
  - [ ] Validar Schema.org em schema.org/validator e Google Rich Results Test
  - [ ] Validar Open Graph em opengraph.dev

### S4-03 Deploy Staging (Vercel)

- **Status:** todo
- **Priority:** P1
- **Size:** S
- **Dependencies:** S4-01
- **Acceptance Criteria:**
  - [ ] Projeto `depillagos-site` criado no Vercel
  - [ ] Deploy funcional em `depillagos-site.vercel.app`
  - [ ] Todas as páginas navegáveis
  - [ ] Imagens carregando corretamente

### S4-04 Deploy Produção (Hostinger)

- **Status:** todo
- **Priority:** P0
- **Size:** M
- **Dependencies:** S4-03
- **Acceptance Criteria:**
  - [ ] Backup do WordPress atual
  - [ ] Conteúdo de `public/` substituindo `public_html/`
  - [ ] depillagos.com.br servindo o novo site
  - [ ] www.depillagos.com.br redirect pra depillagos.com.br
  - [ ] HTTPS funcionando
  - [ ] Links antigos do WordPress redirecionando (301) para novas URLs

---

## Sprint 5: Post-MVP Enhancements

### S5-01 Promoções Ativas

- **Status:** todo
- **Priority:** P1
- **Size:** S
- **Dependencies:** S2-02
- **Acceptance Criteria:**
  - [ ] Seção de promoções na home
  - [ ] Promo 3 áreas destacada
  - [ ] Promoções sazonais (estrutura reutilizável)

### S5-02 Galeria de Fotos

- **Status:** todo
- **Priority:** P1
- **Size:** M
- **Dependencies:** S1-02
- **Acceptance Criteria:**
  - [ ] Galeria lightbox do ambiente do salão
  - [ ] Antes/depois laser (quando disponível)

### S5-03 Marcas Parceiras

- **Status:** todo
- **Priority:** P1
- **Size:** S
- **Dependencies:** S1-02
- **Acceptance Criteria:**
  - [ ] Logo carousel/grid: L'Oréal, Wella, Truss, Alfaparf, Aneethun
  - [ ] Links para páginas dos serviços com cada marca

### S5-04 Banner App Depillagos

- **Status:** todo
- **Priority:** P2
- **Size:** XS
- **Dependencies:** app publicado
- **Acceptance Criteria:**
  - [ ] Smart banner para download do app
  - [ ] Link para Google Play / App Store
