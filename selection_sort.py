# Selection Sort Visualization with Dynamic Sounds
# pip install pygame numpy

import pygame
import time
import random
import numpy as np

# -------------------- PYGAME --------------------
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)

# -------------------- WINDOW --------------------
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Selection Sort Visualization")

clock = pygame.time.Clock()

# -------------------- COLORS --------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# -------------------- ARRAY --------------------
nums = list(range(50))
random.shuffle(nums)

# -------------------- SORT VARIABLES --------------------
index = 0
min_pos = index
j = index + 1

done = False
sorting = False
running = True

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
    global index
    global min_pos
    global j
    global done
    global sorting

    nums = list(range(50))
    random.shuffle(nums)

    index = 0
    min_pos = index
    j = index + 1

    done = False
    sorting = False

# -------------------- FINISH ANIMATION --------------------
def finish_animation():

    for i in range(len(nums)):

        freq = 250 + nums[i] * 10
        play_tone(freq)

        window.fill(BLACK)

        for x in range(len(nums)):

            color = GREEN if x <= i else WHITE

            pygame.draw.rect(
                window,
                color,
                (x * 16, 600 - nums[x] * 6, 15, nums[x] * 6)
            )

        pygame.display.flip()

        pygame.time.delay(20)

# -------------------- DRAW --------------------
def draw():

    for i in range(len(nums)):

        if done:
            color = GREEN

        elif i == index:
            color = RED

        elif i == min_pos:
            color = GREEN

        elif i == j:
            color = BLUE

        else:
            color = WHITE

        pygame.draw.rect(
            window,
            color,
            (i * 16, 600 - nums[i] * 6, 15, nums[i] * 6)
        )

# -------------------- MAIN LOOP --------------------
while running:

    window.fill(BLACK)

    draw()

    # -------------------- EVENTS --------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # START
            if event.key == pygame.K_SPACE and not sorting and not done:

                start = time.time()
                sorting = True

            # RESET
            if event.key == pygame.K_r:

                reset()

    # -------------------- SORTING --------------------
    if sorting:

        if j < len(nums):

            # comparison sound
            freq = 200 + nums[j] * 8
            play_tone(freq)

            if nums[j] < nums[min_pos]:

                min_pos = j

                # lower "found new minimum" sound
                play_tone(150 + nums[min_pos] * 6)

            j += 1

        else:

            # swap sound
            play_tone(300 + nums[index] * 8)

            nums[index], nums[min_pos] = nums[min_pos], nums[index]

            index += 1

            min_pos = index
            j = index + 1

        # finished
        if index >= len(nums) - 1:

            sorting = False
            done = True

            end_time = time.time()

            print(nums)
            print(f"Sorting time: {end_time - start} seconds")

            finish_animation()

    clock.tick(120)

    pygame.display.flip()

pygame.quit()