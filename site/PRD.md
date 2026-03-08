# Depillagos Site — Product Requirements Document

## Product Vision

Novo site institucional para depillagos.com.br que substitui o WordPress atual. Site 100% estático, mobile-first, com catálogo completo de 153 serviços e preços reais do Trinks. Primeiro centro de estética da Região dos Lagos com preços transparentes online.

**One-liner:** "Tudo sobre o Depillagos — serviços, preços e agendamento — em um site rápido e bonito."

---

## Problemas do Site Atual

| Problema | Impacto |
|---|---|
| WordPress/Elementor pesado | PageSpeed <40, bounce rate alto no mobile |
| Sem preços publicados | Cliente desiste antes de ir ao salão ou ligar |
| Página de serviços 404 | Página principal do catálogo quebrada |
| Página do laser 404 | Diferencial principal inacessível |
| Bacaxá ainda listada | Confunde clientes (unidade fechou) |
| Instagram @depillagosararuama | Errado — correto é @_depillagos |
| Copyright 2023 | Passa impressão de abandono |
| Sem Schema.org/Open Graph | Invisível no Google, preview ruim no WhatsApp |
| Blog abandonado | Último post fev/2025, conteúdo irrelevante |
| Design genérico | Não transmite identidade visual rosa da marca |

---

## Target Users

| Persona | Descrição | Necessidade |
|---|---|---|
| **Marina, 25** | Mora em Araruama, quer fazer laser mas não sabe preço | Tabela de preços clara, WhatsApp pra agendar |
| **Carla, 42** | Cliente fiel há 10 anos, faz cera mensal | Ver promoções, conferir preço antes de ir |
| **Turista, 30** | Visitando Região dos Lagos, precisa de manicure | Localização, horário, se atende sem hora marcada |
| **João, 35** | Quer depilação masculina mas tem vergonha de ligar | Ver serviços masculinos com preços, ir direto |

---

## MVP Feature Set

### P0 — Must Have (v1.0)

1. **Home Page** — Banner carousel, categorias de serviço, destaque laser, números (18+ anos, 26K+ clientes), depoimentos Google, localização, footer
2. **Banner Carousel (Home)** — 3 banners rotativos inspirados no app:
   - **Banner 1: Mês das Mães (maio)** — Promoção cabelo exclusiva. "Presenteie sua mãe com um dia de beleza". Escova + tratamento com preço especial. CTA WhatsApp.
   - **Banner 2: Laser 4D** — Destaque do diferencial principal. "Primeiro laser 4D da Região dos Lagos". Imagem do equipamento (reuse `banner-promo-laser.webp`). CTA avaliação gratuita.
   - **Banner 3: Bem-vinda ao Depillagos** — Institucional/acolhimento. "Atendimento sem hora marcada desde 2008". Imagem da recepção (reuse `banner-welcome.webp`). CTA catálogo de serviços.
3. **Catálogo de Serviços** — 153 serviços com preços reais do Trinks, organizados por 10 categorias, filtro/busca
4. **Página do Laser** — Tecnologia 4D, tabela de preços por área, FAQ (migrado do blog), CTA avaliação gratuita
5. **Quem Somos** — História (Luciene, 2008), filosofia, equipe
6. **Contato** — Mapa embed, endereço, WhatsApp, horários por setor
7. **SEO Completo** — Ver seção "SEO Strategy" abaixo (Schema.org, keyword mapping, internal linking, etc.)
8. **Design Rosa** — Identidade visual da marca (#c81773), consistente com o app
9. **Mobile-First** — Layout responsivo, touch-friendly, fast load
10. **WhatsApp CTA** — Botão fixo flutuante + CTAs contextuais por serviço

### P1 — Should Have (v1.1)

10. **Promoções** — Seção de promoções ativas (3 áreas, sazonais)
11. **Galeria de Fotos** — Ambiente do salão, antes/depois (laser)
12. **Blog Estático** — Posts migrados do WordPress (5 relevantes sobre laser/cera)
13. **Marcas Parceiras** — Logos das marcas de produto utilizadas

### P2 — Nice to Have (v1.2+)

14. **Integração App** — Banner/link para download do app Depillagos
15. **Chat WhatsApp Widget** — Widget flutuante com mensagem pré-preenchida por serviço
16. **Depoimentos Dinâmicos** — Puxar reviews do Google via API
17. **Multi-idioma** — Versão em inglês para turistas

---

## Explicitly NOT in Scope

- **CMS/admin** — preços atualizados manualmente via Trinks MCP. Sem painel.
- **Formulário de contato** — WhatsApp é o canal. Sem backend SMTP.
- **Agendamento online** — walk-in + WhatsApp. Sem calendário.
- **E-commerce** — sem venda de produtos online.
- **Bacaxá** — unidade fechou. Somente Araruama.
- **Blog CMS** — posts migrados como HTML estático, sem WordPress.

---

## Catálogo de Serviços (Trinks — 153 serviços, 10 categorias)

### Depilação Cera Feminina (~20 serviços)

| Serviço | Preço |
|---|---|
| Virilha total com ânus | R$82 |
| Virilha cavada com ânus | R$79 |
| Virilha total | R$68 |
| Perna inteira | R$81 |
| Meia perna | R$45 |
| Coxa | R$45 |
| Axila | R$30 |
| Braço | R$50 |
| Meio braço | R$38 |
| Buço | R$20 |
| Sobrancelha (limpeza) | R$39 |
| Nádegas | R$42 |
| Costas | R$45 |
| Faixa | R$23 |
| Queixo | R$20 |
| Seios | R$21 |
| Nariz | R$22 |
| Ânus | R$36 |
| Virilha comum | R$40 |
| **Promo: 3 áreas (seg–qua, dinheiro)** | **R$129,90** |
| **Promo: 3 áreas (qui–sáb)** | **R$139,90** |

### Depilação Cera Masculina (~15 serviços)

| Serviço | Preço |
|---|---|
| Tórax + abdomen | R$89 |
| Perna inteira | R$89 |
| Barba | R$64 |
| Braço | R$60 |
| Costas | R$56 |
| Nádegas | R$55 |
| Tórax | R$52 |
| Virilha comum | R$52 |
| Meia perna | R$50 |
| Coxa | R$49 |
| Abdomen | R$45 |
| Axila | R$35 |
| Sobrancelha (limpeza) | R$40 |
| Virilha total com ânus | R$92 |
| Virilha total | R$80 |
| Ombro | R$38 |
| Faixa | R$28 |
| Orelha | R$28 |
| Bigode | R$27 |
| Queixo | R$27 |
| Nariz | R$25 |
| Ânus | R$45 |

### Depilação Laser (~30 serviços)

| Serviço | Preço |
|---|---|
| **Corpo todo** | **R$299** |
| Perna completa | R$289 |
| Braços | R$149,90 |
| Costas | R$149,90 |
| Coxas | R$149,90 |
| Meia perna | R$149,90 |
| Barba | R$149,90 |
| Virilha completa | R$149,90 |
| Abdomen | R$79,90 |
| Axilas | R$79,90 |
| Glúteos | R$79,90 |
| Maçã do rosto | R$79,90 |
| Nuca | R$79,90 |
| Ombros | R$79,90 |
| Queixo prolongado | R$79,90 |
| Seios | R$79,90 |
| Virilha biquini | R$79,90 |
| Areola | R$59,90 |
| Ânus | R$59,90 |
| Bigode | R$59,90 |
| Buço | R$59,90 |
| Cóccix | R$59,90 |
| Costeletas | R$59,90 |
| Faixa de barba | R$59,90 |
| Linha alba | R$59,90 |
| Mãos e dedos | R$59,90 |
| Nariz | R$59,90 |
| Orelhas | R$59,90 |
| Perianal | R$59,90 |
| Pés e dedos | R$59,90 |
| Testa | R$59,90 |
| **Avaliação** | **Gratuita** |

### Depilação na Linha (3 serviços)

| Serviço | Preço |
|---|---|
| Buço | R$26 |
| Faixa | R$28 |
| Queixo | R$26 |

### Cabelo (~18 serviços)

| Serviço | Preço |
|---|---|
| Maquiagem | R$199 |
| Tratamento Wella | R$189,90 |
| Cauterização (Aneethun Kera) | R$159,90 |
| Tratamento Truss | R$159,90 |
| Coloração | R$155 |
| Tratamento L'Oréal (c/ escova) | R$150 |
| Tratamento Alfaparf | R$150 |
| Tratamento Aneethun | R$130 |
| Penteado | R$130 |
| Matização | R$129,90 |
| Plástica capilar (Aneethun Age) | R$119 |
| Corte estilizado | R$105 |
| Corte | R$79 |
| Aplicação de tinta | R$73 |
| Escova | R$63 |
| Detox capilar (Aneethun Detox) | R$59 |
| Hidratação (Aneethun Linha A) | R$59 |
| Alinhamento capilar (Aneethun Liss) | R$55 |
| Lavar e secar | R$40 |
| Baby liss | R$38 |
| Prancha | R$33 |
| Botox capilar | Sob consulta |
| Escova progressiva | Sob consulta |
| Reflexo / Luzes | Sob consulta |

### Manicure e Pedicure (~25 serviços)

| Serviço | Preço |
|---|---|
| Fibra de vidro | R$179 |
| Acrigel | R$162 |
| Banho de gel (mão inclusa) | R$99 |
| Fibra de vidro (manutenção) | R$99 |
| Acrigel (manutenção) | R$89 |
| SPA do pé (calosidade) | R$85 |
| Pedicure permanente | R$75 |
| Manicure permanente | R$72 |
| Pé e mão | R$65 |
| Unha postiça (avulsa) | R$65 |
| Unha aplicável avulsa | R$65 |
| Unha postiça mão | R$62 |
| Unha encapsulada mão | R$52 |
| Unha postiça (material cliente) | R$51 |
| SPA do pé (c/ 10min massagem) | R$50 |
| Fibra de vidro (retirada) | R$47 |
| Acrigel (retirada) | R$48 |
| Pedicure francesinha | R$38 |
| Unha postiça (retirada) | R$37 |
| Pedicure | R$35 |
| Manicure francesinha | R$33 |
| Manicure | R$30 |
| Massagem relaxante 20min | R$30 |
| Unha encapsulada avulsa | R$21 |
| Pedicure express | R$20 |
| Massagem relaxante 10min | R$20 |
| Manicure express | R$19 |

### Design de Sobrancelha (4 serviços)

| Serviço | Preço |
|---|---|
| Design com henna | R$73 |
| Design sobrancelha | R$56 |
| Sobrancelha linha (limpeza) | R$42 |
| Henna | R$34 |

### Estética Facial (4 serviços)

| Serviço | Preço |
|---|---|
| Cílios | R$169 |
| Limpeza de pele (completa) | R$129 |
| Peeling de cristal | R$89 |
| Peeling de diamante | R$79 |

### Estética Corporal (5 serviços)

| Serviço | Preço |
|---|---|
| Massagem turbinada | R$119 |
| Drenagem linfática | R$99 |
| Esfoliação corporal + banho de lua | R$99 |
| Massagem relaxante | R$99 |
| Esfoliação corporal | R$79 |

### Outros

| Serviço | Preço |
|---|---|
| Micropigmentação | R$450 |
| Micro manutenção | R$150 |
| Experiência única | R$89 |

---

## Blog Posts a Migrar (→ FAQ/conteúdo estático)

| Post WordPress | Destino |
|---|---|
| Como a Depilação a Laser Pode Ajudar a Combater a Foliculite | FAQ laser |
| Depilação a laser durante a gravidez, pode? | FAQ laser |
| Depilação a Laser Masculina | Seção "Laser Masculino" |
| Dúvidas sobre depilação a cera | FAQ serviços |
| Vantagens da depilação com o laser da Depillagos | Página laser |
| ~~O Enigma do Espelho~~ | Não migrar |

---

## SEO Strategy

### Keyword Mapping (por página)

| Página | Keywords primárias | Keywords secundárias |
|---|---|---|
| Home | depillagos, centro de estética araruama, depilação araruama | salão de beleza araruama, estética região dos lagos |
| Serviços | depilação preço araruama, manicure araruama, cabelo araruama | depilação cera preço, pedicure araruama, design sobrancelha |
| Laser | depilação a laser araruama, laser 4D região dos lagos | laser todos fototipos, depilação laser preço, laser masculino |
| Quem Somos | depillagos história, centro estética desde 2008 | luciene freitas, depillagos fundadora |
| Contato | depillagos endereço, depillagos telefone, depillagos horário | como chegar depillagos, depillagos whatsapp |

### Técnicas On-Page (aplicar em TODAS as páginas)

| Técnica | Implementação |
|---|---|
| **Title tags** | `<title>` único por página, keyword primária no início, max 60 chars. Ex: "Depilação a Laser Araruama — Preços | Depillagos" |
| **Meta description** | Única por página, 150-160 chars, com CTA e preço quando aplicável. Ex: "153 serviços com preços. Depilação a laser a partir de R$59,90. Atendimento sem hora marcada. WhatsApp (22) 99235-4970" |
| **H1** | Exatamente 1 por página, contém keyword primária |
| **H2/H3** | Hierarquia semântica, keywords secundárias naturalmente distribuídas |
| **URL slugs** | Clean URLs: `/servicos`, `/depilacao-a-laser`, `/quem-somos`, `/contato` |
| **Image alt text** | Descritivo + keyword quando natural. Ex: `alt="Equipamento de depilação a laser 4D no Depillagos Araruama"` |
| **Image file names** | Kebab-case descritivo: `depilacao-laser-araruama.webp`, não `IMG_001.jpg` |
| **Image optimization** | WebP, lazy loading (`loading="lazy"`), `width`/`height` explícitos (evitar CLS), `srcset` para responsivo |
| **Internal linking** | Toda página linka pra pelo menos 2 outras. Serviços linkar pra laser. Home linkar pra tudo. Anchor text com keywords. |
| **Breadcrumbs** | `Home > Serviços > Depilação a Laser` — Schema.org BreadcrumbList |
| **Canonical** | `<link rel="canonical">` em todas as páginas |
| **Mobile-first** | Google indexa mobile-first. Viewport meta, font-size 16px+, tap targets 48px+ |

### Schema.org Structured Data (JSON-LD)

| Schema | Página | Campos |
|---|---|---|
| **LocalBusiness + BeautySalon** | Home, Contato | name, address, geo, telephone, openingHours, priceRange, image, url, sameAs (Instagram) |
| **Service** | Serviços, Laser | name, description, provider, areaServed, offers (price, priceCurrency) |
| **BreadcrumbList** | Todas (exceto home) | itemListElement com position, name, item |
| **FAQPage** | Laser | mainEntity com Question/Answer pairs |
| **Organization** | Home | name, url, logo, foundingDate (2008), founder, contactPoint |
| **WebSite** | Home | name, url, potentialAction (SearchAction se implementar busca) |

### Técnicas Off-Page / Technical SEO

| Técnica | Implementação |
|---|---|
| **sitemap.xml** | 5 páginas, `<lastmod>` atualizado, submeter no Google Search Console |
| **robots.txt** | Allow all, link pro sitemap |
| **Google Search Console** | Verificar propriedade, submeter sitemap, monitorar indexação |
| **Google Business Profile** | Atualizar URL do site para novo URL, adicionar fotos, manter reviews |
| **301 redirects** | URLs antigas do WordPress → novas URLs (via `.htaccess` no Hostinger) |
| **HTTPS** | Forçar HTTPS, HSTS header se possível |
| **Page speed** | Target: 90+ mobile, 95+ desktop. HTML estático = vantagem enorme vs WordPress |
| **Core Web Vitals** | LCP <2.5s (hero image otimizada), FID <100ms (sem JS pesado), CLS <0.1 (dimensões de imagem explícitas) |
| **Open Graph** | `og:title`, `og:description`, `og:image` (1200x630), `og:url`, `og:type` por página |
| **Twitter Card** | `twitter:card=summary_large_image` + mesmos dados do OG |

### Conteúdo SEO (migrar do blog)

| Conteúdo | Formato no novo site | Keywords alvo |
|---|---|---|
| Foliculite + laser | FAQ na página laser | "laser foliculite", "depilação a laser foliculite" |
| Laser na gravidez | FAQ na página laser | "depilação laser grávida", "laser gestante" |
| Laser masculino | Seção na página laser | "depilação laser masculina araruama" |
| Dúvidas depilação cera | FAQ na página serviços | "depilação cera dúvidas", "depois da cera" |
| Vantagens do laser | Conteúdo na página laser | "vantagens depilação laser", "por que laser" |

### 301 Redirects (.htaccess)

```apache
# WordPress URLs → novo site
RewriteRule ^servicos/?$ /servicos.html [R=301,L]
RewriteRule ^depilacao-a-laser/?$ /depilacao-a-laser.html [R=301,L]
RewriteRule ^quem-somos/?$ /quem-somos.html [R=301,L]
RewriteRule ^fale-conosco/?$ /contato.html [R=301,L]
RewriteRule ^blog/como-a-depilacao-a-laser-pode-ajudar/?$ /depilacao-a-laser.html#faq [R=301,L]
RewriteRule ^blog/depilacao-a-laser-durante-a-gravidez/?$ /depilacao-a-laser.html#faq [R=301,L]
RewriteRule ^blog/depilacao-a-laser-masculina/?$ /depilacao-a-laser.html#masculino [R=301,L]
RewriteRule ^blog/duvidas-sobre-depilacao-a-cera/?$ /servicos.html#faq-cera [R=301,L]
RewriteRule ^blog/vantagens-do-laser-depillagos/?$ /depilacao-a-laser.html [R=301,L]
RewriteRule ^blog/?$ / [R=301,L]
RewriteRule ^lojas/loja-bacaxa/?$ /contato.html [R=301,L]
RewriteRule ^lojas/loja-araruama/?$ /contato.html [R=301,L]
```

---

## Success Metrics

| Métrica | Target (3 meses) |
|---|---|
| PageSpeed Mobile | 90+ |
| PageSpeed Desktop | 95+ |
| Posição "depilação araruama" Google | Top 3 |
| Posição "laser araruama" Google | Top 3 |
| Bounce rate mobile | <40% |
| WhatsApp clicks/mês | 100+ |
| Tempo médio na página serviços | >2min |

---

## Delivered Tasks

| Task ID | Description | Status | Date |
|---|---|---|---|
| S1-01 | Project Setup (dirs, favicon, assets, logos) | done | 2026-03-08 |
| S1-02 | CSS Design System (vars, components, nav, footer) | done | 2026-03-08 |
| S1-03 | Home — Banner Carousel + Categorias | done | 2026-03-08 |
| S1-04 | Home — Laser + Números + Depoimentos + Mapa | done | 2026-03-08 |
| S1-05 | Home — SEO On-Page (Schema, OG, meta) | done | 2026-03-08 |
| S2-01 | Serviços — Layout + Nav + Busca | done | 2026-03-08 |
| S2-02 | Serviços — Depilação Cera (fem + masc + linha) | done | 2026-03-08 |
| S2-03 | Serviços — Depilação Laser | done | 2026-03-08 |
| S2-04 | Serviços — Cabelo, Unhas, Sobrancelha, Estética | done | 2026-03-08 |
| S2-05 | Serviços — SEO + FAQ | done | 2026-03-08 |
| S3-01 | Página Laser 4D (tech, preços, FAQ, masculino) | done | 2026-03-08 |
| S3-02 | Página Quem Somos (história, valores, diferenciais) | done | 2026-03-08 |
| S3-03 | Página Contato (mapa, horários, WhatsApp) | done | 2026-03-08 |
| S4-01 | Performance (preconnect, inline CSS/JS, semântica) | done | 2026-03-08 |
| S4-02 | SEO Technical (sitemap, robots, .htaccess, 301s) | done | 2026-03-08 |
| S4-03 | Deploy Staging (Vercel) | done | 2026-03-08 |
