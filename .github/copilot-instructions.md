# Copilot / AI Agent Quickstart for MedAudit ✅

## Purpose
This file captures the essential, actionable knowledge an AI coding agent needs to be immediately productive in this repo.

## Big picture (what to know first) 🔎
- MedAudit is a Django-based web tool for auditing medical network traffic and HL7 interactions. Main Django project: `medaudit` (folder `src/medaudit`).
- Two primary Django apps:
  - `hl7` (UI + HL7 tooling; templates in `src/templates/hl7/`) — provides the web UI and HL7 workflows.
  - `api` (REST endpoints under `/api/*`) — programmatic access to HL7 operations.
- Many HL7 operations are implemented as Python scripts under `src/hl7/hl7Scripts/` and `src/api/hl7Scripts/` (note: **scripts are duplicated** in both apps — be careful which one a view imports).
- State and logs are stored in `*/networkFiles/` (e.g., `hl7/networkFiles/hl7_messageSender.log`, `api/networkFiles/dosTrackingFile.txt`). These files are used by the runtime as simple flags/logs and are accessed via relative paths.

## Developer workflows & useful commands ⚙️
- Install dependencies (prefer the `src/` requirements for compatibility with the code):

  ```bash
  cd src
  pip install -r requirements.txt
  ```

- Run migrations if required and start dev server (UI is at `/about` by default):

  ```bash
  python manage.py migrate
  python manage.py runserver 8082
  # Visit: http://127.0.0.1:8082/about
  ```

- Run tests:

  ```bash
  python manage.py test
  ```

- Postman examples: `postman_collection/medaudit.postman_collection.json` (import into Postman to test API endpoints).

## Important conventions & gotchas ⚠️
- Dependency mismatch: root `requirements.txt` lists newer versions (including Django 6.0) while `src/requirements.txt` pins older versions (Django 2.2). The codebase (settings comment) and syntax align with Django 2.2. When in doubt, use `src/requirements.txt` and a Python 3.x runtime compatible with Django 2.2 (e.g., 3.6–3.8).
- Relative paths: many modules use local relative file paths (e.g., `api/networkFiles/dosTrackingFile.txt`, `hl7/networkFiles/...`). Ensure the working directory is the `src/` directory when running services, otherwise file access will fail.
- Background processes: DOS and malicious-server behaviors are started via `multiprocessing.Process` (see `api/views.py` and `hl7/views.py`). They rely on tracking files (e.g., `dosTrackingFile.txt`) to start/stop.
- Logging: scripts set up file-based logging (via `logging.basicConfig`) to `hl7/networkFiles/*.log` — logs are frequently overwritten (filemode='w').
- API responses are often plain strings, not structured JSON with HTTP status codes. Treat returned values as opaque strings in existing code.

## Key endpoints & examples (copy/paste) 🧪
- Send HL7 message (API)

  POST `/api/hl7/sendMessage`
  ```json
  { "ipAddress": "10.0.0.1", "port": 7777, "message": "MSH|...", "timeout": 2 }
  ```
  Returns: ack string or exception message (see `src/api/views.py`).

- Host port scan (API)

  POST `/api/hl7/hostScan`
  ```json
  { "ipAddress": "10.0.0.1", "port": 7777, "timeout": 2, "message": "MSH|..." }
  ```

- DOS test (API)

  POST `/api/hl7/dos`
  ```json
  { "ipAddress": "10.0.0.1", "port": 7777, "start": 1 }
  ```
  Behavior: when `start==1` it writes `1` to `api/networkFiles/dosTrackingFile.txt` and spawns the attack process; `start==0` writes `0` to stop.

- Malicious server (API)

  POST `/api/hl7/maliciousServerTest`
  ```json
  { "port": 7777, "message": "ACK...", "start": 1 }
  ```
  Behavior: spawns a server process via `multiprocessing.Process`.

## Files to inspect for implementation patterns 🔧
- `src/medaudit/settings.py` — app list and base settings
- `src/medaudit/urls.py` — mapping of web and API routes
- `src/api/views.py` and `src/hl7/views.py` — how endpoints are implemented
- `src/hl7/hl7Scripts/` and `src/api/hl7Scripts/` — core HL7 tooling (sender, scanner, fuzzer, DOS, analyzer)
- `postman_collection/*` — example payloads for API endpoints

## Priorities for contributors / agents 💡
- When modifying HL7 logic, make sure you update both copies (if they both remain necessary) or consolidate into a single shared utility to avoid drift.
- Prefer reading/writing the `networkFiles/` files via full paths resolved from `BASE_DIR` in `settings.py` (many modules currently use relative paths).
- Add structured API responses and proper HTTP status codes if extending API usage beyond simple PoCs.

---

If anything above is unclear or you want more examples (e.g., request/response pairs for each endpoint or pointers to consolidate duplicated HL7 scripts), say which section to expand and I will iterate. ✨
