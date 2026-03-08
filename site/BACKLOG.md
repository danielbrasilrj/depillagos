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

- **Status:** done
- **Priority:** P0
- **Size:** S
- **Dependencies:** none
- **Acceptance Criteria:**
  - [x] Estrutura de diretórios criada (`public/`, `imagens/`, `logos/`)
  - [x] `favicon.png` copiado do app
  - [x] `.gitignore` criado
  - [x] Assets de imagens copiados do app (categorias, serviços)
  - [x] Logos das marcas copiados do depillagos_hair

### S1-02 CSS Design System

- **Status:** done
- **Priority:** P0
- **Size:** M
- **Dependencies:** S1-01
- **Acceptance Criteria:**
  - [x] CSS variables definidas (cores, tipografia, espaçamento)
  - [x] Reset + base styles
  - [x] Componentes reutilizáveis: `.card`, `.btn`, `.btn-whatsapp`, `.section`, `.grid`
  - [x] Responsivo: breakpoints mobile (default), tablet (768px), desktop (1024px)
  - [x] Header fixo com nav + logo + botão WhatsApp
  - [x] Footer com links, redes sociais, CNPJ, copyright 2026
  - [x] Baseado no estilo do `depillagos_hair/public/index.html`

### S1-03 Home Page — Banner Carousel + Categorias

- **Status:** done
- **Priority:** P0
- **Size:** L
- **Dependencies:** S1-02
- **Acceptance Criteria:**
  - [x] Banner carousel com 3 slides (autoplay 5s, dots, swipe no mobile)
  - [x] **Banner 1: Mês das Mães (maio)** — Promoção cabelo. CTA WhatsApp "Quero agendar"
  - [x] **Banner 2: Laser 4D** — CTA "Avaliação gratuita" → WhatsApp
  - [x] **Banner 3: Bem-vinda** — CTA "Ver serviços" → servicos.html
  - [x] Grid de 7 categorias com ícones e link pra servicos.html#categoria
  - [x] Scroll suave entre seções
  - [x] Animações fade-in no scroll

### S1-04 Home Page — Laser + Números + Depoimentos

- **Status:** done
- **Priority:** P0
- **Size:** M
- **Dependencies:** S1-03
- **Acceptance Criteria:**
  - [x] Seção destaque laser 4D — primeiro da Região dos Lagos, todos os fototipos, CTA avaliação gratuita
  - [x] Contador: 18+ anos, 26K+ clientes, 25 profissionais
  - [x] 4 depoimentos do Google Maps
  - [x] Google Maps embed com place ID real
  - [x] Endereço, horários, WhatsApp

### S1-05 Home Page — SEO On-Page

- **Status:** done
- **Priority:** P0
- **Size:** M
- **Dependencies:** S1-03
- **Acceptance Criteria:**
  - [x] `<title>` com keyword primária
  - [x] `<meta name="description">` com CTA
  - [x] H1 único
  - [x] Schema.org JSON-LD: BeautySalon, Organization, WebSite
  - [x] Open Graph + Twitter Card
  - [x] Geo meta tags
  - [x] `<link rel="canonical">`
  - [x] Internal links: nav, categorias, laser destaque
  - [x] Preconnect para Google Maps e Fonts

---

## Sprint 2: Catálogo de Serviços

**Goal:** Página completa com todos os 153 serviços organizados por categoria com preços reais do Trinks.

### S2-01 Serviços — Layout + Navegação

- **Status:** done
- **Priority:** P0
- **Size:** M
- **Dependencies:** S1-02
- **Acceptance Criteria:**
  - [x] Nav superior com 10 categorias (âncoras)
  - [x] Sticky category nav no mobile
  - [x] Layout de tabela por categoria
  - [x] CTA WhatsApp contextual (mensagem pré-preenchida)
  - [x] Busca/filtro de serviços (JS, client-side)

### S2-02 Serviços — Depilação (Cera Feminina + Masculina + Linha)

- **Status:** done
- **Priority:** P0
- **Size:** M
- **Dependencies:** S2-01
- **Acceptance Criteria:**
  - [x] ~20 serviços cera feminina com preços
  - [x] ~15 serviços cera masculina com preços
  - [x] 3 serviços linha com preços
  - [x] Promoção 3 áreas destacada (R$129,90 seg–qua / R$139,90 qui–sáb)

### S2-03 Serviços — Depilação Laser

- **Status:** done
- **Priority:** P0
- **Size:** M
- **Dependencies:** S2-01
- **Acceptance Criteria:**
  - [x] ~30 serviços laser com preços por área
  - [x] Avaliação gratuita destacada
  - [x] Link pra página dedicada do laser
  - [x] CTA WhatsApp "Agendar avaliação gratuita"

### S2-04 Serviços — Cabelo, Unhas, Sobrancelha, Estética

- **Status:** done
- **Priority:** P0
- **Size:** L
- **Dependencies:** S2-01
- **Acceptance Criteria:**
  - [x] ~18 serviços cabelo com preços (sob consulta onde aplicável)
  - [x] ~25 serviços manicure/pedicure com preços
  - [x] 4 serviços design sobrancelha com preços
  - [x] 4 serviços estética facial com preços
  - [x] 5 serviços estética corporal com preços
  - [x] Marcas mencionadas (Aneethun, L'Oréal, Wella, Truss, Alfaparf)
  - [x] Nota: cabelo não abre segunda

### S2-05 Serviços — SEO On-Page

- **Status:** done
- **Priority:** P0
- **Size:** M
- **Dependencies:** S2-04
- **Acceptance Criteria:**
  - [x] `<title>`: "Serviços e Preços — Depillagos Araruama | 153 Serviços"
  - [x] `<meta description>` com CTA
  - [x] H1 + H2 por categoria
  - [x] Schema.org Service por categoria + BreadcrumbList
  - [x] Open Graph
  - [x] Internal links (laser → depilacao-a-laser.html)
  - [x] FAQ section com Schema.org FAQPage

---

## Sprint 3: Laser + Quem Somos + Contato

**Goal:** Páginas secundárias completas. Laser como diferencial principal com FAQ migrado do blog.

### S3-01 Página Laser

- **Status:** done
- **Priority:** P0
- **Size:** L
- **Dependencies:** S1-02
- **Acceptance Criteria:**
  - [x] Title, meta description, H1, canonical
  - [x] Explicação da tecnologia 4D
  - [x] Tabela completa ~30 serviços laser
  - [x] Seção "Laser Masculino"
  - [x] FAQ (foliculite, gravidez, bronzeado, sessões, dor, diferença 4D)
  - [x] Schema.org FAQPage + Service + BreadcrumbList
  - [x] Open Graph
  - [x] CTA avaliação gratuita WhatsApp

### S3-02 Página Quem Somos

- **Status:** done
- **Priority:** P0
- **Size:** M
- **Dependencies:** S1-02
- **Acceptance Criteria:**
  - [x] Title, meta description, H1, canonical
  - [x] História: Luciene Freitas, 2008
  - [x] Filosofia + diferenciais
  - [x] Números: 18+ anos, 26K+ clientes, 25 profissionais
  - [x] Schema.org AboutPage + BreadcrumbList
  - [x] Open Graph

### S3-03 Página Contato

- **Status:** done
- **Priority:** P0
- **Size:** S
- **Dependencies:** S1-02
- **Acceptance Criteria:**
  - [x] Title, meta description, H1, canonical
  - [x] Google Maps embed
  - [x] WhatsApp, Instagram, endereço
  - [x] Horários por setor (geral + cabelo)
  - [x] Schema.org ContactPage + LocalBusiness + BreadcrumbList
  - [x] Open Graph

---

## Sprint 4: Polish + Deploy

**Goal:** Refinamento visual, performance, sitemap, deploy em produção.

### S4-01 Performance + Core Web Vitals + Acessibilidade

- **Status:** done
- **Priority:** P0
- **Size:** M
- **Dependencies:** S3-03
- **Acceptance Criteria:**
  - [x] `<link rel="preconnect">` para Google Maps, Fonts
  - [x] CSS inline no `<head>` (sem request adicional)
  - [x] JS minimal inline
  - [x] Semântica HTML5: `<nav>`, `<main>`, `<section>`, `<footer>`
  - [x] `<html lang="pt-BR">`, `<meta charset="UTF-8">`
  - [ ] PageSpeed Insights Mobile 90+ / Desktop 95+ (verificar manualmente)
  - [ ] Contraste WCAG AA (verificar manualmente)

### S4-02 SEO Technical — Sitemap, robots.txt, Redirects

- **Status:** done
- **Priority:** P0
- **Size:** M
- **Dependencies:** S3-03
- **Acceptance Criteria:**
  - [x] `sitemap.xml` com 5 páginas + `<lastmod>` + `<changefreq>` + `<priority>`
  - [x] `robots.txt` Allow all + link pro sitemap
  - [x] `.htaccess` com 301 redirects (WordPress → novas URLs)
  - [x] Forçar HTTPS via `.htaccess`
  - [x] Redirect www → non-www
  - [x] Security headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection)
  - [x] Cache headers para assets estáticos
  - [x] Gzip compression
  - [ ] Google Search Console: verificar propriedade, submeter sitemap (manual)
  - [ ] Google Business Profile: atualizar URL (manual)

### S4-03 Deploy Staging (Vercel)

- **Status:** done
- **Priority:** P1
- **Size:** S
- **Dependencies:** S4-01
- **Acceptance Criteria:**
  - [x] Projeto `depillagos-site` criado no Vercel
  - [x] Deploy funcional em `depillagos-site.vercel.app`
  - [x] Todas as páginas navegáveis
  - [x] Imagens carregando corretamente

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
