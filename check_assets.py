"""Check original image filenames and PNG signatures without importing Pygame."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

STARTUP_ASSETS = (
    "assets/blue_fur.png",
    "assets/pink_fur.png",
    "assets/both_fur.png",
    "assets/images/gebackground.png",
    "assets/medal1.png",
    "assets/medal2.png",
    "assets/medal3.png",
)

LEVEL2_INTRO = (
    "assets/1_1.png",
    "assets/2_2.png",
    "assets/3_2.png",
    "assets/4_1.png",
    "assets/5_1.png",
    "assets/6_1.png",
    "assets/7_1.png",
    "assets/8_1.png",
    "assets/9_1.png",
    "assets/10_1.png",
    "assets/11_1.png",
    "assets/12_1.png",
)

ALL_ASSETS = (
    *STARTUP_ASSETS,
    *(f"assets/{i}.png" for i in range(1, 29)),
    *LEVEL2_INTRO,
    "assets/1_2.png",
    "assets/2_3.png",
    "assets/level3.png",
    *(f"assets/gallery/{i}.png" for i in range(1, 17)),
)


def inspect_assets(root=ROOT):
    """Return missing paths and files lacking the expected eight-byte signature.

    A matching signature is only a basic file check, not full image decoding.
    """
    missing = []
    invalid = []
    for relative_path in ALL_ASSETS:
        path = root / relative_path
        if not path.is_file():
            missing.append(relative_path)
            continue
        try:
            with path.open("rb") as image_file:
                valid_signature = image_file.read(8) == PNG_SIGNATURE
        except OSError:
            valid_signature = False
        if not valid_signature:
            invalid.append(relative_path)
    return missing, invalid


def main():
    missing, invalid = inspect_assets()
    print(f"GENOMICON original image references: {len(ALL_ASSETS)}")
    print(f"Missing: {len(missing)}; signature/read problems: {len(invalid)}")
    for label, paths in (("Missing", missing), ("Invalid PNG signature or unreadable", invalid)):
        for path in paths:
            print(f"  {label}: {path}")
    if missing or invalid:
        print("\nAdd the original assets/ folder. See docs/ASSETS.md for exact paths.")
        return 1
    print("All filenames and PNG signatures are present. Pygame playback still needs to be checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
