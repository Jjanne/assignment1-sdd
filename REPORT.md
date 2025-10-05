# Report – Assignment 1 (SD&D)

## SDLC Model: Iterative & Incremental (“Agile-lite”)

I built this in short, repeatable cycles: stand up a thin vertical slice (CRUD + SQLite), test it, then layer on small changes (filters, clearer errors, docs). That rhythm worked well for a small, single-developer project.

**Why this model fits here**
- **Small scope, fast change:** Requirements shift (e.g., swapping `lat/lng` for `start_location`) without derailing the plan.
- **Continuous verification:** After each change I could run the app, hit `/docs`, and add/adjust tests.
- **Low ceremony:** Minimal overhead, maximum momentum—ideal for a course assignment with a tight timeline.
- **Risk control:** There’s always a working baseline; each iteration is a safe, incremental improvement.

Result: I always had something working, and improvements landed in manageable, well-tested steps.

---

## Reflection: How I’d scale this with DevOps practices

If this evolved beyond a class project, here’s how I’d productionize it:

- **CI on every commit:** Run linting and tests (with coverage) in GitHub Actions. Fail the build if coverage drops below the agreed threshold (e.g., 90%).
- **Stronger automated tests:** Keep CRUD tests, add edge cases (bad IDs, invalid payloads), and a few integration tests that exercise the DB path end-to-end.
- **Database migrations:** Introduce **Alembic** so schema changes (like adding indexes or new fields) are versioned and repeatable across dev/staging/prod.
- **12-factor config:** Read `DATABASE_URL` and other settings from environment variables; never hard-code secrets.
- **Containerization:** Ship a small Docker image so dev/prod environments are consistent; use a volume for SQLite (or switch to Postgres in staging/prod).
- **Observability:** Add structured logs, a `/health` endpoint, and basic error tracking. Later, layer in request metrics or OpenTelemetry if needed.
- **Release management:** Version the API (e.g., `/v1`), keep a CHANGELOG, and treat breaking changes as formal, versioned releases.
- **Security + hygiene:** Pin dependencies, enable CORS only where needed, validate inputs at the boundary (Pydantic), and review dependency alerts.

These steps make the service easier to change, safer to deploy, and more transparent when something goes wrong—without losing the simplicity that made it quick to build.
