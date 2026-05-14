# Virtual OS

## Preview

![Virtual OS Demo](assets/demo.mp4)

## Description
Virtual OS is a Python-based experimental project built with Arcade where I push the limits of real-time rendering, UI systems, and lightweight 3D simulation inside a 2D game framework.

The goal is to explore how far Python + Arcade can go in building OS-like interfaces, interactive systems, and custom 3D rendering pipelines.

Current development time: ~27 hours

---

## Features

- Layered 2D UI system (L2D Background)
- Chat-style AI interface ("ChatJT")
- Custom 3D engine (wireframe + projection-based rendering)
- Interactive 3D cube system
- Early GLTF model loading (experimental)
- Mouse-controlled camera rotation and movement
- Custom depth sorting for 3D objects

---

## Tech Stack

- Python
- Arcade
- Trimesh (for GLTF loading)
- Custom software 3D renderer (no GPU pipeline yet)

---

## Current Limitations

- No real GPU rendering (software projection only)
- No texture rendering support yet
- GLTF materials partially supported (PBR not fully used)
- No depth buffer (manual sorting only)
- Performance depends heavily on CPU

---

## Dependencies

### Python Libraries (pip install)

- arcade
- customtkinter
- noise
- trimesh
- pywebview
- requests

### Standard Library (built-in, no pip needed)

- json
- math
- os
- pathlib
- random
- subprocess
- sys

### Graphics / Engine Internals

- pyglet (used internally by Arcade, including pyglet.math)

### Platform-specific

- win32 APIs (Windows only, used indirectly via system calls or libraries)

---

## Installation

```bash
git clone <repo-url>
cd project-folder
pip install -r requirements.txt
