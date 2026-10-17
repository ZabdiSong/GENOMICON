# Revision notes

## Materials reviewed

- `Genomicon_final(2).py`: 694 lines; selected as the working version.
- `Genomicon1(1).1`: 216 lines of Python; read in full as an earlier reference.

Neither file is an archive. No ZIP or image files were supplied with this request. The earlier version contains placeholder screens; it has not been merged into or substituted for the final game. The uploaded originals have not been overwritten.

## Changes made

- Added a module overview, numbered section comments and documentation for all twelve functions.
- Clarified displayed English, including Punnett spelling, the cut/insert instruction, and the phenotype-ratio prompt. The full wording comparison is in `TEXT_CHANGES.md`.
- Added a launcher and a standard-library asset checker, alongside setup and upload documentation.

## Preserved

- Original 900 × 600 window, colors, button rectangles, image scaling and positions.
- Original asset filenames and slide/gallery order.
- Punnett-square computation, parent options, phenotype counts and fur-image selection.
- Original cut/insert steps, explanatory slides and reset behavior.
- Accepted Level 3 answer and existing keyboard/mouse input rules.
- Existing navigation/state transitions, manual milestones and session-only progress.

## Verification

- All three Python files compile.
- After removing docstrings and reversing only the documented displayed-text edits, the revised game has the same Python abstract syntax tree as the original. This checks every executable statement, calculation, branch, state assignment and UI value.
- All nine combinations of `BB`, `Bb` and `bb` produce the expected offspring counts. `Bb × Bb` produces one `BB`, two `Bb` and one `bb`, with a 3:1 blue:red phenotype ratio.
- All 66 image paths in the checker match those referenced by the final game.
- The asset checker identifies missing files and invalid PNG signatures.
- Launching from a different working directory produces a clear missing-artwork message without requiring Pygame.

Full Pygame playback and visual comparison were **not** run: the original artwork is absent, and Pygame is not installed in the review environment. PNG signature checks do not substitute for full image decoding or visual review.

## Existing details kept at the requested scope

- The first Level 3 input starts with a space. Mouse Submit compares exact input, while Enter trims spaces. Leaving Level 3 clears its input.
- Library and Milestone update a shared Back-button rectangle that the level menu also uses.
- The original gallery's final thumbnail row overlaps part of its Back-button area. Expanding every library section can push lower definitions beyond the window.

These follow directly from the supplied coordinates and input code. They have been documented rather than changing the requested design or behavior.
