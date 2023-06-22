# BSCraft Launcher

Source for BSCraft 3.0 Launcher & Bootstrapper <br>
BSCraft is a vanilla+ lightweight minecraft modpack 

## Progress

- Launcher bootstrapper ready. ((1))
- Bootstrapper development-platform test (ubuntu/aarch64) = Success ((2))
- Bootstrapper target-platform test (windows/amd64) = Pending ((3))
- Launcher bootstrapper platform-build release (exe/windows/amd64) = Waiting for (3) ((4))
- Begin work on main launcher = TBA ((5))

## Development Target

- Windows OS (7 and up) are the target platforms.
- Imported/Native code is recommended cross platform or atleast support (linux/aarch64).
- Build target is amd64.
- Python 3.10.6 64-bit must be used.
- PyQt5 v5.15.6 must be used.
- PyInstaller to build executable must be used.

## Execution (Bootstrapper)

- Ensure Python 3.10.6 64-bit is installed.
- `git clone` OR download this repository and set repo root to working directory.
- Install modules. `python -m pip install -r requirements.txt`
- Run the script. `python ./bootstrapper/main.py`
- If background image/fonts do not load, check working directory (must be the root folder, not the `bootstrapper` folder.) OR modify code to point to the files correctly.

## Developers
[**Zukashi**](https://github.com/zukashix)
[**Braxton Elmer**](https://github.com/BraxtonElmer)
