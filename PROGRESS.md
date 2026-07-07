# Brainrot Rush — progress

**Italian Brainrot endless runner** (Subway Surfers clone) starring **Tung Tung Tung Sahur**.
Single-file HTML5 canvas PWA at `C:\Users\adamt\BrainrotRun`. Built with the
[GAME_DEV_PLAYBOOK](../GAME_DEV_PLAYBOOK.md) loop (one verified change per iteration).

## Controls
- **Lanes:** ← / → / A / D / swipe left-right
- **Jump:** ↑ / W / Space / swipe up / tap
- **Roll:** ↓ / S / swipe down
- **Pause:** P / Esc / top-right button

## Architecture
- Pseudo-3D 3-lane road: `proj(z) = {scale: Z_CAM/(Z_CAM+z), y}` maps world distance→screen; lanes converge to horizon.
- State machine MENU / PLAY / OVER. rAF loop, dt clamped to 0.05.
- Obstacles resolve when `z<=0.4` in the player's lane: `jump` needs air, `roll` needs rolling, `block` must dodge.
- Coins collect at `z<=0.5` in-lane (`hi` coins need a jump).
- Persistence: `br_best` (distance), `br_coins` (total). Network-first SW (no stale-page pain).

## Version log
- **v1** — 2.5D canvas MVP (superseded).
- **v2** — fairness spawner.
- **v3** — FULL 3D REBUILD (Three.js): real Subway-Surfers runner, jump on trains/trucks, Sahur 3D model, city scenery, coins, deployed to Pages.
- **v4** freeze fix + PBR/texture model pipeline. **v5** Blender headless GLB pipeline (models/*.py→assets/*.glb, GLTFLoader). **v6** fix mesh-not-defined coin freeze. **v7** model-load diagnostics. **v8** power-ups (magnet/shield/2x).

## Backlog / ideas
- More brainrot characters (Tralalero Tralala 🦈, Bombardiro Crocodilo 🐊✈️, Lirilì Larilà, Boneca Ambalabu) as unlockable playable skins.
- Power-ups (magnet, jetpack/hoverboard equivalent, 2× coins, shield).
- Themed environments / biomes.
- Missions/daily, character select screen, shop (coins → unlock characters).
- Real art pass on Sahur + obstacles; brainrot voice/soundbites.
- Monetization (portal SDK: rewarded revive + 2× coins; interstitial on game over).
- Deploy to GitHub Pages + submit to CrazyGames (same loose-files flow as Splash Hero).

## Overnight session (2026-07-05) — v12→v18
- **v12** Difficulty curve: diffOf()=min(1,dist/1400); diff-scaled obstacle mix (early train/truck, late barriers), variable-length trains (14/22) with length-scaled roof coins, ramping 2-block density.
- **v13** Risk-reward scoring: coin-combo multiplier x1→x5, near-miss bonus (adjacent-lane train pass), roof-surf bonus, floating DOM score popups, 🔥 combo HUD.
- **v14** Roster: +Bombardiro Crocodilo 🐊✈️ (Blender-authored GLB, 3000 coins).
- **v15** Daily missions: 3 rotating goals (dist/coins/surf/near/combo/runs) w/ coin rewards + progress bars, auto-reroll.
- **v16** Biomes: 4 environments (Città/Tramonto/Notte Neon/Foresta) shift bg/fog/ground/building colors every 600m.
- **v17** Hoverboard 🛹 power-up: 10s plow-through invincibility + board mesh.
- **v18** Render polish (ACES tone mapping + rim light) + distance milestones (+50 coins/500m).

All verified structurally (node --check module + el-id/feature checks) and deployed to https://popnoodler.github.io/BrainrotRun/

## Live-feedback session (2026-07-06) — v71→v76
- **v71** User fixes: un-inverted L/R controls (mirrored screen-x), Subway-Surfers camera (higher/closer/steeper), Sahur rebuilt toward the Fortnite skin (bat-tapered body, big shouting face, cloth wrap, chunky bat).
- **v72** (superseded) billboards + tung drum in music + sky bomber.
- **v73** CHARACTER ZONES (user design): 7 zones, one per character — palette, entry banner, giant 3D character w/ catchphrase quips, themed floating props, per-zone music key, zone-locked bomber.
- **v74** Distinct zone scenery (no generic cubes): log stumps / waves + giant Nikes / hangars + watchtowers / cacti + rocks / tire stacks / giant coffee cups / palms + giant bananas. Per-character giant idle anims + zone-entry confetti.
- **v75** Geometry audit fixes (palm fronds fanned inward; banana tips floating) — verified against real three.js Euler math.
- **v76** Milestones are now TUNG TUNG TUNG drum moments; zone-aware game-over quips.
- Infra: Pages moved to workflow deploys w/ cancel-in-progress after transient "Deployment failed" emails; strict one-deploy-batch discipline.

## Never-stop session (2026-07-07) — v77→v97
- Juice/feel: combo fire-trail, per-character zone jingles, squash-stretch tuning, key-repeat fix, snappier dodge, roll camera dip, resume 3-2-1 countdown, near-miss slow-mo, landing dust ∝ impact.
- Progression: Brainrot Level (+2% coins/lvl), trophy wall w/ live progress, char grid, unlock fanfare, best-run marker, coin storms, level/achievement game-over callouts.
- Content: 8th character Frigo Camelo (render-verified), zigzag coin trails, zone gates.
- Sim/bug passes (real extracted code): progression clean; mission dupe-kind reroll FIXED; daily streak verified; spawner 30k rows — long-train row-overlap wall FIXED; 30fps roof-landing tunneling FIXED (swept check).
- Render-verified scenery fixes (hangar dome, cactus arms), power-up world visuals (magnet ring, shield bubble), adaptive quality governor, pause-menu missions.
