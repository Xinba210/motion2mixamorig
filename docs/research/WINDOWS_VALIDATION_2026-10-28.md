# Motion2MixamoRig v0.1.8 — Windows Validation Handoff
Date: 2026-10-28 (Asia/Taipei)

Status: **P0/P1 research only. DO NOT MERGE / RELEASE / SHIP.**
Purpose: safely evaluate upstream Motion2MixamoRig as a human-video-to-motion source for Rigforge / KineForge. This public fork contains no proprietary Pixal3D meshes, user video, licensed SMPL-X or Mixamo assets.

## Provenance / safety
- Fork: `Xinba210/motion2mixamorig`
- Isolated research branch: `research/v0.1.8-windows-validation`
- Pin: `f05a718188026b06e7ee64b47bab077970444b19` (upstream release v0.1.8, published 2026-10-24).
- Fork `main` intentionally remains at v0.1.0 (`78b624b8d909e68ebbfa9c996b7042571bbef524`).
- Windows workspace: `D:\\Xinba Tools\\Motion2MixamoRig-Research`.
- Local Git remote `upstream`: official fetch URL, intentionally invalid push URL; never push/PR to `MaxLiu22/Motion2MixamoRig`.
- No reset/clean/force checkout of existing Rigforge, KineForgeStudio, Mesh2Motion or Fable repositories.
- No production deploy, no automatic dependency/weight download, no commercial assets committed.

## Actual results on SuperAlice Windows
- Python `D:\\Xinba Tools\\Python\\python.exe`: **3.11.15**.
- Blender: **4.5.13 LTS**; Git: 2.53; NVIDIA GeForce RTX 5060 Laptop GPU available (GPU inference **not tested**).
- Git shallow clone of above isolated research branch: **PASS**; `git status` clean.
- `python -m compileall -q motion2mixamorig blender_extension`: **PASS, exit 0**.
- `python scripts/package_blender_extension.py --platform windows-x64`: **PASS, exit 0**.
- Package output: `dist/motion2mixamorig-0.1.8-windows-x64.zip` (236,521 bytes); ZIP integrity **PASS**. This is a local test build, **not** an official Windows release.
- Blender headless registration/unregistration of `motion2mixamorig_blender`: **PASS, exit 0** on 4.5.13.
- `python -m motion2mixamorig.cli doctor`: **FAIL / expected missing prerequisites, exit 1**. Present: NumPy, ffmpeg, configured extractor. Missing: SMPL-X NEUTRAL NPZ; Mixamo FBX; a single-person video or still; Python `cv2`, `torch`, and `gvhmr`.
- Therefore **NO real motion extraction, retargeting, GLB animation export, visual quality, foot IK, fingers, self-intersection diagnostics, or game-runtime test was completed**.

## Licensing HOLD
Project code Apache-2.0 does not clear dependency or asset licenses.
- Upstream `NOTICE.md` identifies GVHMR and SMPL-X research/noncommercial restrictions.
- MANO / HaMeR, HMR checkpoint families, YOLO and other dependency terms require separate audit.
- Do not assume any generated output is ready for commercial game production.
- Do not commit or redistribute model weights, registered body models, raw licensed character assets, or user-provided videos.

## Next gated QA plan
1. **P0** confirm repository push isolation and pin upstream SHA, dependency/weight hashes, license approvals and an isolated venv. No alterations to shipping systems.
2. **P1-A** install Python runtime dependencies into **isolated** environment; run `m2mr doctor`. Authorized users must obtain required registered assets directly from licensors.
3. **P1-B** run a clean 5–20 s single-actor full-body video with Mixamo Y Bot; retain `run.json`, `skeleton_motion.npz`, `mixamo_rotations.npz`, `mixamo_character.glb`, previews, `diagnostics.json`.
4. **P1-C** retarget the same skeleton to a second Mixamo rig using `--skeleton`; measure no need for repeated expensive extraction.
5. **P2** map to a Pixal3D high-poly swordsman only after independently validated skeleton/skin; preserve immutable original mesh, UV and PBR. Evaluate foot contact, hip motion, sword grip/trajectory, self-intersection and visible deformations frame by frame.
6. **P3** compare against Rigforge CMU/UAL motions and KineForge battle motions. Only verified and license-cleared results can enter an internal animation catalog.

## Acceptance status
- Static Windows / Blender add-on feasibility: **PASS**.
- Runnable inference environment: **BLOCKED**.
- Motion and commercial game integration: **NOT TESTED**.
- Release/merge approval: **NOT GRANTED**.

AI agents: Do not mark any unexecuted gate as PASS. Keep all new changes on a separate research branch, and never write to the official upstream repository.

## Continuation — 2026-10-28 (P1 isolated runtime and math QA)
- SuperAlice Windows machine online. Existing Rigforge, KineForgeStudio, Mesh2Motion, Fable asset directories were searched non-destructively for named SMPL-X / Mixamo / reference footage. No suitable licensed SMPL-X NPZ, Mixamo FBX or single-person full-body video was confirmed. Existing `mesh2motion-app/dist/animpreviews/human/*Sword*.mp4` are animation previews, **not** validated single-person live-action source videos.
- Isolated venv: `D:\Xinba Tools\Motion2MixamoRig-Research\.venv` using Python **3.11.15**, NumPy **1.26.4**. `chumpy==0.70` installed successfully with `--no-build-isolation`. Remaining project dependencies were initiated; do not assume fully installed until `doctor` is rerun.
- New public, asset-free `tests/test_foot_lock_math.py`: **9/9 PASS** on SuperAlice; `python -m unittest discover -s tests -p test_foot_lock_math.py -v` exit **0**.
- `.github/workflows/motion-math-regression.yml` runs exactly those tests with NumPy only on Windows + Ubuntu and does not download model weights or gate-kept assets.
- GitHub Actions push and PR runs **SUCCESS** ([run 40637273924](https://github.com/Xinba210/motion2mixamorig/actions/runs/40637273924), [run 40637275990](https://github.com/Xinba210/motion2mixamorig/actions/runs/40637275990)).
- Latest checked upstream release remains **v0.1.8** and commit **f05a718188026b06e7ee64b47bab077970444b19**.
- Pending: full runtime dependencies, licensed input assets, inference, retargeting/GLB export, animation quality, and commercial approvals. **Do not treat unit/CI PASS as animation acceptance.**

## Runtime install and doctor — verified 2026-10-28
- Isolated `uv pip install` for `motion2mixamorig==0.1.8` completed successfully: **exit 0**. The resulting environment includes `gvhmr==1.6.1`, `torch==2.14.1`, OpenCV, `smplx`, and `numpy==2.4.6`. This new NumPy version requires separate legacy `chumpy` compatibility scrutiny; no production inference certification implied.
- Re-ran `python -m motion2mixamorig.cli doctor` inside the isolated environment. Dependency probes for `numpy`, `cv2`, `torch`, `gvhmr` and `ffmpeg` all **OK**. Exit code remains **1**, solely because this workspace has no registered `SMPLX_NEUTRAL.npz`, Mixamo FBX or single-person source video/still.
- Re-ran nine motion-math regression tests after full install: **9/9 PASS**, exit code **0**.
- No licensed model assets, inference weights, original customer video, commercial game deliverable or generated animation GLB were created or downloaded.

## Late compatibility probe — Python 3.11 / chumpy (2026-10-28)
- Isolated runtime actual module imports: `numpy 2.4.6`, `torch 2.14.1+cpu`, `cv2 5.0.0`, `gvhmr` **PASS**. `torch.cuda.is_available()` **False** despite RTX 5060 hardware; CUDA inference needs separate verified wheel/runtime work.
- `uv pip check`: **106 installed packages compatible**, exit 0. This checks package metadata constraints, not legacy import/runtime behavior.
- Standalone `import chumpy`: **FAIL** under Python 3.11, `AttributeError: module inspect has no attribute getargspec`. This may affect workflows that import Chumpy; it has not yet been established whether the main inference path imports it.
- An **ephemeral, process-local** compatibility probe using `inspect.getargspec = inspect.getfullargspec` and only missing legacy NumPy aliases passed: `CHUMPY_SHIM_EXIT=0`. This does **not** mean production code is fixed; no changes were made to site-packages or global Python startup. Formal compatibility code should be added only after real inference coverage and impact review.
- P1 status: runtime packages installed, CLI doctor checks 5 software modules OK; **gated input assets missing; full end-to-end inference not attempted**.
