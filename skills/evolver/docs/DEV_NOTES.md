# Private Evolver Development Workspace
 
This is a **private, isolated** copy of the `evolver` skill.
Use this directory for experimental development, refactoring, and testing without affecting the live `skills/evolver` or `skills/feishu-evolver-wrapper`.

## Protocol
1.  **Isolation**: Do not run `npm link` or `openclaw install` from here into the main workspace.
2.  **Safety**: Test changes locally using `node index.js`.
3.  **Sync**: Only manually copy approved changes back to `skills/evolver`.
4.  **Git**: This folder should have its own git history or be ignored by the main repo's `.gitignore` if we want strict separation (or just tracked carefully).

## Current Version
Copied from `skills/evolver` on 2026-02-03.

## Release Workflow (Private Repo as Release Tool)

Goals:
- This private repo is the **source + release-tool repo** (contains publishing scripts and internal notes).
- The public repo `autogame-17/evolver` receives **build output (`dist-public`)**, not the private source tree.
- `docs/` and `memory/` are internal-only and MUST NOT be included in public build output (`scripts/build_public.js` validates and blocks them).

### Standard Release (private -> public + GitHub Release + ClawHub)

1) Finish changes in the private repo
- Bump `package.json` version (SemVer).
- Update changelogs in `README.md` and `README.zh-CN.md` (include historical versions).
- Commit and push (recommended style: `chore(release): prepare vX.Y.Z`).
- Create an annotated tag and push it (e.g. `v1.4.2`).

2) Create GitHub Release (private repo)
- Using GitHub CLI (Windows example path):
  - `& "C:\Program Files\GitHub CLI\gh.exe" release create vX.Y.Z --repo autogame-17/evolver-private-dev --generate-notes`

3) Build public output (`dist-public`)
- `npm run build`
- Note: the build writes `dist-public/package.json` (its version should match the release version).

4) Push to the public repo (publish build output, not source)
- Use the publish script: `node scripts/publish_public.js`
- Required env vars (PowerShell examples):
  - `$env:PUBLIC_REPO='autogame-17/evolver'`
  - `$env:PUBLIC_BRANCH='main'`
  - `$env:PUBLIC_USE_BUILD_OUTPUT='true'`
  - `$env:PUBLIC_RELEASE_ONLY='false'`
  - `$env:RELEASE_TAG='vX.Y.Z'`
  - `$env:RELEASE_USE_GH='true'` (prefer creating releases via gh)
  - `$env:CLAWHUB_REGISTRY='https://clawhub.ai'` (choose based on token compatibility)
- Note: this script clones the public repo into a temp directory, replaces its contents with `dist-public/`, then commits and pushes.

5) Create GitHub Release (public repo)
- `publish_public.js` will create it when `RELEASE_SKIP != true` and gh/token prerequisites are met.
- If you only want to fix public code without re-creating a release, set:
  - `$env:RELEASE_SKIP='true'`

6) Sync to ClawHub (optional; enabled by default)
- After GitHub release succeeds, `publish_public.js` publishes to two slugs:
  - `evolver`
  - `capability-evolver`
- Common toggles:
  - Disable: `$env:CLAWHUB_SKIP='true'`
  - Force enable: `$env:CLAWHUB_PUBLISH='true'`

### Common Pitfalls (Read This)

- Env vars can "stick" in the same shell session
  - If `$env:PUBLIC_RELEASE_ONLY='true'` was set previously, the script may only create a release and not push code, leaving the public repo unchanged.
  - Always explicitly set: `$env:PUBLIC_RELEASE_ONLY='false'` before publishing.

- `publish_public.js` checks whether the local tag already exists
  - If the private repo already has the local tag (e.g. `v1.4.2`), the script may fail with `Tag v1.4.2 already exists.` (to avoid partial publishes).
  - Options:
    1) Temporarily delete the local tag: `git tag -d vX.Y.Z`, then restore via `git fetch --tags origin` after publishing.
    2) Do not pass `RELEASE_TAG` and only push build output (you lose tag-related commit/message conventions).

- ClawHub registry endpoint differences
  - Some tokens are unauthorized against `https://www.clawhub.ai` but work with `https://clawhub.ai`.
  - If you see auth failures, try: `$env:CLAWHUB_REGISTRY='https://clawhub.ai'`.

- ClawHub visibility (hide/unhide)
  - If `inspect evolver` returns `Skill not found` after publishing, the skill may be hidden.
  - Run:
    - `clawhub.cmd --registry https://clawhub.ai unhide evolver --yes`
    - `clawhub.cmd --registry https://clawhub.ai unhide capability-evolver --yes`
