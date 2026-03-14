**BEFORE WRITING ANY CODE: Load the `tdd` skill (invoke Skill tool with `skill: "tdd"`). This is mandatory — do NOT skip it, do NOT just apply the pattern from memory.**

# Depillagos Trinks

Trinks API integration tools for Depillagos — analytics, data extraction, reporting, and automation scripts for the beauty salon business.

## Trinks API

- **Base URL:** `https://api.trinks.com/v1`
- **Auth:** `X-Api-Key` header + `estabelecimentoId: 243726`
- **Docs:** https://trinks.readme.io/reference/introducao
- **Establishment:** Depillagos (ID: 243726)
- **Rate limit:** ~10 req/s, add 300ms delay between paginated calls

Full endpoint reference in `.claude/commands/trinks.md`.

## Skills

9 skills under `.claude/skills/`. Key ones:
- `tdd` — mandatory before any code
- `data-analysis` — pandas, matplotlib for analytics
- `deep-research` — web search + crawling
- `domain-intelligence` — stack decisions
- `api-contract-testing` — API contract validation

## Interaction

- EXTREMELY concise. No polite filler.
- Execute commands without asking. Only confirm destructive ops.
- **Never commit or push** unless explicitly asked.

## Non-Negotiable Rules

- **TDD always. No exceptions.**
- Tests for every feature. Run them before committing.

## Context

- **26,260 clients** in Trinks
- **153 services** across 10 categories
- **25 professionals**
- Key endpoints: `/servicos`, `/agendamentos`, `/clientes`, `/profissionais`, `/transacoes`, `/vendas`, `/consumo`

## NFS-e

O Trinks é sistema de gestão (POS), **não fiscal**. A API não expõe dados de NFS-e (endpoint `/transacoes/notas-fiscais` documentado mas retorna 404). Toda documentação de NFS-e, conciliação e dashboard está em `notas_fiscais/CLAUDE.md`.

## Docs

- `autoatendimento.md` — Levantamento sobre o módulo de autoatendimento da Trinks (totem, pagamento via Stone, custos)
