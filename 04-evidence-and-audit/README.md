# 04 · Evidence and audit

"Momentum is a computed state." This pillar holds the clock that proves it:

- [`data/regulatory-dates.yaml`](data/regulatory-dates.yaml) — every governing date,
  sourced, with estimates flagged as estimates at the schema level.
- [`data/audit_clock.py`](data/audit_clock.py) — validates the dates, computes
  days-since/days-until against any `--as-of`, renders the fixed-date calendar.
- [`frameworks/audit-calendar.md`](frameworks/audit-calendar.md) — the rendered
  calendar. CI fails if it is stale.
- [`data/test_audit_clock.py`](data/test_audit_clock.py) — attacks the clock: control
  test, mutation guard, the exact day-count arithmetic, and a test asserting the
  rendered calendar contains no day counts (so the staleness check stays green on
  purpose, not by luck).

What is deliberately absent: evidence. `evidence_in_repo: none` is load-bearing —
nothing here reads a Jasper system, and the audit-state inventory (which SOC 2 window,
what slipped, what the certification body actually scheduled) is day-one work that only
exists inside.
