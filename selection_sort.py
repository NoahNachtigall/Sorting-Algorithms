import pygame
import time
import random

pygame.init()
pygame.mixer.init()

#sounds
sound = pygame.mixer.Sound("stay.mp3")
finished_sound = pygame.mixer.Sound("finished.mp3")

# Fenster
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Test")
clock = pygame.time.Clock()

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Nummern fuer balken
nums = list(range(50))
random.shuffle(nums)

# Sort-Variablen
index = 0
min_pos = index
j = index + 1
done = False

running = True
sorting = False


# Zeichnen
def draw():
    for i in range(len(nums)):
        if i == index:
            color = RED
        elif i == min_pos:
            color = GREEN
        elif i == j:
            color = (0, 0, 255)  # blau
        else:
            color = WHITE

        pygame.draw.rect(
            window,
            color,
            (i * 16, 600 - nums[i] * 6, 15, nums[i] * 6)
        )



while running:
    window.fill(BLACK)
    draw()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               start = time.time()
               sorting = True
                
    
    if sorting:
        if j < len(nums):
            sound.play()
            if nums[j] < nums[min_pos]:
                min_pos = j
            j += 1                       #j muss immer + 1 ich bin so dumm

                
        else:
            temp = nums[index]
            nums[index] = nums[min_pos]
            nums[min_pos] = temp

            index += 1
            min_pos = index
            j = index + 1

                
        if index >= len(nums) - 1:
            done = True
    
    if done:
        finished_sound.play()
        end_time = time.time()
        print(nums)
        print(f"Sorting time: {end_time - start} Seconds")
        time.sleep(2000)
        running = False
        pygame.quit()

    clock.tick(120)
    pygame.display.flip()

pygame.quit()