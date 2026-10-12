TABLEFLOW RESTAURANT POS — WINDOWS DESKTOP BUILD

The app_launcher.py uses pywebview with Edge WebView2 and starts in a frameless fullscreen window. It bundles index.html as the register UI and can start the local print agent if the packaged executable is present.

Build steps (Windows):
1. Install Python 3.11 or 3.12 x64.
2. Install dependencies listed/used by BUILD_WINDOWS_SETUP.bat.
3. Run BUILD_WINDOWS_SETUP.bat.
4. Install Inno Setup 6 if needed.
5. Run BUILD_INSTALLER_ONLY.bat to create Setup.exe.
6. Install on a test PC and run the POS checklist.

This build package does not include a prebuilt, Windows-verified Setup.exe. The build must be performed and tested on Windows.
