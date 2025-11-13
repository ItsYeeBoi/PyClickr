# PyClickr

A fast, hotkey-driven autoclicker built with **Python**, **DearPyGui**, and **pynput**.

> **Note:** Automation can be restricted or prohibited in some apps/games. Use responsibly and follow the relevant Terms of Service.

---

## Features

- Global hotkeys (start/stop) that work outside the app window
- Click spam
- Adjustable interval (CPS/seconds)
- In-app hotkey remapping
- Settings saved to user config folder
- Portable Windows build via PyInstaller
- Semantic-versioned releases from Conventional Commits

---

## Downloads

Grab the latest Windows build from **GitHub Releases**:
[**➡️ Releases page**](https://github.com/ItsYeeBoi/PyClickr/releases)

> Want to build it yourself instead? See **Build from source** below.

---

## Quick start (from source)

**Prereqs:** Python 3.7+ and `pip`.
> Note: Made with **Python 3.13.1**; earlier versions may work but are untested.

```bash
git clone https://github.com/ItsYeeBoi/PyClickr.git
cd PyClickr
python -m venv .venv
# Windows:
 .venv/Scripts/activate
# macOS/Linux:
 source .venv/bin/activate

pip install -r requirements.txt
python -m src.pyclickr.app
```

---

## Usage

- Launch the app.
- Use the slider to set **CPS** (Clicks Per Second).
- Use the configured **hotkey** to start/stop.
- Change hotkeys with the **Change Hotkey** button.

> On first run, the app may request accessibility/input permissions (see **Permissions**).

---

## Settings & file locations

- **Settings file**: `settings.json`  
  - **Windows:** `%APPDATA%\pyclickr\settings.json` (e.g., `C:\Users\<user>\AppData\Roaming\pyclickr\settings.json`)
  - Cross-platform support is not tested
- Typical keys: `cps`, `tart_stop_key`.

Settings are created on first run. Corrupt/missing files fall back to sane defaults.

---

## Build an .exe (PyInstaller)

With the spec file (recommended):

```bash
pip install pyinstaller
pyinstaller pyclickr.spec
```

Outputs to `dist/pyclickr/pyclickr.exe`.

If you add icons or data files, update `pyclickr.spec` accordingly.

---

## CI/CD & releases

This repo is set up for **Conventional Commits** + **semantic-release**:

- `feat: ...` → **minor** version bump
- `fix: ...` → **patch** bump
- `feat!: ...` or a `BREAKING CHANGE:` footer → **major** bump

A GitHub Action parses commit messages on pushes to `main`, bumps the version, tags the commit, publishes a **GitHub Release**, and a separate workflow builds and attaches the Windows `.exe`.

- Release workflow: `.github/workflows/release.yml`
- Binary build workflow: `.github/workflows/build-binaries.yml`

---

## Roadmap (ideas)

- Hold mouse button instead of click spam
- Right-click / middle-click modes
- Click at fixed coordinates / cursor position toggle
- GUI themes (light/dark)
- Per-OS packaging (macOS app bundle, Linux AppImage)

---

## Permissions & troubleshooting

- **Windows:** Some apps require “Run as administrator” for input injection.
- **macOS:** Grant **Accessibility** permissions (System Settings → Privacy & Security → Accessibility).
- **Antivirus/SmartScreen:** Unsigned executables may trigger warnings; verify checksums and download from the official Releases page.

---

## Development notes

- Package version is defined in `src/pyclickr/__init__.py` as `__version__`.  
- The app reads and displays this version in the GUI.
- Long-running work (click loop) runs on a daemon thread; the GUI must stay on the main thread.

Project structure:

```
src/pyclickr/
  __init__.py        # __author__, __title__, __version__, __license__
  app.py             # DearPyGui + pynput app
assets/
  PyClickr.ico       # app icon for Windows build
  settings.json     # default settings (copied to user config on first run)
pyclickr.spec        # PyInstaller spec
pyproject.toml       # project & semantic-release config
requirements.txt
.github/workflows/   # release + build pipelines
```

---

## License

MIT © **ItsYeeBoi**

See [LICENSE](./LICENSE) for details.

---

## Acknowledgements

- DearPyGui — https://github.com/hoffstadt/DearPyGui
- pynput — https://github.com/moses-palmer/pynput

---
