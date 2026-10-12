\
import os
import sys
import subprocess
from pathlib import Path
import webview

APP_NAME = "TableFlow Restaurant POS"

def resource_path(name: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / name

def install_dir() -> Path:
    return Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent

def start_print_agent() -> None:
    folder = install_dir()
    agent = folder / "TableFlowPrintAgent.exe"
    if agent.exists():
        try:
            subprocess.Popen([str(agent)], cwd=str(folder), creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except Exception:
            pass

class WindowApi:
    def minimize_window(self):
        try:
            if webview.windows:
                webview.windows[0].minimize()
                return True
        except Exception:
            pass
        return False

    def close_window(self):
        try:
            if webview.windows:
                webview.windows[0].destroy()
                return True
        except Exception:
            pass
        return False

def main() -> None:
    html = resource_path("index.html")
    if not html.exists():
        raise FileNotFoundError(f"POS interface not found: {html}")
    start_print_agent()
    webview.create_window(
        APP_NAME,
        html.as_uri(),
        fullscreen=True,
        frameless=True,
        resizable=True,
        text_select=True,
        confirm_close=True,
        js_api=WindowApi(),
    )
    webview.start(gui="edgechromium", debug=False)

if __name__ == "__main__":
    main()
