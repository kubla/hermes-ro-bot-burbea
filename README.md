# RoBot Burbea

RoBot Burbea is a Hermes profile distribution for a long-running meditation coach inspired by Rob Burbea's teachings without impersonating Rob Burbea.

It is designed as a first Hermes experience: install Hermes Desktop, install this profile, then begin with a local-first coach that can help you practice, study, reflect, and gradually shape a path over time.

## Install and Run

After Hermes is installed and configured:

```bash
hermes profile install github.com/kubla/hermes-ro-bot-burbea --alias
```

### Hermes Desktop

The most reliable Desktop path is:

```bash
hermes profile use ro-bot-burbea
hermes desktop
```

`hermes profile use ro-bot-burbea` makes this profile the sticky active profile. When Desktop opens, start a new chat and send:

```text
Use the first-run-setup skill.
```

You can also switch inside Desktop: open **Profiles**, confirm `ro-bot-burbea` is listed, then choose `ro-bot-burbea` from the profile switcher/profile rail before starting a new chat. Desktop's profile switcher changes the active profile context for new chats and opens that profile's backend as needed.

### CLI Fallback

If you created the alias during install:

```bash
ro-bot-burbea chat
```

Without the alias:

```bash
hermes -p ro-bot-burbea chat
```

## First Run

Start with:

```text
Use the first-run-setup skill.
```

The coach will ask whether you want to:

- keep the starting name `RoBot Burbea` or co-create another name
- clone the Rob Burbea digital garden as a local knowledge base
- use the coach only when you start chats or add scheduled check-ins
- orient practice toward consistency, depth, gentleness, study, jhana/energy body, emptiness, soulmaking, daily-life integration, or another emphasis

If you do not know what to choose, the default recommendation is a course that moves toward and then through Soulmaking Dharma.

## Knowledge Base

This profile does not vendor Rob Burbea's talks or the digital garden corpus. Instead, it treats the public garden as a dependency and can clone it locally:

```bash
python3 scripts/clone_or_update_garden.py
python3 scripts/build_garden_index.py
```

The source project is:

```text
https://github.com/fschuhi/digital-garden-rob-burbea-publish
```

See [docs/knowledge-base-rights.md](docs/knowledge-base-rights.md) before redistributing outputs that quote or transform the source material.

## Local First

The distribution does not choose a model provider and does not require provider-specific API keys. Configure Hermes itself however you normally would.

Practice logs, curriculum notes, safety notes, and the cloned garden stay local by default.

## Boundaries

RoBot Burbea is a meditation coach and study companion. It is not Rob Burbea, not the Hermes Amara Foundation, not a therapist, not a doctor, not a crisis service, and not a substitute for a qualified human teacher.

See [docs/coaching-contract.md](docs/coaching-contract.md) for the working contract.

## Development

Run tests:

```bash
/usr/bin/python3 -m unittest discover -s tests -v
```

Run the full local Hermes runtime interaction acceptance test with a fake OpenAI-compatible loopback provider:

```bash
RUN_HERMES_RUNTIME_ACCEPTANCE=1 /usr/bin/python3 -m unittest tests.test_acceptance_hermes_profile.HermesRuntimeInteractionAcceptanceTests -v
```

See [SPEC.md](SPEC.md) for the implementation spec.
