# VPS deployment

Use Ubuntu 24.04 LTS with at least 4 vCPU, 8 GB RAM, 100 GB SSD, a public IPv4 address, and reliable bandwidth. Run the app and the supported AzuraCast deployment independently; FastAPI never carries audio bytes.

1. Create a non-root `deploy` user, add SSH keys, disable password SSH authentication, then install Docker Engine and the Compose plugin.
2. Configure UFW: allow `OpenSSH`, `80/tcp`, and `443/tcp`; enable Fail2ban. Do **not** publish PostgreSQL or backend container ports.
3. Clone this repository, copy `.env.example` to `.env`, generate `JWT_SECRET` with `openssl rand -hex 48`, and assign strong database credentials.
4. Set `API_DOMAIN`, `ADMIN_DOMAIN`, `RADIO_DOMAIN`, CORS origins, and HTTPS `RADIO_STREAM_URL`. Configure A records for all three names to the VPS IP.
5. Start `docker compose up -d --build`, then run `docker compose exec backend alembic upgrade head`. Use `python -m app.seed` only in development.
6. Install AzuraCast using its official Docker deployment documentation on the same sufficiently sized VPS or a dedicated radio VPS. Create its station, obtain the API key, and put only the key in the server `.env`. Configure its public HTTPS stream in `RADIO_STREAM_URL`.
7. Replace the example Nginx server blocks with per-domain server blocks and use `certbot --nginx -d "$API_DOMAIN" -d "$ADMIN_DOMAIN"`. Test renewal with `certbot renew --dry-run`.

## Operations

Health: `curl -fsS https://$API_DOMAIN/api/health`. Watch `docker compose logs -f`, container CPU/RAM/disk, database storage, stream reachability, SSL expiry, and AzuraCast/Icecast status. Back up PostgreSQL daily using `pg_dump` to encrypted off-host storage; verify with `pg_restore --list`. Back up AzuraCast volumes/configuration according to its official procedure. Restore first into an isolated database, then schedule maintenance before promoting it.

## Mobile release

Set the production API address at build time in the mobile API configuration and never include server secrets. Run `flutter pub get`, `flutter analyze`, `flutter test`, then `flutter build apk --release`. The direct stream URL is returned by the authenticated-free radio metadata API; it is never proxied through FastAPI.
