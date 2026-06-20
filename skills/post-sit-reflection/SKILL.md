---
name: post-sit-reflection
description: Convert a meditation report into a concise reflection and optional local practice-log entry.
---

# Post-Sit Reflection

Use this after practice or when reviewing a recent sit.

## Ask

Ask at most three prompts:

- What practice did you do, and for how long?
- What supported practice?
- What felt tight, forced, flat, avoidant, or destabilizing?

## Reflect

Summarize:

- practice family
- support
- friction
- next hint
- whether to continue, simplify, or pause

## Local Log

If the user wants to record it, use:

```bash
python3 scripts/log_practice_checkin.py --duration-min <minutes> --practice-family <family> --note "<short note>" --source-ref "<source path>"
```

Do not log sensitive details unless the user explicitly wants them recorded.
