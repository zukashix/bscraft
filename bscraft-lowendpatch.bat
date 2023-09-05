@echo off
title BSCraft Low End Patcher
echo Patching BSCraft...
echo This patch will make the game look awful. The main menu will be restored to minecraft default, animations and shader support will be removed.
echo It is not recommended to use this unless the game is literally unplayable.

REM del /F /Q %appdata%\.bscraft\modpack\mods\QOL_MobPlaques-v4.0.1-1.19.2-Forge.jar
REM del /F /Q %appdata%\.bscraft\modpack\mods\QOL_illuminations-forge-1.19.2-1.10.9.20.jar
REM del /F /Q %appdata%\.bscraft\modpack\mods\QOL_appleskin-forge-mc1.19-2.4.2.jar
del /F /Q %appdata%\.bscraft\modpack\mods\CL-QOL_notenoughanimations-forge-1.6.2-mc1.19.2.jar
del /F /Q %appdata%\.bscraft\modpack\mods\CL-QOL_soundphysics-forge-1.19.2-1.0.18.jar
del /F /Q %appdata%\.bscraft\modpack\mods\CL-QOL_invhud.forge.1.19-3.4.7.jar
del /F /Q %appdata%\.bscraft\modpack\mods\CL-QOL_effective_fg-1.3.4.jar
del /F /Q %appdata%\.bscraft\modpack\mods\CL-QOL_AmbientSounds_FORGE_v5.2.13_mc1.19.2.jar
del /F /Q %appdata%\.bscraft\modpack\mods\CL-QOL_BetterAnimationsCollection-v4.0.5-1.19.2-Forge.jar
del /F /Q %appdata%\.bscraft\modpack\mods\CL-QOL_3dskinlayers-forge-1.5.2-mc1.19.1.jar
del /F /Q %appdata%\.bscraft\modpack\mods\CL-BASE_oculus-mc1.19.2-1.6.4.jar
del /F /Q %appdata%\.bscraft\modpack\mods\CL-BASE_FpsReducer2-forge-1.19.2-2.1.jar
del /F /Q %appdata%\.bscraft\modpack\mods\CL-BASE_fancymenu_forge_2.14.9_MC_1.19-1.19.2.jar
del /F /Q %appdata%\.bscraft\modpack\mods\CL-BASE_farsight-1.19.2-2.1.jar

echo If you did not see any errors above, the patch was successfully applied. If you saw errors, please run script as administrator.
echo NOTE: This patch does not guarantee that your fps will absolutely skyrocket. You should gain some improvements though.
echo If your PC does not meet the recommended to requirements to run vanilla minecraft either, please dont expect better performance on BSCraft.