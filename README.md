# MERADIO'N

MERADIO'N is a production-oriented campus radio platform with a Flutter listener app, FastAPI business API, PostgreSQL persistence, Next.js control room, and a direct AzuraCast/Icecast audio path.

## Architecture

Flutter and the Next.js dashboard call FastAPI over HTTPS. FastAPI owns authentication, roles, programs, schedules, announcements, requests, metadata, and a `/ws/radio` WebSocket. Flutter gets continuous audio directly from the configured AzuraCast/Icecast URL; FastAPI never streams audio. Nginx fronts the application containers, while PostgreSQL remains private.

## Repository layout

| Path | Purpose |
|---|---|
| `backend/` | FastAPI API, SQLAlchemy models, Alembic migration, seed tool, pytest tests |
| `mobile/` | Material 3/Riverpod Flutter listener application |
| `admin/` | Next.js + Tailwind admin control room |
| `infra/nginx/` | Reverse-proxy baseline |
| `docs/DEPLOYMENT.md` | VPS, DNS, TLS, backups, monitoring, Android release guide |

## Local development

Copy `.env.example` to `.env` and use secure values. Start PostgreSQL/FastAPI/Admin with `docker compose up --build`. The API docs are available at `http://localhost:8000/docs` and `/redoc`; health is `/api/health`. For a local Python workflow: create a virtual environment, `pip install -r backend/requirements.txt`, run `alembic upgrade head` from `backend/`, then `uvicorn app.main:app --reload`. Add sample non-production accounts/content with `python -m app.seed`; every seed account uses `ChangeMe123!` and must not be deployed.

For Flutter, install the Flutter SDK, run `cd mobile && flutter pub get && flutter run`. Android emulators access the local API through `10.0.2.2`; update `ApiService` or inject an environment-specific endpoint for real devices and production. Validate release builds with `flutter analyze`, `flutter test`, and `flutter build apk --release`.

For the dashboard, run `cd admin && npm install && npm run dev`, or use Docker. It uses the same warm Meradio'N palette: Rosewater `#FCECDF`, Crimson Velvet `#9E122C`, Tangerine `#EE6A43`, Coral Blush `#F99D90`, and Golden Glow `#FBCB77`.

## Configuration and security

Required server-side values are documented in `.env.example`: database access, JWT secret, AzuraCast URL/key/station ID, public stream URL, domains, and CORS origins. Do not commit `.env`, expose AzuraCast keys to the web/mobile clients, publish PostgreSQL, or use FastAPI as an audio relay. Configure DNS/TLS, UFW, Fail2ban, SSH keys, backups, monitoring, and official AzuraCast deployment as described in [the deployment guide](docs/DEPLOYMENT.md).

## Database migrations and testing

Run `alembic upgrade head`; rollback the initial migration with `alembic downgrade base`. Run backend tests from `backend/` with `pytest`. Tests cover health, registration/authenticated identity, request creation, and role-gated program management. Expand CI to run backend, Flutter, and `npm run build` before deployment.
