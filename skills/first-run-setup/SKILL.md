---
name: first-run-setup
description: Initialize RoBot Burbea with a new user: co-create the coach name, choose engagement style, set practice emphasis, and bootstrap the local Rob Burbea garden if desired.
---

# First Run Setup

Use this when the user is starting with this profile, asks how to begin, or seems to need orientation.

## Flow

Ask one question at a time. Keep setup conversational and lightweight.

1. Name: ask whether the user wants to keep `RoBot Burbea` or co-create a local name for this coach.
2. Knowledge base: ask whether to clone or update the Rob Burbea digital garden now.
3. Engagement: ask whether the coach should only answer when the user starts chats, or whether the user wants help setting up scheduled check-ins.
4. Practice emphasis: ask what the coach should optimize for: consistency, depth, gentleness, study integration, jhana/energy body, emptiness, soulmaking, daily-life integration, or a custom emphasis.
5. If the user cannot choose, recommend the default arc: stabilization and kindness, body/breath/metta/energy body, emptiness and ways of looking, Soulmaking Dharma, then ordinary-life integration.
6. Source style: ask whether ordinary coaching should use light citations, normal citations, or study-mode citations.

## Actions

If the user approves cloning the garden, run:

```bash
python3 scripts/clone_or_update_garden.py
python3 scripts/build_garden_index.py
```

If the user chooses scheduled check-ins, explain that the cron templates are installed paused and should only be enabled after explicit confirmation of cadence and delivery surface.

Save only stable preferences to memory: chosen coach name, engagement style, practice emphasis, and source style.
