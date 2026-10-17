# Original image inventory

The final program references **66 PNG files**. Neither supplied attachment contains image bytes. Preserve spelling and capitalization when adding the original files.

## Required at startup — 7 images

The original program loads all seven before opening its menu:

- `assets/blue_fur.png`
- `assets/pink_fur.png`
- `assets/both_fur.png`
- `assets/images/gebackground.png`
- `assets/medal1.png`
- `assets/medal2.png`
- `assets/medal3.png`

## Level 1 explanation — 28 images

`assets/1.png` through `assets/28.png`, inclusive.

## Level 2 introduction — 12 images

The original order is:

1. `assets/1_1.png`
2. `assets/2_2.png`
3. `assets/3_2.png`
4. `assets/4_1.png`
5. `assets/5_1.png`
6. `assets/6_1.png`
7. `assets/7_1.png`
8. `assets/8_1.png`
9. `assets/9_1.png`
10. `assets/10_1.png`
11. `assets/11_1.png`
12. `assets/12_1.png`

## Level 2 activity explanations — 2 images

- `assets/1_2.png`: cutting explanation.
- `assets/2_3.png`: insertion explanation.

## Level 3 question — 1 image

- `assets/level3.png`

## Gallery — 16 images

`assets/gallery/1.png` through `assets/gallery/16.png`, inclusive.

## Check the folder

```sh
python check_assets.py
```

The checker examines filenames and the standard PNG signature. It does not fully decode or visually inspect the images. Pygame playback should be checked after all original files are restored.
