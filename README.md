# 🧠 Brainrot Rush 3D

**An Italian Brainrot endless runner.** Dodge trains, surf roofs, and sprint through the worlds of the brainrot universe as Tung Tung Tung Sahur and friends.

**▶ Play now:** https://popnoodler.github.io/BrainrotRun/

## Features

- **8 playable brainrot characters** — Tung Tung Tung Sahur, Tralalero Tralala 🦈, Bombardiro Crocodilo 🐊✈️, Lirilì Larilà 🌵🐘, Boneca Ambalabu 🐸🛞, Cappuccino Assassino ☕🗡️, Chimpanzini Bananini 🐒🍌, Frigo Camelo 🐫🧊 — all procedurally modelled, unlocked with coins
- **7 character zones** — every 600m you cross a gate into another character's world: their palette, scenery (log stumps & drums, ocean waves & giant Nikes, hangars, cacti, tire stacks, giant coffee cups, jungle palms), a giant version of them shouting their catchphrase, themed floating props, zone-skinned trains, and their own music key
- **Skill-driven scoring** — coin combos ×1–×5 with a fire-trail, near-miss slow-mo bonuses, roof-surfing rewards, HOP/DUCK clears, best-run marker to chase
- **Deep progression** — Brainrot Level (XP → coin bonus), 14-trophy wall with live progress, rotating missions, daily streak bonus, **Daily Challenge** runs with rotating modifiers, permanent upgrade shop, laps, coin storms and gems
- **Feel & polish** — squash-and-stretch, camera dips and FOV kicks, resume countdown, roll-cancel jumps, coyote time + jump buffering, haptics, per-character jingles, dynamic hi-hat layer at high combo
- **Installable PWA** — offline-capable, add-to-home-screen, adaptive quality on weak devices, colorblind-safe barrier arrows, reduced-motion support

## Tech

- Single-file **Three.js** (r160) game — no build step, no bundler; open `index.html`
- All characters and scenery are **procedural primitives** (no model files)
- `models/render_preview.py` — Blender-headless tool that re-creates the in-game builders and renders PNGs to inspect/iterate character likeness (`blender --background --python models/render_preview.py -- <name|lineup|scenery>`)
- Core systems (spawner fairness, landing physics, missions, progression) are **simulation-tested** by extracting the shipped code into Node harnesses — see PROGRESS.md
- Deployed to GitHub Pages via Actions (`.github/workflows/deploy.yml`)

## Development log

See [PROGRESS.md](PROGRESS.md) — 110+ versions of iterative development.
