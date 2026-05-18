# a Merge-Sort visualisation using the PYGAME libary
# pip install pygame before running

import numpy as np
import pygame
import random
import time

# -------------------- SETTINGS --------------------        change the settings to your use
WIDTH = 1200
HEIGHT = 700
BAR_WIDTH = 10
ARRAY_SIZE = WIDTH // BAR_WIDTH

BACKGROUND_COLOR = (20, 20, 20)
BAR_COLOR = (100, 200, 255)
LEFT_COLOR = (255, 100, 100)
RIGHT_COLOR = (100, 255, 100)
MERGED_COLOR = (255, 255, 100)
SORTED_COLOR = (0, 255, 0)

FPS = 120

# -------------------- PYGAME SETUP --------------------
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Merge Sort Visualization")

clock = pygame.time.Clock()

# -------------------- ARRAY --------------------
def generate_array():
    return [random.randint(10, HEIGHT - 50) for _ in range(ARRAY_SIZE)]
arr = generate_array()


# -------------------- DYNAMIC TONES --------------------
pygame.mixer.init(frequency=44100, size=-16, channels=1)

# -------------------- SOUND --------------------
def play_tone(frequency, duration=0.02, volume=0.1):
    sample_rate = 44100

    t = np.linspace(0, duration, int(sample_rate * duration), False)

    wave = np.sin(frequency * 2 * np.pi * t)

    audio = wave * (2**15 - 1) * volume
    audio = np.column_stack((audio, audio))
    audio = audio.astype(np.int16)

    sound = pygame.sndarray.make_sound(audio)

    sound.play()

# -------------------- DRAW FUNCTION --------------------
def draw_array(arr, left=None, right=None, merged=None, sorted_index=None):
    screen.fill(BACKGROUND_COLOR)

    for i, value in enumerate(arr):
        x = i * BAR_WIDTH
        y = HEIGHT - value

        color = BAR_COLOR

        if left and left[0] <= i <= left[1]:
            color = LEFT_COLOR

        if right and right[0] <= i <= right[1]:
            color = RIGHT_COLOR

        if merged and merged[0] <= i <= merged[1]:
            color = MERGED_COLOR

        if sorted_index is not None and i <= sorted_index:
            color = SORTED_COLOR

        pygame.draw.rect(screen, color, (x, y, BAR_WIDTH, value))

    pygame.display.update()


# -------------------- MERGE SORT --------------------
def merge_sort(arr, start, end):
    if end - start <= 1:
        return

    mid = (start + end) // 2

    merge_sort(arr, start, mid)                 #left arr
    merge_sort(arr, mid, end)                   #right arr

    merge(arr, start, mid, end)                 #sorted arr


def merge(arr, start, mid, end):                #helper function
    left = arr[start:mid]
    right = arr[mid:end]

    i = 0
    j = 0
    k = start

    while i < len(left) and j < len(right):             #compare left arr and right arr

        freq = 200 + arr[k]
        play_tone(freq)

        # draw current state
        draw_array(
            arr,
            left=(start, mid - 1),
            right=(mid, end - 1),
            merged=(start, k)
        )

        pygame.time.delay(5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if left[i] < right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1

        k += 1

    while i < len(left):                               #if left arr still has elements but right arr not then just add all left elements
        arr[k] = left[i]
        i += 1
        k += 1

        draw_array(
            arr,
            left=(start, mid - 1),
            merged=(start, k)
        )

        pygame.time.delay(5)

    while j < len(right):                               #if right arr still has elements but left arr not then just add all left elements
        arr[k] = right[j]
        j += 1
        k += 1

        draw_array(
            arr,
            right=(mid, end - 1),
            merged=(start, k)
        )

        pygame.time.delay(5)

def finish_animation(arr):

    for i in range(len(arr)):

        freq = 200 + arr[i]
        play_tone(freq)

        draw_array(arr, sorted_index=i)

        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# -------------------- MAIN LOOP --------------------
running = True
sorting = False

while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not sorting:
                sorting = True

                start_time = time.perf_counter()

                merge_sort(arr, 0, len(arr))

                end_time = time.perf_counter()

                print("Time Taken:", end_time - start_time)

            if event.key == pygame.K_r:

                arr = generate_array()

                sorting = False

        

    draw_array(arr)

pygame.quit()