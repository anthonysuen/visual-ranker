# Visual Ranker — working principles

Local-first, zero-backend, single-file HTML. Ranks a set of things against
a weighted rubric, four views (list/tournament/quadrant/tiers), plus a
Group lens that aggregates many people's boards and surfaces disagreement.
North star: a working platform to create AGGREGATE scores, shared by
passing board files/links around — no database, no accounts.

## Before executing ANY plan (the step-back rule)
The director (Anthony) has strong product instinct; the models are strong
builders. Do not just run an EXECUTE queue. First, out loud, answer:
1. REFRAME: is there a single idea that makes half these items unnecessary?
   (The aggregate table became a "Group lens" — one reframe deleted a
   whole view. That leap is the job, not the checklist.)
2. THREE MOVES AHEAD: where does this feature point? What does it unlock
   or block next? Design for move 3, not move 1.
3. 10x NOT 10%: does this deepen the wedge (aggregate + disagreement,
   local-first) or just polish? Prefer wedge.
Surface the reframe to the director BEFORE building, so it can be caught.

## Panel usage
- Tactical panels (bugs, code review): 3 models find, verify, execute.
- DIRECTION panels: ask the bigger-picture questions explicitly — "what
  does this become in a year, what's the sharpest wedge, what reframe are
  we missing" — not "suggest improvements." Rotate the synthesizer.
- Taste does not average across models. Panels generate options; the
  director picks the sharp one. Lean on that, don't average to mush.

## Quality gates
- score_version.py after each iteration (deterministic capability score).
- Verify every change in the browser (single-file app: real load, real
  interaction), not just "it parses." Hard-reload — the http server caches.
- Scale test features that touch aggregation (group lens O(items) = fine;
  per-contributor rendering O(items×people) = breaks past ~15).
