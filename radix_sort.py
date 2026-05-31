# Radix Sort Visualization with Dynamic Sounds
# pip install pygame numpy

import pygame
import time
import random
import numpy as np

# -------------------- SETTINGS --------------------
WIDTH = 1400
HEIGHT = 700
BAR_WIDTH = 5
ARRAY_SIZE = WIDTH // BAR_WIDTH

BACKGROUND_COLOR = (20, 20, 20)
BAR_COLOR = (100, 200, 255)
COUNTING_COLOR = (255, 150, 100)
SORTED_COLOR = (0, 255, 0)
BUCKET_COLOR = (150, 150, 255)

FPS = 120

# -------------------- PYGAME SETUP --------------------
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radix Sort Visualization")

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
def draw_array(arr, digit_pos=None, sorted_indices=None):
    screen.fill(BACKGROUND_COLOR)

    for i, value in enumerate(arr):
        x = i * BAR_WIDTH
        y = HEIGHT - value

        color = BAR_COLOR

        if sorted_indices is not None and i in sorted_indices:
            color = SORTED_COLOR

        if digit_pos is not None:
            digit = (value // (10 ** digit_pos)) % 10
            color = tuple(min(255, 100 + digit * 20) for _ in range(3))

        pygame.draw.rect(screen, color, (x, y, BAR_WIDTH, value))

    pygame.display.update()


# -------------------- RADIX SORT --------------------
def radix_sort(arr):
    if not arr:
        return
    
    max_num = max(arr)
    exp = 1
    digit_pos = 0
    
    while max_num / exp > 1:
        counting_sort(arr, exp, digit_pos)
        exp *= 10
        digit_pos += 1
        
        # Draw final state for this digit
        draw_array(arr, digit_pos=None)
        time.sleep(0.1)


def counting_sort(arr, exp, digit_pos):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    # Count occurrences
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
        
        # Visualize counting
        draw_array(arr, digit_pos=digit_pos)
        play_tone(200 + index * 50, duration=0.01)
        
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

    # Update count array
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build output array
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        
        # Visualize building
        draw_array(arr, digit_pos=digit_pos)
        play_tone(400 + arr[i], duration=0.01, volume=0.05)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

    # Copy back to arr
    for i in range(n):
        arr[i] = output[i]


# -------------------- MAIN --------------------
def main():
    sorting = True
    sorted_indices = set()

    while sorting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sorting = False

        # Start sorting
        radix_sort(arr)
        
        # Mark all as sorted
        sorted_indices = set(range(len(arr)))
        draw_array(arr, digit_pos=None, sorted_indices=sorted_indices)
        
        time.sleep(2)
        sorting = False

    pygame.quit()


if __name__ == "__main__":
    main()