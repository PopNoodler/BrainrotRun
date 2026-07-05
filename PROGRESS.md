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
