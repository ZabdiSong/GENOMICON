"""Launch the unchanged game flow from any working directory."""

import importlib.util
import os
from pathlib import Path
import runpy

from check_assets import STARTUP_ASSETS, inspect_assets

ROOT = Path(__file__).resolve().parent


def main():
    """Explain setup problems before handing control to the original game."""
    missing, invalid = inspect_assets(ROOT)
    startup_problems = [path for path in STARTUP_ASSETS if path in missing or path in invalid]
    if startup_problems:
        print("GENOMICON needs the original artwork before it can start:")
        for path in startup_problems:
            print(f"  {path}")
        print("\nCopy the original assets/ folder beside genomicon.py.")
        print("Run python check_assets.py for the complete list of 66 image references.")
        return 2

    if importlib.util.find_spec("pygame") is None:
        print("Pygame is not installed in this Python environment.")
        print("From the project folder, run: python -m pip install -r requirements.txt")
        return 2

    if missing or invalid:
        print(f"Some lesson/gallery images are unavailable ({len(missing) + len(invalid)}).")
        print("The original in-game image-not-found messages will be used.")
        print("Run python check_assets.py to list the affected paths.")

    # The original program uses relative paths. Set the folder only at launch;
    # no game function, path literal or event rule needs to change.
    os.chdir(ROOT)
    runpy.run_path(str(ROOT / "genomicon.py"), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
