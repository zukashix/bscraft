# BSCraft Launcher

Source for BSCraft 3.0 Launcher & Bootstrapper <br>
BSCraft is a vanilla+ lightweight minecraft modpack 

## For Players
- If you are a player wanting to download and play BSCraft, please head over to the "[**Releases**](https://github.com/zukashix/bscraft/releases/tag/Bootstrapper)" page and download the latest application.

## Progress

- Launcher bootstrapper = Complete ((1))
- Bootstrapper development-platform test (ubuntu/aarch64) = Success ((2))
- Bootstrapper target-platform test (windows/amd64) = Success ((3))
- Bootstrapper platform-build release (exe/windows/amd64) = Success ((4))
<br><br>
- Work on main launcher = Complete ((5))
- Launcher development-platform test (ubuntu/aarch64) = Success ((6))
- Launcher target-platform test (windows/amd64) = Success ((7))
- Launcher target-build release (exe/windows/amd64) = Success ((8))

## Development Target

- Windows OS (7 and up) are the target platforms.
- Imported/Native code is recommended to be cross platform or atleast support (linux/aarch64).
- Build target is amd64.
- Python 3.10.6 64-bit must be used.
- PyQt5 v5.15.6 must be used.
- PyInstaller to build executable must be used.

## Execution

- Ensure Python 3.10.6 64-bit is installed.
- `git clone` OR download this repository and set repo root to working directory.
- Install modules. `python -m pip install -r requirements.txt`
- Run the script. `python ./bootstrapper/main.py` (Bootstrapper) or `python ./launcher/main.py` (Launcher) or `python ./server/bot.py` (Skin Server Bot)
- If background image/fonts do not load, check working directory (must be the root folder, not the `bootstrapper`/`launcher` folder.) OR modify code to point to the files correctly.

## Developers
- [**Zukashi**](https://github.com/zukashix)
- [**Braxton Elmer**](https://github.com/BraxtonElmer)
