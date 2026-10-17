"""GENOMICON — the original three-activity Pygame genetics game.

Start with ``python run.py`` so assets are resolved relative to this folder.
This readability revision adds comments, docstrings and English copy edits.
Its original calculations, event flow, state updates and UI geometry remain.

Code guide:
    Session state and lesson content -> inheritance logic -> click targets
    -> draw_* functions -> event loop.
"""

import pygame
import sys
from collections import Counter

pygame.init()

# 1. STARTUP ASSETS — required images, with the original sizes and paths
blue_fur = pygame.transform.scale(pygame.image.load("assets/blue_fur.png"), (100, 100))
red_fur = pygame.transform.scale(pygame.image.load("assets/pink_fur.png"), (100, 100))
both_fur = pygame.transform.scale(pygame.image.load("assets/both_fur.png"), (140, 70))
background = pygame.transform.scale(pygame.image.load("assets/images/gebackground.png"), (900, 600))
gallery_images = [f"assets/gallery/{i}.png" for i in range(1, 17)]
thumbnail_size = (150, 100)

medal_img1 = pygame.transform.scale(pygame.image.load("assets/medal1.png"), (250, 250))
medal_img2 = pygame.transform.scale(pygame.image.load("assets/medal2.png"), (250, 250))
medal_img3 = pygame.transform.scale(pygame.image.load("assets/medal3.png"), (250, 250))

in_slideshow = False
slideshow_index = None


# 2. WINDOW AND TEXT — original 900 x 600 layout
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Genomicon - Your First Book About Genome!")
font = pygame.font.SysFont(None, 32)

# Original interface colors
WHITE = (255, 255, 255)
BLUE = (100, 200, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# 3. SESSION STATE — screens, parent choices and gene-editing steps
current_screen = "main"
selected_p1 = None
selected_p2 = None
genotypes = None
phenotypes = None
gene_cut = False
gene_inserted = False
gallery_buttons = {}
show_level2_slide = None

# 4. LESSON CONTENT — original text/image order for Levels 1 and 2
intro_slides_map = {
    "level1": [
        {"type": "text", "content": "Welcome to Genomicon!"},
        {"type": "text", "content": "Explore how genes determine traits."},
        {"type": "text", "content": "Let's get started!"},
        {"type": "text", "content": "1. The Punnett Square"},
        {"type": "text", "content": "I would like you to first think of a question."},
        {"type": "text", "content": "Where do your characteristics come from?"},
        {"type": "text", "content": "The answer is simple."},
        {"type": "text", "content": "Although environment also affects our phenotype,"},
        {"type": "text", "content": "Many traits are inherited from our parents."},
        {"type": "text", "content": "A Punnett square is a tool"},
        {"type": "text", "content": "for predicting offspring genotypes and phenotypes."},
        {"type": "text", "content": "Let me give you an example."},
        {"type": "image", "content": "assets/1.png"},
        {"type": "image", "content": "assets/2.png"},
        {"type": "image", "content": "assets/3.png"},
        {"type": "image", "content": "assets/4.png"},
        {"type": "image", "content": "assets/5.png"},
        {"type": "image", "content": "assets/6.png"},
        {"type": "image", "content": "assets/7.png"},
        {"type": "image", "content": "assets/8.png"},
        {"type": "image", "content": "assets/9.png"},
        {"type": "image", "content": "assets/10.png"},
        {"type": "image", "content": "assets/11.png"},
        {"type": "image", "content": "assets/12.png"},
        {"type": "image", "content": "assets/13.png"},
        {"type": "image", "content": "assets/14.png"},
        {"type": "image", "content": "assets/15.png"},
        {"type": "image", "content": "assets/16.png"},
        {"type": "image", "content": "assets/17.png"},
        {"type": "image", "content": "assets/18.png"},
        {"type": "image", "content": "assets/19.png"},
        {"type": "image", "content": "assets/20.png"},
        {"type": "image", "content": "assets/21.png"},
        {"type": "image", "content": "assets/22.png"},
        {"type": "image", "content": "assets/23.png"},
        {"type": "image", "content": "assets/24.png"},
        {"type": "image", "content": "assets/25.png"},
        {"type": "image", "content": "assets/26.png"},
        {"type": "image", "content": "assets/27.png"},
        {"type": "image", "content": "assets/28.png"},
        {"type": "text", "content": "Blue fur is dominant; red fur is recessive."},
    ],
    "level2": [
        {"type": "text", "content": "Welcome to the Gene Editing Lab."},
        {"type": "text", "content": "In this level, you will simulate editing DNA!"},
        {"type": "image", "content": "assets/1_1.png"},
        {"type": "image", "content": "assets/2_2.png"},
        {"type": "image", "content": "assets/3_2.png"},
        {"type": "image", "content": "assets/4_1.png"},
        {"type": "image", "content": "assets/5_1.png"},
        {"type": "image", "content": "assets/6_1.png"},
        {"type": "image", "content": "assets/7_1.png"},
        {"type": "image", "content": "assets/8_1.png"},
        {"type": "image", "content": "assets/9_1.png"},
        {"type": "image", "content": "assets/10_1.png"},
        {"type": "image", "content": "assets/11_1.png"},
        {"type": "image", "content": "assets/12_1.png"},
        {"type": "text", "content": "Now it's your turn!"},
        {"type": "text", "content": "Use the buttons, then explain each step to a friend."},
    ]
}
current_slide_index = 0
current_level_target = None
skip_button = pygame.Rect(750, 20, 100, 40)
level2_intro_index = 0
skip_button2 = pygame.Rect(750, 20, 100, 40)
input_box = pygame.Rect(350, 400, 200, 40)
user_input = " "
feedback_message = " "
active_input = False
answer = "9:3:3:1"
# Answer and whitespace-handling rules are intentionally unchanged.

# 5. REFERENCE LIBRARY — expandable topic groups
library_sections = {
    "DNA & Genes": {
        "Gene": "A segment of DNA that codes for a specific protein.",
        "DNA": "Carries genetic instructions in living organisms.",
        "Chromosome": "Tightly coiled DNA and proteins, carrying genetic information.",
        "Nucleotide": "The basic building block of DNA.",
        "Double Helix": "The twisted-ladder structure of DNA.",
        "Genome": "The complete set of genetic material in an organism.",
    },
    "Inheritance":{
        "Dominant": "Dominant alleles mask recessive alleles in this model.",
        "Recessive": "A recessive trait appears when both alleles are recessive.",
        "Punnett Square": "A diagram predicting the probability of offspring genotypes."
    },
    "Gene Editing & Evolution":{
        "CRISPR": "A revolutionary gene-editing tool that allows DNA modifications.",
        "Mutation": "A permanent alteration in the DNA sequence.",
        "Natural Selection": "Advantageous traits become common."
    }
}

expanded_sections = {section: False for section in library_sections}
section_button_rects = {}

# 6. INHERITANCE CALCULATION — the original complete-dominance rule
def punnett_square(parent1, parent2):
    """Return four equally weighted offspring outcomes for two parents.

    Parents are BB, Bb or bb. Sorting normalizes bB to Bb. The complete-
    dominance model treats every genotype containing B as blue fur.
    """
    offspring = [a + b for a in parent1 for b in parent2]
    normalized = [''.join(sorted(child)) for child in offspring]
    genotype_counts = Counter(normalized)
    phenotype_counts = {
        'Blue Fur': sum(v for k, v in genotype_counts.items() if 'B' in k),
        'Red Fur': genotype_counts.get('bb', 0)
    }
    return genotype_counts, phenotype_counts

# 7. CLICK TARGETS — all coordinates and dimensions are unchanged
main_buttons = {
    "New Game": pygame.Rect(50, 500, 150, 50),
    "Library": pygame.Rect(250, 500, 150, 50),
    "Gallery": pygame.Rect(450, 500, 150, 50),
    "Milestone": pygame.Rect(650, 500, 150, 50)
}

level_select_buttons = {
    "Level 1": pygame.Rect(400, 200, 150, 50),
    "Level 2": pygame.Rect(400, 270, 150, 50),
    "Level 3": pygame.Rect(400, 340, 150, 50),
    "Back": pygame.Rect(400, 420, 150, 40)
}

level1_buttons = {}
for i, allele in enumerate(["BB", "Bb", "bb"]):
    level1_buttons[f"P1_{allele}"] = pygame.Rect(100, 100 + i * 60, 100, 40)
    level1_buttons[f"P2_{allele}"] = pygame.Rect(700, 100 + i * 60, 100, 40)
level1_buttons["Back"] = pygame.Rect(400, 520, 150, 40)

level2_buttons = {
    "DNA": pygame.Rect(300, 200, 300, 60),
    "Insert": pygame.Rect(300, 300, 300, 60),
    "Back" : pygame.Rect(400, 500, 150, 40)
}

level3_buttons = {
    "Submit": pygame.Rect(250, 500, 150, 50),
    "Back": pygame.Rect(450, 500, 150, 50),
}

# 8. MANUAL MILESTONES — session-only self-assessment
milestone_texts = {
    "Level 1": "I understand how a Punnett square works.",
    "Level 2": "I understand how gene editing works.",
    "Level 3": "I understand how to analyze ratios."
}

milestone_status = {
    "Level 1": False,
    "Level 2": False,
    "Level 3": False
}

milestone_buttons = {
    "Level 1": pygame.Rect(100, 420, 200, 50),
    "Level 2": pygame.Rect(350, 420, 200, 50),
    "Level 3": pygame.Rect(600, 420, 200, 50)
}

checkbox_rects = {
    "Level 1": pygame.Rect(160, 500, 20, 20),
    "Level 2": pygame.Rect(410, 500, 20, 20),
    "Level 3": pygame.Rect(660, 500, 20, 20)
}

milestone_selected = None


# 9. SCREEN DRAWING FUNCTIONS
def draw_main_screen():
    """Draw the original background, title and four main-menu buttons."""
    screen.blit(background, (0, 0))
    title = font.render("Your First Book About Genome!", True, BLACK)
    screen.blit(title, (250, 30))
    for label, rect in main_buttons.items():
        pygame.draw.rect(screen, WHITE, rect)
        screen.blit(font.render(label, True, BLACK), (rect.x + 20, rect.y + 10))

# New Game menu
def draw_new_game_menu():
    """Draw the three level choices and the existing Back button."""
    screen.fill(WHITE)
    title = font.render("Select a Level", True, BLACK)
    screen.blit(title, (340, 120))
    for label, rect in level_select_buttons.items():
        pygame.draw.rect(screen, BLUE, rect)
        screen.blit(font.render(label, True, BLACK), (rect.x + 10, rect.y + 10))

# Intro slides
def draw_intro_slides():
    """Draw the current text/image slide and its click/Skip controls."""
    screen.fill(WHITE)
    slides = intro_slides_map.get(current_level_target, [])
    if current_slide_index < len(slides):
        slide = slides[current_slide_index]
        if slide["type"] == "text":
            text = font.render(slide["content"], True, BLACK)
            rect = text.get_rect(center=(450, 300))
            screen.blit(text, rect)
        elif slide["type"] == "image":
            try:
                image = pygame.image.load(slide["content"])
                image = pygame.transform.scale(image, (900, 600))  # adjust as needed
                screen.blit(image, (0, 0))
            except:
                screen.blit(font.render("Image not found", True, BLACK), (350, 300))
        screen.blit(font.render("Click to continue...", True, GRAY), (350, 550))

    pygame.draw.rect(screen, GRAY, skip_button)
    screen.blit(font.render("Skip", True, BLACK), (skip_button.x + 20, skip_button.y + 10))

# Level 1 — choose two parent genotypes and view the cross
def draw_level1():
    """Draw parent selections, offspring counts and the fur illustration."""
    global genotypes, phenotypes
    screen.fill(WHITE)
    screen.blit(font.render("Predicted offspring:", True, BLACK), (300, 40))

    for label in ["P1_BB", "P1_Bb", "P1_bb"]:
        rect = level1_buttons[label]
        allele = label.split("_")[1]
        color = (50, 180, 255) if selected_p1 == allele else BLUE
        pygame.draw.rect(screen, color, rect)
        screen.blit(font.render(f"{allele}", True, BLACK), (rect.x + 10, rect.y + 10))

    for label in ["P2_BB", "P2_Bb", "P2_bb"]:
        rect = level1_buttons[label]
        allele = label.split("_")[1]
        color = (50, 180, 255) if selected_p2 == allele else BLUE
        pygame.draw.rect(screen, color, rect)
        screen.blit(font.render(f"{allele}", True, BLACK), (rect.x + 10, rect.y + 10))

    if genotypes and phenotypes:
        y = 300
        screen.blit(font.render("Results:", True, BLACK), (350, y))
        y += 30
        for g, v in genotypes.items():
            screen.blit(font.render(f"{g}: {v}", True, BLACK), (350, y))
            y += 30
        for p, v in phenotypes.items():
            screen.blit(font.render(f"{p}: {v}", True, BLACK), (350, y))
            y += 30

        if phenotypes['Blue Fur'] > 0 and phenotypes['Red Fur'] > 0:
            img = both_fur
            screen.blit(img, (400, 100))
        elif phenotypes["Blue Fur"] > 0 and phenotypes["Red Fur"] == 0:
            img = blue_fur
            screen.blit(img, (400, 100))
        elif phenotypes["Red Fur"] > 0 and phenotypes["Blue Fur"] == 0:
            img = red_fur
            screen.blit(img, (400, 100))

    back = level1_buttons["Back"]
    pygame.draw.rect(screen, GRAY, back)
    screen.blit(font.render("Back", True, BLACK), (back.x + 10, back.y + 10))

# Level 2 — cut DNA, read the slide, then insert a gene
def draw_level2():
    """Show the cut/insert simulation using the two existing state flags."""
    global gene_cut, gene_inserted
    screen.fill(WHITE)
    title = font.render("Level 2: Gene Editing Simulation", True, BLACK)
    screen.blit(title, (250, 30))

    instructions = "Click Original DNA, then Insert Gene Here."
    screen.blit(font.render(instructions, True, BLACK), (180, 80))

    pygame.draw.rect(screen, BLUE if not gene_cut else GRAY, level2_buttons["DNA"])
    screen.blit(font.render("Original DNA", True, BLACK), (level2_buttons["DNA"].x + 70, level2_buttons["DNA"].y + 20))

    if gene_cut:
        pygame.draw.rect(screen, BLUE if not gene_inserted else GRAY, level2_buttons["Insert"])
        screen.blit(font.render("Insert Gene Here", True, BLACK), (level2_buttons["Insert"].x + 50, level2_buttons["Insert"].y + 20))

    if gene_inserted:
        screen.blit(font.render("Simulation complete: DNA edited!", True, (0, 150, 0)), (220, 400))

    pygame.draw.rect(screen, GRAY, level2_buttons["Back"])
    screen.blit(font.render("Back", True, BLACK), (level2_buttons["Back"].x + 10, level2_buttons["Back"].y + 10))

# Level 2 cutting explanation
def draw_level2_slide1():
    """Show the cutting explanation and return its Back-button rectangle."""
    screen.fill(WHITE)
    try:
        image = pygame.image.load("assets/1_2.png")
        image = pygame.transform.scale(image, (800, 500))
        screen.blit(image, (50, 50))
    except:
        screen.blit(font.render("Slide 1 not found", True, (255, 0, 0)), (350, 300))

    back_btn = pygame.Rect(750, 20, 120, 40)
    pygame.draw.rect(screen, GRAY, back_btn)
    screen.blit(font.render("Back", True, BLACK), (back_btn.x + 20, back_btn.y + 10))
    return back_btn

# Level 2 insertion explanation
def draw_level2_slide2():
    """Show the insertion explanation and return its Back-button rectangle."""
    screen.fill(WHITE)
    try:
        image = pygame.image.load("assets/2_3.png")
        image = pygame.transform.scale(image, (800, 500))
        screen.blit(image, (50, 50))
    except:
        screen.blit(font.render("Slide 2 not found", True, (255, 0, 0)), (350, 300))

    back_btn = pygame.Rect(750, 20, 120, 40)
    pygame.draw.rect(screen, GRAY, back_btn)
    screen.blit(font.render("Back", True, BLACK), (back_btn.x + 20, back_btn.y + 10))
    return back_btn

# Level 3 — enter the phenotype ratio shown in the supplied image
def draw_level3():
    """Draw the ratio image, text input, answer feedback and buttons."""
    screen.fill(WHITE)

    # Image
    try:
        img = pygame.image.load("assets/level3.png")
        img = pygame.transform.scale(img, (300, 200))
        screen.blit(img, (300, 150))
    except:
        screen.blit(font.render("Image not found", True, (255, 0, 0)), (300, 100))

    # Title
    title = font.render("Level 3: Solve the ratio question.", True, BLACK)
    screen.blit(title, (250, 30))

    instructions = "Enter the phenotype ratio (e.g., 1:1:1:1)."
    screen.blit(font.render(instructions, True, BLACK), (180, 80))

    pygame.draw.rect(screen, BLUE if active_input else GRAY, input_box)
    input_text = font.render(user_input, True, BLACK)
    screen.blit(input_text, (input_box.x + 5, input_box.y + 5))

    # Buttons
    pygame.draw.rect(screen, BLUE, level3_buttons["Submit"])
    screen.blit(font.render("Submit", True, BLACK), (level3_buttons["Submit"].x + 60, level3_buttons["Submit"].y + 10))

    pygame.draw.rect(screen, BLUE, level3_buttons["Back"])
    screen.blit(font.render("Back", True, BLACK), (level3_buttons["Back"].x + 60, level3_buttons["Back"].y + 10))

    # Feedback
    if feedback_message:
        color = (0, 150, 0) if "Congratulations" in feedback_message else (255, 0, 0)
        feedback = font.render(feedback_message, True, color)
        screen.blit(feedback, (250, 350))

# Library screen — render definitions and update hit regions
def draw_library():
    """Draw expandable definitions and remember their clickable regions.

    This retains the original shared Back-button rectangle assignment.
    """
    global section_button_rects
    section_button_rects = {}
    screen.fill(WHITE)
    screen.blit(font.render("Genetic Library", True, BLACK), (350, 30))
    y_offset = 80

    for section, terms in library_sections.items():
        # Section title
        toggle_rect = pygame.Rect(50, y_offset, 300, 30)
        pygame.draw.rect(screen, GRAY, toggle_rect)
        symbol = "▼" if expanded_sections[section] else "▶"
        screen.blit(font.render(f"{symbol} {section}", True, BLACK), (60, y_offset + 5))

        section_y = y_offset + 40
        if expanded_sections[section]:
            for term, definition in terms.items():
                screen.blit(font.render(f"{term}: {definition}", True, BLACK), (80, section_y))
                section_y += 30

        section_button_rects[section] = toggle_rect
        y_offset = section_y + 10

    # Back button
    back_button = pygame.Rect(760, 550, 120, 40)
    pygame.draw.rect(screen, GRAY, back_button)
    text = font.render("Back", True, BLACK)
    text_rect = text.get_rect(center=back_button.center)
    screen.blit(text, text_rect)

    level_select_buttons["Back"] = back_button

# Gallery — four columns of thumbnails, followed by slideshow controls
def draw_gallery():
    """Draw sixteen thumbnails or the selected image slideshow."""
    global in_slideshow, slideshow_index, gallery_buttons

    screen.fill(WHITE)
    screen.blit(font.render("Gallery", True, BLACK), (370, 20))

    if in_slideshow:
        # slide show
        try:
            img = pygame.image.load(gallery_images[slideshow_index])
            img = pygame.transform.scale(img, (600, 400))
            screen.blit(img, (150, 100))
        except:
            screen.blit(font.render("Image not found", True, (255, 0, 0)), (350, 300))

        # Prev
        prev_rect = pygame.Rect(100, 520, 100, 40)
        pygame.draw.rect(screen, GRAY, prev_rect)
        screen.blit(font.render("Previous", True, BLACK), (prev_rect.x + 10, prev_rect.y + 10))

        # Next button
        next_rect = pygame.Rect(700, 520, 100, 40)
        pygame.draw.rect(screen, GRAY, next_rect)
        screen.blit(font.render("Next", True, BLACK), (next_rect.x + 25, next_rect.y + 10))

        # Back button
        back_rect = pygame.Rect(400, 520, 100, 40)
        pygame.draw.rect(screen, GRAY, back_rect)
        screen.blit(font.render("Back", True, BLACK), (back_rect.x + 25, back_rect.y + 10))

        # Buttons
        gallery_buttons["SlidePrev"] = prev_rect
        gallery_buttons["SlideNext"] = next_rect
        gallery_buttons["SlideBack"] = back_rect

    else:
        gallery_buttons = {}
        for idx, path in enumerate(gallery_images):
            x = 70 + (idx % 4) * 190
            y = 80 + (idx // 4) * 140
            try:
                thumb = pygame.image.load(path)
                thumb = pygame.transform.scale(thumb, thumbnail_size)
                screen.blit(thumb, (x, y))
                rect = pygame.Rect(x, y, *thumbnail_size)
                gallery_buttons[f"Thumb_{idx}"] = rect
            except:
                screen.blit(font.render("?", True, BLACK), (x + 20, y + 40))

        # Back button
        back_rect = pygame.Rect(400, 520, 100, 40)
        pygame.draw.rect(screen, GRAY, back_rect)
        screen.blit(font.render("Back", True, BLACK), (back_rect.x + 25, back_rect.y + 10))
        gallery_buttons["GalleryBack"] = back_rect

# Milestones — checkboxes are controlled by the player
def draw_milestone():
    """Draw manually toggled checkboxes, medals and selected statements."""
    screen.fill(WHITE)
    screen.blit(font.render("Milestones", True, BLACK), (370, 30))

    for level, rect in milestone_buttons.items():
        pygame.draw.rect(screen, BLUE, rect)
        screen.blit(font.render(level, True, BLACK), (rect.x + 50, rect.y + 10))

        # checkbox
        checkbox = checkbox_rects[level]
        pygame.draw.rect(screen, WHITE, checkbox)
        pygame.draw.rect(screen, BLACK, checkbox, 2)
        if milestone_status[level]:
            pygame.draw.line(screen, BLACK, (checkbox.x, checkbox.y), (checkbox.x+20, checkbox.y+20), 3)
            pygame.draw.line(screen, BLACK, (checkbox.x+20, checkbox.y), (checkbox.x, checkbox.y+20), 3)

            # medals
            if level == "Level 1":
                screen.blit(medal_img1, (rect.x + 1, rect.y - 320))
            elif level == "Level 2":
                screen.blit(medal_img2, (rect.x + 1, rect.y - 320))
            elif level == "Level 3":
                screen.blit(medal_img3, (rect.x + 1, rect.y - 320))

    # text show
    if milestone_selected:
        sentence = milestone_texts[milestone_selected]
        screen.blit(font.render(sentence, True, BLACK), (200, 380))

    # Back button
    back_rect = pygame.Rect(750, 520, 100, 40)
    pygame.draw.rect(screen, GRAY, back_rect)
    screen.blit(font.render("Back", True, BLACK), (back_rect.x + 25, back_rect.y + 10))
    level_select_buttons["Back"] = back_rect



# 10. GAME LOOP — draw the active screen, process input, refresh the display
running = True
# Drawing precedes event handling, matching the original frame order.
while running:
    if current_screen == "main":
        draw_main_screen()
    elif current_screen == "new_game":
        draw_new_game_menu()
    elif current_screen == "intro":
        draw_intro_slides()
    elif current_screen == "level1":
        draw_level1()
    elif current_screen == "level2":
        if show_level2_slide == "slide1":
            slide1_back_btn = draw_level2_slide1()
        elif show_level2_slide == "slide2":
            slide2_back_btn = draw_level2_slide2()
        else:
            draw_level2()
    elif current_screen == "level3":
        draw_level3()
    elif current_screen == "library":
        draw_library()
    elif current_screen == "gallery":
        draw_gallery()
    elif current_screen == "milestone":
        draw_milestone()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            # main
            if current_screen == "main":
                for label, rect in main_buttons.items():
                    if rect.collidepoint(pos):
                        if label == "New Game":
                            current_screen = "new_game"
                        else:
                            current_screen = label.lower()
            # Library
            elif current_screen == "library":
                for section, rect in section_button_rects.items():
                    if rect.collidepoint(pos):
                            expanded_sections[section] = not expanded_sections[section]

                if level_select_buttons["Back"].collidepoint(pos):
                        current_screen = "main"

            # Gallery
            elif current_screen == "gallery":
                if in_slideshow:
                    if "SlidePrev" in gallery_buttons and gallery_buttons["SlidePrev"].collidepoint(pos):
                       slideshow_index = (slideshow_index - 1) % len(gallery_images)
                    elif "SlideNext" in gallery_buttons and gallery_buttons["SlideNext"].collidepoint(pos):
                       slideshow_index = (slideshow_index + 1) % len(gallery_images)
                    elif "SlideBack" in gallery_buttons and gallery_buttons["SlideBack"].collidepoint(pos):
                       in_slideshow = False
                else:
                    for key, rect in gallery_buttons.items():
                        if key.startswith("Thumb_") and rect.collidepoint(pos):
                            slideshow_index = int(key.split("_")[1])
                            in_slideshow = True
                    if "GalleryBack" in gallery_buttons and gallery_buttons["GalleryBack"].collidepoint(pos):
                        current_screen = "main"

            # Milestone
            elif current_screen == "milestone":
                for level, rect in milestone_buttons.items():
                    if rect.collidepoint(pos):
                        milestone_selected = level

                for level, checkbox in checkbox_rects.items():
                    if checkbox.collidepoint(pos):
                        milestone_status[level] = not milestone_status[level]

                if level_select_buttons["Back"].collidepoint(pos):
                    current_screen = "main"

            # new game
            elif current_screen == "new_game":
                for label, rect in level_select_buttons.items():
                    if rect.collidepoint(pos):
                        if label == "Back":
                            current_screen = "main"
                        else:
                            current_level_target = label.lower().replace(" ", "")
                            current_slide_index = 0
                            if current_level_target in intro_slides_map:
                                current_screen = "intro"
                            else:
                                current_screen = current_level_target
            # level2
            elif current_screen == "level2":
                if show_level2_slide == "slide1":
                    if slide1_back_btn.collidepoint(pos):
                        show_level2_slide = None
                        gene_cut = True
                elif show_level2_slide == "slide2":
                    if slide2_back_btn.collidepoint(pos):
                        show_level2_slide = None
                        gene_inserted = True
                else:
                    if level2_buttons["DNA"].collidepoint(pos) and not gene_cut:
                        show_level2_slide = "slide1"

                    elif level2_buttons["Insert"].collidepoint(pos) and gene_cut and not gene_inserted:
                        show_level2_slide = "slide2"

                    elif level2_buttons["Back"].collidepoint(pos):
                        current_screen = "main"

                        gene_cut = False
                        gene_inserted = False
                        show_level2_slide = False

            # intro
            elif current_screen == "intro":
                if skip_button.collidepoint(pos):
                    current_screen = current_level_target
                    current_slide_index = 0
                elif current_slide_index < len(intro_slides_map[current_level_target]) - 1:
                    current_slide_index += 1
                else:
                    current_screen = current_level_target
                    current_slide_index = 0

            # Level1
            elif current_screen == "level1":
                for label, rect in level1_buttons.items():
                    if rect.collidepoint(pos):
                        if label.startswith("P1_"):
                            selected_p1 = label.split("_")[1]
                        elif label.startswith("P2_"):
                            selected_p2 = label.split("_")[1]
                        elif label == "Back":
                            current_screen = "main"
                            selected_p1 = selected_p2 = None
                            genotypes = phenotypes = None
                if selected_p1 and selected_p2:
                    genotypes, phenotypes = punnett_square(selected_p1, selected_p2)

            # Level3
            elif current_screen == "level3":
                if input_box.collidepoint(pos):
                    active_input = True
                else:
                    active_input = False

                if level3_buttons["Submit"].collidepoint(pos):
                    # Mouse submission keeps the original exact-string comparison.
                    if user_input == answer:
                        feedback_message = "Congratulations! Your ratio is correct!"
                    else:
                        feedback_message = "Try Again!"

                elif level3_buttons["Back"].collidepoint(pos):
                    current_screen = "main"
                    user_input = ""
                    feedback_message = ""
                    active_input = False

        elif event.type == pygame.KEYDOWN and current_screen == "level3":
            if active_input:
                if event.key == pygame.K_RETURN:
                    # Enter submission keeps the original whitespace trimming.
                    if user_input.strip() == answer:
                        feedback_message = "Congratulations! Your ratio is correct!"
                    else:
                        feedback_message = "Try Again!"
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

    pygame.display.flip()

pygame.quit()
sys.exit()
