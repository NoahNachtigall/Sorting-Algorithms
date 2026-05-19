# Bubble Sort Visualization with Dynamic Sounds
# pip install pygame numpy

import time
import random
import pygame
import numpy as np

# -------------------- PYGAME SETUP --------------------
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)

# -------------------- WINDOW --------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bubble Sort Visualization")

clock = pygame.time.Clock()

# -------------------- SETTINGS --------------------
ARRAY_SIZE = 100

BAR_WIDTH = SCREEN_WIDTH / ARRAY_SIZE
HEIGHT_MULTIPLIER = SCREEN_HEIGHT / ARRAY_SIZE

# -------------------- COLORS --------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# -------------------- ARRAY --------------------
def generate_array():
    nums = list(range(1, ARRAY_SIZE + 1))
    random.shuffle(nums)
    return nums

nums = generate_array()

# -------------------- SORT VARIABLES --------------------
sorting = False
done = False

index = len(nums) - 1
j = 0

# -------------------- SOUND --------------------
def play_tone(frequency, duration=0.015, volume=0.08):

    sample_rate = 44100

    t = np.linspace(
        0,
        duration,
        int(sample_rate * duration),
        False
    )

    wave = np.sin(frequency * 2 * np.pi * t)

    audio = wave * (2**15 - 1) * volume

    # stereo
    audio = np.column_stack((audio, audio))

    audio = audio.astype(np.int16)

    sound = pygame.sndarray.make_sound(audio)

    sound.play()

# -------------------- RESET --------------------
def reset():

    global nums
    global sorting
    global done
    global index
    global j

    nums = generate_array()

    sorting = False
    done = False

    index = len(nums) - 1
    j = 0

# -------------------- FINISH ANIMATION --------------------
def finish_animation():

    for i in range(len(nums)):

        freq = 200 + nums[i] * 10
        play_tone(freq)

        window.fill(BLACK)

        for x in range(len(nums)):

            color = GREEN if x <= i else WHITE

            pygame.draw.rect(
                window,
                color,
                (
                    x * BAR_WIDTH,
                    SCREEN_HEIGHT - nums[x] * HEIGHT_MULTIPLIER,
                    BAR_WIDTH,
                    nums[x] * HEIGHT_MULTIPLIER
                )
            )

        pygame.display.flip()

        pygame.time.delay(10)

# -------------------- MAIN LOOP --------------------
running = True

while running:

    clock.tick(120)

    # -------------------- EVENTS --------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # START SORT
            if event.key == pygame.K_SPACE and not sorting and not done:

                start = time.perf_counter()
                sorting = True

            # RESET
            if event.key == pygame.K_r:

                reset()

    # -------------------- DRAW BACKGROUND --------------------
    window.fill(BLACK)

    # -------------------- SORTING --------------------
    if sorting:

        # comparison tone
        freq = 200 + nums[j] * 8
        play_tone(freq)

        if nums[j] > nums[j + 1]:

            # swap sound
            play_tone(300 + nums[j] * 8)

            nums[j], nums[j + 1] = nums[j + 1], nums[j]

        j += 1

        # end of one pass
        if j >= index:

            j = 0
            index -= 1

        # sorting finished
        if index <= 0:

            sorting = False
            done = True

            end = time.perf_counter()

            print(nums)
            print(f"Sorting time: {end - start:.6f} seconds")

            finish_animation()

    # -------------------- DRAW BARS --------------------
    for i in range(len(nums)):

        if done:
            color = GREEN

        elif i == j:
            color = RED

        elif i == j + 1:
            color = GREEN

        else:
            color = WHITE

        pygame.draw.rect(
            window,
            color,
            (
                i * BAR_WIDTH,
                SCREEN_HEIGHT - nums[i] * HEIGHT_MULTIPLIER,
                BAR_WIDTH,
                nums[i] * HEIGHT_MULTIPLIER
            )
        )

    pygame.display.flip()

pygame.quit()