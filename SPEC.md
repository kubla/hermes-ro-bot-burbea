# RoBot Burbea Hermes Profile Distribution Spec

Status: final implementation spec for v0.1.0
Date: 2026-06-20
Repository: `kubla/hermes-ro-bot-burbea`
Profile name: `ro-bot-burbea`
Starting coach name: `RoBot Burbea`

## Intent

`ro-bot-burbea` is a public Hermes profile distribution that gives new and experienced Hermes users a long-running meditation coach as a first-class Hermes profile. It should install through the ordinary Hermes profile-distribution path, work well in Hermes Desktop by default, and remain useful from CLI or gateway surfaces for users who configure those later.

The coach is inspired by Rob Burbea's teaching style and teaching corpus, but it must never impersonate Rob Burbea, claim lineage authority, speak for the Hermes Amara Foundation, or behave as a substitute for a human teacher, therapist, doctor, sangha, crisis service, or emergency support.

The distribution is meant to feel like real work: it includes a specific `SOUL.md`, skills, setup flow, local practice records, local knowledge-base bootstrap/index scripts, source-grounded retrieval habits, and opt-in scheduling templates.

## User-Approved Product Decisions

- Package this as a normal Hermes profile distribution, using the happy-path repo layout Hermes documents.
- Make the GitHub repository public.
- Do not choose a default model provider or require provider-specific API keys. The user's Hermes installation or Desktop setup owns model/provider configuration.
- Make Hermes Desktop the primary recommended first experience.
- Use built-in local Hermes memory and local repo data only. Do not use Honcho or another external memory provider in v0.1.0.
- Do not enable scheduled check-ins by default. Install opt-in cron templates and have first-run setup ask whether the user wants scheduled engagement.
- Ask the user what the coach should optimize for: consistency, depth, gentleness, study integration, jhana/energy body, emptiness, soulmaking, daily-life integration, or another emphasis.
- If the user cannot choose a direction, recommend a course that progresses toward and then through Soulmaking Dharma.
- Draw heavily on the Rob Burbea digital garden. Source-grounding is a core differentiator, not an optional flourish.
- Keep `RoBot Burbea` as the default starting name, but have the coach invite the user to co-create a personal name for the coach during setup.

## Source Basis

Hermes profile distributions package a whole agent as a git repository: `distribution.yaml`, `SOUL.md`, `config.yaml`, skills, cron jobs, MCP configuration, and docs. Installer-owned data such as `.env`, memories, sessions, logs, state, and local runtime artifacts must survive updates.

Hermes `SOUL.md` is the profile's primary identity. It is the right place for stable voice, relational stance, boundaries, and non-impersonation rules.

Hermes skills are the right place for repeatable workflows: setup, intake, retrieval, guided sessions, reflection, review, and safety handling.

Hermes cron jobs are the right mechanism for scheduled check-ins and reviews, but they should be opt-in because reminders can become pressure.

The Rob Burbea digital garden repository is an Obsidian publish vault for "The Garden of the Soul: Rob Burbea's Teachings." Its README states that the Hermes Amara Foundation holds rights to Rob's talks. The distribution should not vendor the corpus or imply ownership. It should treat the garden as a local dependency cloned by the user and preserve attribution.

Public source dependency:

```text
https://github.com/fschuhi/digital-garden-rob-burbea-publish
```

Locally inspected source snapshot during spec work:

```text
b86280a58e5ff2f8e5e61377d06d7e100fa6d9e4
542 Markdown files
```

## Distribution Repository Layout

```text
hermes-ro-bot-burbea/
├── distribution.yaml
├── SOUL.md
├── config.yaml
├── mcp.json
├── README.md
├── SPEC.md
├── .env.EXAMPLE
├── .gitignore
├── cron/
│   ├── morning-practice-invitation.json
│   ├── evening-reflection.json
│   ├── weekly-practice-review.json
│   ├── monthly-curriculum-refresh.json
│   └── quarterly-safety-and-direction-review.json
├── docs/
│   ├── coaching-contract.md
│   ├── knowledge-base-rights.md
│   └── supported-practices.md
├── knowledge/
│   ├── README.md
│   └── manifests/
│       └── .gitkeep
├── scripts/
│   ├── clone_or_update_garden.py
│   ├── build_garden_index.py
│   └── log_practice_checkin.py
├── skills/
│   ├── first-run-setup/SKILL.md
│   ├── practice-intake/SKILL.md
│   ├── meditation-session/SKILL.md
│   ├── post-sit-reflection/SKILL.md
│   ├── burbea-garden-retrieval/SKILL.md
│   ├── practice-plan-review/SKILL.md
│   ├── safety-and-grounding/SKILL.md
│   └── teacherly-style-guardrails/SKILL.md
└── tests/
    ├── test_bootstrap_garden.py
    ├── test_index_garden.py
    ├── test_practice_log.py
    └── test_distribution_structure.py
```

Runtime paths ignored by git:

```text
knowledge/rob-burbea-garden/
knowledge/indexes/
data/
```

## Distribution Manifest

`distribution.yaml` should be deliberately provider-silent:

```yaml
name: ro-bot-burbea
version: 0.1.0
description: "A local-first, source-grounded meditation coach inspired by Rob Burbea's teachings."
hermes_requires: ">=0.13.0"
author: "kubla"
license: "MIT for this profile distribution; Rob Burbea source materials remain governed by their own rights holders."
env_requires: []
distribution_owned:
  - SOUL.md
  - config.yaml
  - mcp.json
  - skills/
  - scripts/
  - cron/
  - docs/
  - knowledge/README.md
  - knowledge/manifests/
```

The distribution should not require `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or any gateway secrets. Users should configure Hermes Desktop or Hermes setup normally.

## Personality

`SOUL.md` should do five things:

1. Establish RoBot Burbea as a starting identity, not a fixed mask.
2. Invite co-creation of a personal name during setup.
3. Define a Rob Burbea-inspired manner without impersonation.
4. Require source-grounded study when drawing on Rob's teaching corpus.
5. Keep safety and authority boundaries explicit.

Voice qualities:

- warm
- precise
- spacious
- phenomenological
- invitational
- source-grounded
- humble about uncertainty
- uninterested in spiritual performance

Default coaching shape:

1. Listen for the user's actual experience.
2. Ask one or two clarifying questions if needed.
3. Offer one modest practice experiment.
4. Name what to notice.
5. Name what not to push.
6. Invite reflection.
7. Record only stable, useful patterns.

## First-Run Setup

The first-run setup skill should ask the user:

1. Whether to keep the name RoBot Burbea or co-create a name for this coach.
2. Whether to clone or update the Rob Burbea digital garden now.
3. Whether they want the coach to answer only when they initiate chats, or to help set up scheduled check-ins.
4. If scheduled check-ins are desired, what cadence and tone they want.
5. What the coach should optimize for: consistency, depth, gentleness, study integration, jhana/energy body, emptiness, soulmaking, daily-life integration, or a custom emphasis.
6. If they cannot choose, whether they accept the default arc: stabilization and responsiveness, then energy body and metta, then emptiness/ways of looking, then Soulmaking Dharma.
7. How source-heavy ordinary coaching should be: light citations, normal citations, or study-mode citations.

The skill should make clear that the user can change all of these later.

## Knowledge Base Dependency

Recommended implementation: clone-on-first-run, not submodule and not vendored corpus.

Reasoning:

- This follows the spirit of public profile distribution: the profile repo stays small, installable, and inspectable.
- It respects the source repo as a separate project with its own rights context.
- It lets users update the garden dependency without profile updates.
- It avoids making this public repo look like a republication of Rob's talks.
- It still makes the corpus a real dependency through scripts, manifests, indexes, skills, and behavior.

Bootstrap script:

```bash
python3 scripts/clone_or_update_garden.py
```

Default clone path:

```text
knowledge/rob-burbea-garden/
```

Manifest output:

```text
knowledge/manifests/garden-source.json
```

Index output:

```text
knowledge/indexes/ro-bot-burbea.sqlite
```

The local index should include documents, links, topics, guided meditation entries, retreats, and heading-bounded chunks. Retrieval should always return source paths.

## Local Data

Practice records are local and ignored by git:

```text
data/practice-log.jsonl
data/curriculum-state.json
data/safety-notes.json
```

Built-in Hermes memory should store only small, stable facts:

- user prefers concise or spacious guidance
- user wants scheduled or chat-only engagement
- user responds well to a practice family
- safety constraints that should affect future suggestions
- chosen coach name

Detailed history belongs in local data files, not bounded prompt memory.

## Skills

Required skills:

- `first-run-setup`: onboarding and co-creation.
- `practice-intake`: current conditions and practice selection.
- `meditation-session`: concise guided practice plans.
- `post-sit-reflection`: local logging and integration.
- `burbea-garden-retrieval`: source-grounded retrieval from local garden clone/index.
- `practice-plan-review`: weekly/monthly review and next experiments.
- `safety-and-grounding`: destabilization, crisis, and simplification handling.
- `teacherly-style-guardrails`: non-impersonation and anti-authority checks.

Skills should be terse and operational. They should not read like generic AI personality copy.

## Cron Templates

Cron templates should be present but opt-in. The first-run setup skill may help the user create or unpause jobs after explicit consent.

Templates:

- morning practice invitation
- evening reflection
- weekly practice review
- monthly curriculum refresh
- quarterly safety and direction review

All scheduled outputs should be gentle, non-coercive, and easy to pause.

## MCP

`mcp.json` should be conservative in v0.1.0. Since the actual local retrieval is handled by scripts and skills, MCP can remain empty or documented as a future read-only local KB server. Do not expose write/delete operations to the garden through MCP.

## Safety

Required behavior:

- Do not diagnose attainments, trauma, pathology, or path stages.
- Do not intensify practice when the user is destabilized.
- If the user reports suicidality, psychosis, mania, severe dissociation, traumatic flooding, inability to function, or immediate danger, stop normal coaching and guide toward grounding and human/professional/emergency support.
- Recommend qualified human teachers or clinicians when the situation exceeds chat-based coaching.
- Treat spiritual authority as a risk. The coach is a tool and companion, not a guru.

## Verification Requirements

Before v0.1.0 is treated as publishable:

- `python3 -m unittest discover -s tests -v` passes.
- `python3 scripts/build_garden_index.py --garden <fixture> --output <tmp-db>` builds an index.
- `python3 scripts/log_practice_checkin.py --log <tmp-jsonl> ...` appends valid JSONL.
- `distribution.yaml` parses as YAML if PyYAML is available, or passes a conservative standard-library structural check.
- Required profile files exist.
- Required skills have `SKILL.md` files.
- Runtime paths remain ignored by git.
- GitHub repo visibility is public.

## v0.1.0 Scope

In scope:

- installable distribution shape
- final spec
- public README
- `SOUL.md`
- local-first config
- skills
- cron templates
- local garden bootstrap/index scripts
- practice logging script
- tests
- public GitHub sync

Out of scope:

- full custom MCP server
- external memory providers
- model-provider selection
- automatic gateway setup
- embedded copy of the Rob Burbea garden
- remote practice-note syncing
- clinical safety system beyond conservative coaching boundaries
