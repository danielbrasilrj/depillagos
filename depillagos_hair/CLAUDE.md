# Depillagos Hair — Landing Page

Landing page estática do setor de cabeleireiro do Depillagos. Tema sazonal, atualmente **Mês da Mulher — Março 2026**.

## URLs

- **Vercel:** https://depillagoshair.vercel.app
- **Domínio:** https://www.depillagos.com.br/2026_mar_mes_mulher

## Estrutura

```
depillagos_hair/
├── public/
│   ├── index.html          ← página completa (HTML + CSS + JS inline)
│   ├── favicon.png          ← ícone da aba (boneca rosa Depillagos)
│   ├── imagens/
│   │   ├── Jacqueline.jpeg
│   │   ├── Jessica.jpeg
│   │   ├── Tauanny.jpeg      (nome correto: Tawanny — arquivo mantém grafia original)
│   │   ├── imagem_salao.jpeg
│   │   └── cronograma_capilar.jpeg
│   └── logos/
│       ├── loreal.png
│       ├── wella.png
│       ├── truss.png
│       ├── alfaparf.png
│       └── aneethun.png
└── videos/
    └── CLAUDE.md             ← links dos Instagram Reels embeddados na página
```

## Conteúdo da página

- **Hero:** chamada temática Mês da Mulher
- **Promoção:** Escova R$49,90 — promoção exclusiva de março
- **Serviços:** corte, coloração, escova, tratamentos capilares, progressiva
- **Equipe:** Jacqueline, Jéssica, Tawanny (fotos reais)
- **Vídeos:** 4 Instagram Reels embeddados via iframe
- **Marcas:** L'Oréal, Wella, Truss, Alfaparf, Aneethun
- **Depoimentos:** reviews reais do Google Maps com link para o perfil
- **Mapa:** Google Maps embed com place ID real
- **Horário cabelo:** Ter a Sex 9h–19h, Sáb 9h–17h (não abre segunda)
- **CTA:** WhatsApp (22) 99235-4970
- **Instagram:** @_depillagos
- **SEO:** Schema.org HairSalon, Open Graph, geo tags

## Cores (brand pink)

```css
--gold: #c81773;          /* primary — rosa Depillagos */
--gold-light: #e065a8;
--gold-dark: #c2185b;
--cream: #fdf2f8;         /* background */
--cream-dark: #fce7f3;
```

Cores extraídas de `depillagos_app_v2/apps/mobile/src/theme/tokens.ts`.

## Deploy

### Vercel

```bash
cd depillagos_hair/
npx --yes vercel@latest --yes --prod --scope daniels-projects-548066da
# Após deploy, setar alias:
npx --yes vercel@latest alias <deployment-url> depillagoshair.vercel.app --scope daniels-projects-548066da
```

- Projeto Vercel: `depillagos-hair` (scope: `daniels-projects-548066da`)
- Detalhes e troubleshooting em `memory/vercel-deploy.md`

### Hostinger

1. Gerar zip: `cd public/ && zip -r /tmp/depillagos_hair.zip .`
2. Upload via File Manager em `public_html/2026_mar_mes_mulher/`
3. Extrair com `.` no campo "folder name"

## Notas

- Página 100% estática (sem build, sem framework, sem package.json)
- Tema sazonal — ao trocar o mês/campanha, atualizar hero, promo banner, badge e footer
- Arquivo de imagem `Tauanny.jpeg` mantém grafia original do upload; o nome exibido na página é "Tawanny"
