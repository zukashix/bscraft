# BSCraft Launcher

Source for BSCraft 3.0 Launcher & Bootstrapper <br>
BSCraft is a vanilla+ lightweight minecraft modpack 

## For Players
- If you are a player wanting to download and play BSCraft, please head over to the "[**Releases**](https://github.com/zukashix/bscraft/releases/tag/BootstrapperMain)" page and download the latest application.

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
- Python 3.8.10 64-bit must be used.
- PyQt5 v5.15.6 must be used.
- PyInstaller to build executable must be used.

## Execution

- Ensure Python 3.10.6 64-bit is installed.
- `git clone` OR download this repository and set repo root to working directory.
- Install modules. `python -m pip install -r requirements.txt`
- Build resources file (pre-built but rebuilding will be needed if any changes made to QRC) `pyrcc5 resources.qrc -o resources.py`
- Copy `resources.py` generated to `./bootstrapper/modules/resources.py` and `./launcher/modules/resources.py`
- Run the script. `python ./bootstrapper/main.py` (Bootstrapper) or `python ./launcher/main.py` (Launcher)
- Compile to EXEs for Windows using commands provided in `./pyinstallerCmd.txt`

## Developers
- [**Zukashi**](https://github.com/zukashix)
- [**Braxton Elmer**](https://github.com/BraxtonElmer)
