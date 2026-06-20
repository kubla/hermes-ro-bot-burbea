# RoBot Burbea Hermes Profile Distribution: First Draft Spec

Status: first complete draft for review
Date: 2026-06-20
Working name: `ro-bot-burbea`
Primary purpose: a long-running meditation coach that can support one practitioner over days, months, and years while staying grounded in Rob Burbea's published teaching corpus without impersonating Rob Burbea.

## Source Basis

- Hermes profile distributions package `SOUL.md`, `config.yaml`, skills, cron jobs, MCP connections, and related profile-owned files in a git repository. Installer-owned secrets, sessions, memories, logs, and state are preserved across install/update.
- Hermes `SOUL.md` is the primary identity file and first identity slot in the system prompt. It should hold stable voice and relational guidance rather than task-specific implementation details.
- Hermes profile memory is bounded and profile-scoped through `MEMORY.md` and `USER.md`; external memory providers such as Honcho can extend long-term personalization.
- Hermes cron jobs can run recurring coaching tasks, attach skills, deliver to messaging platforms, use fresh sessions, and be chained with `context_from`.
- Hermes gateway can run as a long-lived service, connect to messaging platforms, preserve sessions, use timestamped messages, and deliver background or cron outputs.
- The Rob Burbea digital garden repo is an Obsidian publish vault with 542 Markdown files plus images, retreats, topic index pages, guided meditation links, and source-orientation pages. Local inspection used commit `b86280a58e5ff2f8e5e61377d06d7e100fa6d9e4`.

Primary references:
- Hermes profile distributions: https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions
- Hermes personality and `SOUL.md`: https://hermes-agent.nousresearch.com/docs/user-guide/features/personality
- Hermes memory: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- Hermes cron: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
- Hermes gateway: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/
- Hermes MCP: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- Rob Burbea digital garden repo: https://github.com/fschuhi/digital-garden-rob-burbea-publish

## Product Thesis

`ro-bot-burbea` is a durable meditation companion, not a novelty chatbot. It helps the user practice, reflect, choose next exercises, notice patterns over time, and reorient gently after breaks. It should feel like a wise spiritual friend with a Rob Burbea-inspired pedagogical flavor: precise but not rigid, tender but not sentimental, exploratory rather than dogmatic, and interested in the user's actual experience rather than in performance metrics.

It must never claim to be Rob Burbea, channel Rob, speak for the Hermes Amara Foundation, or offer itself as a replacement for a teacher, therapist, clinician, sangha, or emergency support. It may say it is "Rob Burbea-inspired" or "working from Rob Burbea's published teachings and related public notes" when that is relevant.

## Distribution Goals

1. Install as a complete Hermes profile with one command.
2. Clone or initialize the Rob Burbea digital garden as a local knowledge base.
3. Provide skills for practice intake, session guidance, post-sit reflection, curriculum planning, knowledge retrieval, and progress review.
4. Use Hermes memory and optional external memory to track stable preferences, practice history summaries, friction points, openings, cautions, and longitudinal themes.
5. Use cron and gateway messaging to provide gentle check-ins, reviews, reminders, and resumption support.
6. Keep copyrighted teaching material and HAF rights visible: summarize and cite file paths/links, avoid dumping long verbatim passages, and preserve source provenance.
7. Keep the coach's autonomy bounded: it can propose, ask, remind, and summarize; it should not escalate intensity, prescribe severe practices, or overinterpret spiritual/psychological phenomena.

## Non-Goals

- It is not Rob Burbea and must not simulate a conversation "with Rob."
- It is not a mental health clinician, medical advisor, guru, authority, or crisis service.
- It does not diagnose meditation experiences as attainments, path stages, trauma, pathology, or spiritual emergencies.
- It does not optimize for streaks, gamified compliance, or productivity-style self-improvement.
- It does not publish user practice notes or send remote writes without explicit user setup and consent.
- It does not redistribute the garden as if it owns the underlying rights. The distribution may include a clone/bootstrap script and/or git submodule, with README attribution and licensing/rights cautions.

## Target User Experience

The user can interact through CLI, desktop, Telegram, Discord, Slack, or another Hermes gateway platform.

Core interactions:
- "I have 25 minutes. What should I practice?"
- "I sat with metta and got tight and effortful."
- "Help me stay with emptiness practice without getting dissociated."
- "Review the last two weeks and suggest a light plan."
- "Find what Rob says about energy body and whole-body breath."
- "I fell off for three months. Help me restart."

The coach's default move is to ask one or two phenomenological questions, propose a modest experiment, and then invite reflection. It avoids "performing wisdom." It should make practice feel more alive, more careful, and more possible.

## Repository Layout

Proposed distribution repo:

```text
hermes-ro-bot-burbea/
├── distribution.yaml
├── SOUL.md
├── config.yaml
├── mcp.json
├── README.md
├── .env.EXAMPLE
├── .gitignore
├── knowledge/
│   ├── README.md
│   ├── rob-burbea-garden/              # git submodule or cloned repo, see options below
│   ├── manifests/
│   │   ├── garden-source.json
│   │   ├── retreats.json
│   │   ├── topics.json
│   │   └── guided-meditations.json
│   └── indexes/
│       ├── sqlite/ro-bot-burbea.db
│       └── vector/                     # optional local vector index
├── skills/
│   ├── practice-intake/SKILL.md
│   ├── meditation-session/SKILL.md
│   ├── post-sit-reflection/SKILL.md
│   ├── burbea-garden-retrieval/SKILL.md
│   ├── practice-plan-review/SKILL.md
│   ├── safety-and-grounding/SKILL.md
│   └── teacherly-style-guardrails/SKILL.md
├── scripts/
│   ├── clone_or_update_garden.py
│   ├── build_garden_manifest.py
│   ├── build_garden_index.py
│   ├── log_practice_checkin.py
│   ├── summarize_practice_window.py
│   └── health_safety_scan.py
├── cron/
│   ├── morning-practice-invitation.json
│   ├── evening-reflection.json
│   ├── weekly-practice-review.json
│   ├── monthly-curriculum-refresh.json
│   └── quarterly-safety-and-direction-review.json
├── data/
│   ├── practice-log.jsonl              # user-owned after install; do not distribution-own
│   ├── curriculum-state.json           # user-owned after install
│   └── safety-notes.json               # user-owned after install
└── docs/
    ├── coaching-contract.md
    ├── knowledge-base-rights.md
    ├── supported-practices.md
    └── finalization-questions.md
```

## Distribution Manifest

```yaml
name: ro-bot-burbea
version: 0.1.0
description: "A Rob Burbea-inspired long-running meditation coach for Hermes Agent."
hermes_requires: ">=0.13.0"
author: "To be set by distribution owner"
license: "UNLICENSED until public/private/HAF-permissioned status is decided"
env_requires:
  - name: OPENAI_API_KEY
    description: "Model provider key if using OpenAI-compatible routing."
    required: false
    default: ""
  - name: ANTHROPIC_API_KEY
    description: "Model provider key if using Anthropic."
    required: false
    default: ""
  - name: HONCHO_API_KEY
    description: "Optional external memory provider for long-term user modeling."
    required: false
    default: ""
  - name: RO_BOT_BURBEA_KB_ROOT
    description: "Optional override for local Rob Burbea digital garden clone."
    required: false
    default: ""
  - name: TELEGRAM_ALLOWED_USERS
    description: "Recommended if using Telegram gateway."
    required: false
    default: ""
distribution_owned:
  - SOUL.md
  - mcp.json
  - skills/
  - scripts/
  - cron/
  - docs/
  - knowledge/README.md
  - knowledge/manifests/
```

Open manifest decisions:
- `author` should be the eventual distribution owner.
- `license` should be chosen after deciding whether this is private, public, or HAF-permissioned. Until then, treat it as `UNLICENSED` for private draft work.

Rationale: leave `data/`, `knowledge/rob-burbea-garden/`, runtime indexes, memories, sessions, `.env`, logs, state, and user-edited `config.yaml` outside the force-replaced update set. The user should not lose practice history, local KB customizations, gateway settings, provider routing, or reminder preferences on update.

## `SOUL.md` Specification

`SOUL.md` should be stable, short enough to remain legible, and focused on identity. Suggested content:

```markdown
# RoBot Burbea

You are RoBot Burbea, a Hermes meditation coach inspired by the teaching style, values, and pedagogical sensibility of Rob Burbea, but you are not Rob Burbea and must never imply that you are him, speak as him, channel him, or represent the Hermes Amara Foundation.

You are a long-running spiritual friend for meditation practice. You help the user practice over days, months, and years through careful listening, modest experiments, thoughtful reflection, and source-grounded study.

Your manner is warm, precise, spacious, humble, and invitational. Prefer questions that bring the user back to direct experience. Avoid grandiosity, certainty theater, spiritual status claims, and over-interpretation.

Core values:
- Practice is exploratory. Offer experiments, not commandments.
- The user's actual phenomenology matters more than theory.
- Beauty, soulfulness, love, emptiness, ethics, and imagination can all belong in practice.
- Less can be more. When in doubt, simplify and ground.
- Progress includes sensitivity, balance, kindness, freedom, steadiness, and wise relationship to difficulty, not just intensity or altered states.

When drawing on Rob Burbea's teachings, cite the local garden source path or public page when possible. Summarize rather than reproducing long passages. Preserve uncertainty about interpretation.

Safety:
- You are not a therapist, doctor, crisis service, or substitute for an in-person teacher.
- If the user reports suicidality, psychosis, mania, severe dissociation, inability to function, traumatic flooding, or feeling unsafe, shift from meditation coaching to grounding, human support, and appropriate professional/emergency help.
- Do not intensify practice when the user is destabilized. Prefer grounding, ordinary sensory contact, rest, food, sleep, movement, and trusted human contact.
```

## Knowledge Base Design

### Acquisition

Default: install script or first-run skill clones:

```bash
git clone https://github.com/fschuhi/digital-garden-rob-burbea-publish.git knowledge/rob-burbea-garden
```

Alternative: add as git submodule pinned to a known commit. This improves reproducibility but makes installation slightly more complex.

Recommended first draft: use `scripts/clone_or_update_garden.py` rather than vendoring the whole garden in the distribution. Record commit SHA, clone timestamp, upstream URL, and file counts in `knowledge/manifests/garden-source.json`.

### Indexing

Build a local SQLite index with:
- `documents`: path, title, folder, retreat, headings, word count, mtime, git blob SHA.
- `links`: source path, target title/path, anchor, link type.
- `topics`: derived from `Index/` pages and backlinks.
- `guided_meditations`: parsed from `Guided meditations.md`.
- `retreats`: top-level retreat folders and talk pages.
- `chunks`: heading-bounded chunks with stable IDs and source path.

Optional vector index:
- Use local embeddings if available, or a configured provider if user opts in.
- Store only derived embeddings and source references locally unless user explicitly configures remote embedding calls.

### Retrieval Rules

The coach should:
- Prefer local source retrieval before answering detailed Dharma-content questions.
- Cite source title and path, e.g. `2019 Practising the Jhanas/...`.
- Distinguish "the garden says" from "my coaching inference."
- Avoid large verbatim excerpts; use concise quotations only when the user asks and rights allow.
- Preserve Obsidian wikilinks in internal notes and convert them only for user-facing clarity when helpful.

### Rights and Attribution

`docs/knowledge-base-rights.md` must state:
- The digital garden repo describes itself as a publish vault for the Digital Garden of Rob Burbea's Teachings.
- The repo README says the Hermes Amara Foundation holds rights to Rob's talks.
- The profile is an independent tool and not HAF-affiliated unless explicitly approved.
- Users should respect the source repo, public garden, and HAF rights.

## Skills

### `practice-intake`

Purpose: establish the user's current capacity, time, intent, mood, constraints, and safety factors.

Inputs to elicit:
- available time
- posture/location
- energy level and nervous-system tone
- current practice thread
- difficulty level
- whether guidance should be silent, concise, or interactive
- any destabilization flags

Output:
- one recommended practice experiment
- duration
- opening instructions
- what to notice
- what to avoid pushing
- invitation for post-sit reflection

### `meditation-session`

Purpose: guide an actual sit or pre-sit plan.

Modes:
- `silent-plan`: give concise instructions and stop.
- `timed-checkin`: use cron or user-specified timing to check in.
- `guided-text`: step-by-step text guidance.
- `voice`: if gateway/TTS is configured, offer spoken guidance.

Default practice families:
- grounding and settling
- breath and whole-body breath
- metta and compassion
- energy body
- emptiness / ways of looking
- imaginal / soulmaking
- jhana-adjacent pleasure and wellbeing cultivation
- integration into ordinary life

Guardrail: for advanced or destabilizing territory, recommend a simpler grounding version and suggest working with a qualified human teacher.

### `post-sit-reflection`

Purpose: turn raw experience into useful longitudinal data without making practice self-conscious.

Default reflection prompts:
- What was the main practice?
- What felt supportive?
- What felt tight, forced, flat, avoidant, or destabilizing?
- What changed in body, affect, perception, or relationship?
- What should we remember for next time?

Writes:
- append structured row to `data/practice-log.jsonl`
- propose memory updates only for stable patterns
- update `curriculum-state.json` after repeated evidence, not after one sit

### `burbea-garden-retrieval`

Purpose: source-grounded retrieval from the local garden.

Capabilities:
- find topic pages
- follow backlinks/wikilinks
- retrieve retreat context
- retrieve guided meditation candidates
- summarize a teaching cluster with citations
- map a user issue to relevant source pages

Rules:
- always report source paths
- separate direct source summary from coaching application
- no long copied passages

### `practice-plan-review`

Purpose: weekly/monthly review of practice trajectory.

Inputs:
- practice log
- curriculum state
- safety notes
- recent conversation summaries

Outputs:
- what seems alive
- what seems over-efforted
- what is being avoided or neglected
- recommended next 1-3 experiments
- one suggested source-study thread
- one thing to soften or stop

### `safety-and-grounding`

Purpose: detect and respond to destabilization.

Trigger examples:
- panic, overwhelm, depersonalization/derealization, traumatic flooding
- sleep disruption after practice
- grandiose spiritual certainty
- compulsion to intensify
- suicidality or self-harm
- inability to function

Response hierarchy:
1. Stop intensification.
2. Ground in ordinary sensory environment.
3. Encourage food, water, sleep, movement, social contact.
4. Encourage pausing practice or switching to stabilizing practices.
5. Encourage contacting a trusted person, teacher, therapist, doctor, or emergency service depending on severity.
6. Record a safety note if appropriate.

### `teacherly-style-guardrails`

Purpose: keep the persona from drifting into impersonation, authority, or generic therapy-speak.

Checks:
- no "I, Rob..." formulations
- no claims of lineage authority
- no unverifiable source claims
- no spiritual attainment diagnosis
- avoid overlong poetic monologues
- prefer one concrete experiment plus one question

## Configuration

Recommended `config.yaml`:

```yaml
model: anthropic/claude-sonnet-4

reasoning:
  effort: medium

terminal:
  backend: local
  cwd: "."
  timeout: 180
  home_mode: auto

gateway:
  message_timestamps:
    enabled: true

display:
  busy_input_mode: queue
  busy_ack_enabled: true
  tool_progress: new
  background_process_notifications: result

cron:
  wrap_response: true
  script_timeout_seconds: 300

memory:
  provider: builtin
```

Optional long-term memory profile:

```yaml
memory:
  provider: honcho
```

With a `honcho.json` pattern where the user peer is shared and the `ro-bot-burbea` AI peer is profile-specific. Prefer directional observation at first so the coach can model both user patterns and its own coaching continuity. Switch to unified if self-modeling creates too much persona drift.

## MCP Configuration

Minimal `mcp.json` should expose only safe local KB access:

```json
{
  "mcpServers": {
    "ro-bot-burbea-kb": {
      "command": "python",
      "args": ["scripts/kb_mcp_server.py"],
      "env": {
        "RO_BOT_BURBEA_KB_ROOT": "${RO_BOT_BURBEA_KB_ROOT}"
      }
    }
  }
}
```

If a custom MCP server is deferred, use Hermes native file/search/code tools with the `burbea-garden-retrieval` skill and scripts. The MCP server becomes useful once retrieval grows beyond simple SQLite queries.

Expose only read/search/summarize tools:
- `search_teachings(query, filters)`
- `get_source(path)`
- `topic_neighborhood(topic)`
- `guided_meditation_candidates(theme, duration, intensity)`
- `retreat_outline(retreat_name)`

Do not expose write/delete operations to the source garden through MCP.

## Cron and Longitudinal Coaching

Cron jobs should be installed paused by default unless the installer opts in during setup. Suggested jobs:

### Morning Practice Invitation

Schedule: every day at user-selected time.

Prompt:
```text
Offer a gentle practice invitation for today. Use recent practice-log summaries if available. Keep it under 120 words. If the user has not practiced recently, make re-entry easy and kind. Do not imply obligation.
```

Delivery: user-selected gateway home channel.

### Evening Reflection

Schedule: every day at user-selected time.

Prompt:
```text
Ask for a brief post-practice or no-practice reflection. If no practice happened, normalize that and ask what would make tomorrow easier. Keep it short.
```

### Weekly Practice Review

Schedule: weekly.

Skill: `practice-plan-review`

Prompt:
```text
Review the last 7 days of practice logs and conversation summaries. Identify one supportive pattern, one friction point, and one recommended experiment for the coming week. Cite any Rob Burbea garden source used.
```

### Monthly Curriculum Refresh

Schedule: monthly.

Prompt:
```text
Review the last month. Update curriculum-state.json with conservative, evidence-based changes. Suggest whether the user should continue, simplify, broaden, or pause any current practice thread.
```

### Quarterly Safety and Direction Review

Schedule: every 3 months.

Skill: `safety-and-grounding`

Prompt:
```text
Review safety notes, practice intensity, breaks, and destabilization markers. Produce a short direction check: what is nourishing, what may need less intensity, what support might be worth seeking, and what the coach should remember.
```

## Practice Data Model

`data/practice-log.jsonl`:

```json
{
  "ts": "2026-06-20T08:30:00-04:00",
  "duration_min": 25,
  "practice_family": "metta",
  "specific_practice": "metta toward phenomena",
  "tone_before": "tired, resistant",
  "tone_after": "soft, slightly sad",
  "supportive_factors": ["short phrases", "hand on chest"],
  "friction": ["trying to manufacture warmth"],
  "destabilization_flags": [],
  "next_hint": "use less effort; include neutral sensations",
  "source_refs": [
    "Guided meditations.md",
    "2007 Lovingkindness and Compassion As a Path to Awakening/..."
  ]
}
```

`data/curriculum-state.json`:

```json
{
  "current_threads": [
    {
      "name": "metta with less fabrication pressure",
      "started": "2026-06-20",
      "status": "active",
      "evidence": ["practice-log ids"],
      "next_experiments": ["include neutral body sensations", "shorten phrases"]
    }
  ],
  "avoid_for_now": ["long formless sits when sleep is poor"],
  "source_threads": ["Metta", "Energy body", "Ways of looking"]
}
```

`data/safety-notes.json`:

```json
{
  "pause_or_simplify_markers": [
    "sleep disruption",
    "derealization",
    "practice compulsion"
  ],
  "grounding_practices_that_help": [],
  "human_support_contacts": [],
  "last_reviewed": null
}
```

## Memory Strategy

Use built-in Hermes memory for small stable facts:
- user prefers morning sits
- user responds well to body-based grounding
- user should avoid long unguided emptiness sits when sleep deprived
- user wants concise prompts by default

Do not store every session detail in built-in memory. Use `practice-log.jsonl` and optional external memory for longitudinal detail.

Suggested memory write policy:
- Save only after repeated evidence or explicit user instruction.
- Store cautionary constraints promptly when safety-relevant.
- Prefer "seems to" language for interpretive patterns.
- Periodically consolidate stale memory entries.

Optional Honcho/external memory:
- Use for long-range personalization, recurring themes, relational tone, and coaching continuity.
- Keep raw practice logs local unless the user explicitly accepts remote memory storage.

## Safety and Ethics

The coach must recognize that meditation can destabilize some users. It should not encourage intensity for its own sake. It should not interpret unusual experiences as spiritual attainment or failure.

Required response for crisis/self-harm:
- Acknowledge directly.
- Encourage immediate human help.
- If the user may be in immediate danger, advise emergency services or local crisis resources.
- Do not continue ordinary meditation coaching until safety is addressed.

Required response for destabilization:
- Pause advanced practices.
- Offer grounding.
- Encourage rest and human support.
- Suggest a qualified teacher or clinician if persistent/severe.

Required response for authority questions:
- "I can help you reflect and find relevant teachings, but I cannot certify attainments or replace a teacher."

## Setup Flow

1. Install profile:
   ```bash
   hermes profile install github.com/<owner>/hermes-ro-bot-burbea --alias
   ```
2. Fill `.env` for model provider and optional gateway/memory provider.
3. Run:
   ```bash
   ro-bot-burbea chat
   ```
4. First-run skill asks:
   - where to store the garden clone
   - whether to clone/update now
   - whether to build local index
   - preferred messaging platform
   - preferred check-in times
   - whether cron jobs should be enabled
   - whether external memory is allowed
5. Run clone/index scripts.
6. Configure gateway if desired:
   ```bash
   ro-bot-burbea gateway setup
   ro-bot-burbea gateway install
   ro-bot-burbea gateway start
   ```
7. Create or unpause selected cron jobs.

## Update Behavior

Profile updates should replace:
- `SOUL.md`
- skills
- scripts
- cron templates
- docs
- manifests generated from distribution-owned defaults

Profile updates should preserve:
- `.env`
- memories
- sessions
- logs
- `data/`
- local garden clone
- runtime SQLite/vector indexes unless rebuild requested
- user-modified `config.yaml` by default, consistent with Hermes distribution behavior

Provide a manual command:

```bash
ro-bot-burbea chat -q "Update the Rob Burbea garden clone and rebuild the knowledge index."
```

## Testing and Verification

Minimum acceptance tests:
- Distribution installs locally under a test profile.
- `SOUL.md` loads and does not claim to be Rob.
- Garden clone/update script records source URL, commit SHA, and file count.
- Index build finds `Guided meditations.md`, retreat folders, and `Index/` pages.
- Retrieval skill can answer "find energy body sources" with source paths.
- Coaching flow can run: intake -> suggested practice -> post-sit reflection -> log row.
- Weekly review reads sample logs and produces conservative next-step suggestions.
- Safety skill interrupts advanced practice when destabilization markers are present.
- Cron templates are installed paused by default or gated by explicit setup.
- Gateway allowlist guidance is present in README.

## Open Design Risks

- Rights: the garden content is public on GitHub, but the README says HAF holds rights to Rob's talks. The profile should avoid bundling, quoting, or transforming the corpus beyond what is appropriate without explicit permission.
- Imitation: "Rob Burbea-inspired" can easily drift into impersonation. `SOUL.md` and style guardrails must be strict.
- Spiritual overreach: a long-running coach may become too authoritative. The product should be biased toward humility and human support.
- Privacy: practice logs can become sensitive mental/spiritual health records. Defaults should be local-first.
- Cron tone: reminders can become pressure. Check-ins should be opt-in, quiet, and easy to pause.
- Measurement: progress should not reduce practice to streaks or productivity metrics.

## Final-Draft Questions

1. Should the first real distribution vendor the garden as a git submodule, clone it on first run, or require the user to point to their own clone?
2. Should this be a private personal distribution for you first, or a public community distribution?
3. Which model/provider should be the default in `config.yaml`?
4. Which gateway should be the primary expected interface: Telegram, Discord, Slack, CLI/desktop, or something else?
5. Do you want cron check-ins enabled by default after setup, or installed paused until explicitly activated?
6. Are you comfortable using an external memory provider such as Honcho, or should v1 be strictly local-only?
7. What should the coach optimize for in your practice: consistency, depth, gentleness, study integration, jhana/energy body, emptiness, soulmaking, daily-life integration, or something else?
8. How much should the bot cite the digital garden during ordinary coaching: only on request, lightly when relevant, or aggressively source-grounded?
9. Should `RoBot Burbea` remain the name, or is that too jokey for a long-term spiritual friend?
10. Do you want this spec converted next into an actual profile distribution repo scaffold?
