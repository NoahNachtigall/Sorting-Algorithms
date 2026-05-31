# a Radix-Sort visualisation using the PYGAME libary
# pip install pygame before running

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
COUNTING_COLOR = (255, 150, 100)
SORTED_COLOR = (0, 255, 0)

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
def draw_array(arr, counting_indices=None, sorted_index=None):
    screen.fill(BACKGROUND_COLOR)

    for i, value in enumerate(arr):
        x = i * BAR_WIDTH
        y = HEIGHT - value

        color = BAR_COLOR

        if counting_indices and i in counting_indices:
            color = COUNTING_COLOR

        if sorted_index is not None and i <= sorted_index:
            color = SORTED_COLOR

        pygame.draw.rect(screen, color, (x, y, BAR_WIDTH, value))

    pygame.display.update()


# -------------------- RADIX SORT --------------------
def radix_sort(arr):
    if not arr:
        return
    
    max_num = max(arr)
    exp = 1
    
    while max_num / exp > 1:
        counting_sort(arr, exp)
        exp *= 10


def counting_sort(arr, exp):                #helper function
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    # Count occurrences of each digit in the exp position
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
        
        freq = 200 + index * 100
        play_tone(freq, duration=0.01)
        
        draw_array(arr, counting_indices={i})
        
        pygame.time.delay(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    # Update the count array to hold the cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        
        freq = 400 + arr[i]
        play_tone(freq, duration=0.01, volume=0.05)
        
        draw_array(arr, counting_indices={i})
        
        pygame.time.delay(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    # Copy the output array back to arr, so that arr now contains sorted numbers
    for i in range(n):
        arr[i] = output[i]
        
        draw_array(arr)
        
        pygame.time.delay(2)


# -------------------- MAIN --------------------
def main():
    sorting = True

    while sorting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sorting = False

        radix_sort(arr)
        
        # Final sorted display
        for i in range(len(arr)):
            draw_array(arr, sorted_index=i)
            freq = 200 + arr[i]
            play_tone(freq)
            pygame.time.delay(10)
        
        time.sleep(2)
        sorting = False

    pygame.quit()


if __name__ == "__main__":
    main()