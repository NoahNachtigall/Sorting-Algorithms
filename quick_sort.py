#Visualisation of Quick Sort Algorithm using pygame'
import numpy as np
import pygame
import random
import time

# -------------------- SETTINGS --------------------        change the settings to your use
WIDTH = 1400
HEIGHT = 700
BAR_WIDTH = 5
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
pygame.display.set_caption("Quick Sort Visualization")

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


# -------------------- EVENT HANDLING --------------------
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


# -------------------- QUICK SORT --------------------
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        handle_events()
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            play_tone(200 + arr[i])
            draw_array(arr, left=(low, i), right=(j, high))
            pygame.time.delay(10)

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    play_tone(200 + arr[i + 1])
    draw_array(arr, left=(low, i + 1), right=(high, high))
    pygame.time.delay(10)

    return i + 1


def QuickSort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        QuickSort(arr, low, pi - 1)
        QuickSort(arr, pi + 1, high)


def finish_animation(arr):
    for i in range(len(arr)):
        handle_events()
        freq = 200 + arr[i]
        play_tone(freq)
        draw_array(arr, sorted_index=i)
        pygame.time.delay(10)

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

                QuickSort(arr, 0, len(arr) - 1)
                finish_animation(arr)

                end_time = time.perf_counter()
                print("Time Taken:", end_time - start_time)

                sorting = False

            if event.key == pygame.K_r:

                arr = generate_array()

                sorting = False

        

    draw_array(arr)

pygame.quit()