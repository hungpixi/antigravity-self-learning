---
name: worldquant-alpha-factory
description: >-
  WorldQuant BRAIN alpha-factory pipeline defaults, env conventions, VPS deploy,
  and generator focus modes. Use when the workspace mentions alpha-factory, WQ Brain,
  WorldQuant, Sharpe, simulation settings, hypothesis_driven, VPS deploy for alpha
  mining, rsync systemd, or hungpixi/alpha-factory-private.
---

# WorldQuant Alpha Factory — Agent Defaults

Apply these conventions **without waiting for the user to repeat them** when `alpha-factory`, `WQ Brain`, or WorldQuant mining appears in context.

## 1. Simulation alignment (BRAIN “fast screen”)

- Prefer **`ASYNC_MARKET_PROFILE=usa_brain`**: USA, **TOP200**, delay 1, **SECTOR**, decay **[2]**.
- Avoid **`usa_fast`** unless the user explicitly wants TOP1000 / INDUSTRY (different from the BRAIN UI baseline they saved).
- **`wq_client` payload defaults** (override via env): `WQ_SIM_TRUNCATION=0.1`, `WQ_SIM_PASTEURIZATION=OFF`, `WQ_SIM_NAN_HANDLING=OFF`, `WQ_SIM_UNIT_HANDLING=VERIFY`.

## 2. Generator / Sharpe-first prior

- **`GENERATOR_MODE=hypothesis_driven`** for async pipeline when tuning for short-horizon edge.
- **`ALPHA_FOCUS_MODE=fast_sharpe`**: heavy **mean_reversion + overreaction**, **price_volume + liquidity** ~20%, **momentum ~0**. Alternatives: `balanced_hypotheses`, `momentum_ramp`.
- Legacy seeds: optional **`ASYNC_SEED_MODE=sharpe_fast`** (reversion/microstructure-heavy, weak fundamental).

## 3. `alpha_factory_cli` profiles (`auto --profile vps`)

- **`_profile_env` merges `local` + overlay** (`vps`, `gha`). Subprocess always gets full WQ/async defaults; **`.env` still wins** (`os.getenv` first).
- Do not assume `vps` only sets three keys anymore.

## 4. `.env` hygiene

- **Never commit** `.env`. Keep `WQ_EMAIL` / `WQ_PASSWORD` only local and on VPS `EnvironmentFile`.
- After changing local `.env`, **sync to VPS** with `scp` (rsync workflow excludes `.env`).
- If pytest fails in `test_optimizer`, cause is often **real `.env` lowering gates** — tests patch `ASYNC_MIN_SHARPE`, `ASYNC_MIN_FITNESS`, `ASYNC_REQUIRE_ALL_CHECKS`, `ASYNC_MIN_CHECKS_RATIO`; preserve that pattern.

## 5. VPS deploy & runtime (GitHub Actions + Ubuntu)

- Workflow must **`mkdir -p "$VPS_APP_PATH"`** on remote **before** `rsync` (parent dir may not exist on fresh VPS).
- On clean Ubuntu, install **`python3-venv`** (and `python3-pip`) **before** `python -m venv .venv`.
- **First deploy**: install **`alpha-factory.service`** from `deploy/alpha-factory.service.example` with root path substitution; `daemon-reload`, `enable`, `restart`.
- **SSH**: after VPS reinstall, **`ssh-keygen -R <host>`** if host key changed; deploy key in GitHub Secret `VPS_SSH_KEY` only.
- **Common failures**: WQ `API rate limit exceeded`; placeholder `.env`; asyncio noise on rapid `systemctl restart`.

## 6. Repo reference

- Private app repo: **`hungpixi/alpha-factory-private`**. Docs: `DEPLOY_VPS.md`, `.env.example`.

## 7. Security

- No real credentials in this skill or public site copies.
