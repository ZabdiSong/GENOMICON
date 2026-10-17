# GENOMICON

A Pygame genetics learning game with three activities: a Punnett-square cross, a guided gene-editing simulation, and a phenotype-ratio question. The original menu also includes a reference library, an image gallery, and manually selected milestones.

## Package status

The source has been reviewed and clarified. **Original artwork is still needed to run the complete game.** The supplied files were two Python programs, not an asset ZIP. This package contains no substitute artwork.

## Run locally

1. Install Python 3 and extract this project folder.
2. Copy the original `assets/` folder into the project, preserving every filename and subfolder.
3. Open a terminal in the project folder and run:

```sh
python -m pip install -r requirements.txt
python check_assets.py
python run.py
```

On a machine where Python is named `python3`, use `python3` in these commands. `run.py` also works when launched by its full path from another folder.

The game uses one 900 × 600 desktop window. It does not need an account or network connection during play.

## How to play

| Area | Controls and behavior |
| --- | --- |
| New Game | Choose Level 1, 2 or 3. Levels 1 and 2 start with explanatory slides. Click to advance, or click Skip. |
| Level 1 | Choose `BB`, `Bb` or `bb` for each parent. View the four offspring outcomes and blue/red phenotype counts. In this model, `B` is dominant over `b`. |
| Level 2 | Click Original DNA, read the cutting slide, and use its Back button. Click Insert Gene Here, read the insertion slide, and use its Back button. Leaving this activity resets the editing steps, as in the supplied final program. |
| Level 3 | Click the input box, type a ratio, and submit with the button or Enter. Backspace edits text. The supplied question's accepted answer is `9:3:3:1`. |
| Library | Click a topic heading to expand or collapse its definitions. |
| Gallery | Click a thumbnail. Previous and Next cycle through sixteen images; Back returns to the thumbnail view. |
| Milestone | Select a level to read its statement. Toggle its checkbox yourself to show or hide the medal. These are self-assessments, not automatically earned achievements. |
| Exit | Close the window. |

Progress is held in memory for the current session; the original program does not save it to disk. Mouse Submit in Level 3 compares the input exactly; Enter trims surrounding spaces. Type the answer without spaces for consistent results.

## Files

- `genomicon.py`: the clarified final game program, retaining the supplied design and gameplay.
- `run.py`: a launcher that resolves the original asset paths and explains missing setup requirements.
- `check_assets.py`: checks the 66 referenced image paths and their PNG signatures without needing Pygame.
- `requirements.txt`: the original third-party dependency.
- `assets/`: place the original artwork here.
- `docs/ASSETS.md`: exact image inventory.
- `docs/TEXT_CHANGES.md`: each displayed-text edit.
- `docs/REVISION_NOTES.md`: review scope, checks and preserved behavior.
- `docs/GitHub_Upload_ZH.md`: upload and setup instructions in Chinese.

## Review scope

The revision adds comments and function documentation and clarifies English instructions. Calculations, screen coordinates, image sizes, slide order, accepted answers and event/state transitions are retained. Full visual playback has not been verified because the original images are absent.

## Short project description

GENOMICON translates introductory genetics into three interactive activities: Punnett-square inheritance, a guided gene-editing simulation, and phenotype-ratio analysis. Built with Python and Pygame, it combines explanatory slides, a reference library, an image gallery, and self-assessment milestones to let learners explore simplified genetic concepts through direct interaction.
