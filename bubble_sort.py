import time
import random
import pygame


pygame.init()
pygame.mixer.init()

sound = pygame.mixer.Sound("stay.mp3")
finished_sound = pygame.mixer.Sound("finished.mp3")

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Bubble Sort Visualization")

nums  = list(range(50))
random.shuffle(nums)

sorting = False
index = len(nums) - 1
j = 0
done = False


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


                
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = time.time()
                sorting = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                nums = list(range(50))
                random.shuffle(nums)
                sorting = False
                index = len(nums) - 1
                j = 0
                done = False
    
    window.fill(BLACK)
    print(index, j)
    
    if sorting:
        
        if nums[j] > nums[j+1]:
            temp = nums[j]
            nums[j] = nums[j+1]
            nums[j+1] = temp
            window.fill(BLACK)
            pygame.draw.rect(window, RED, (j * 16, 600 - nums[j] * 6, 15, nums[j] * 6))
            pygame.draw.rect(window, GREEN, ((j+1) * 16, 600 - nums[j+1] * 6, 15, nums[j+1] * 6))
            sound.play(maxtime=500)
            j += 1
            if j >= index:
              j = 0
              index -= 1
            
        else:
            j += 1
            if j >= index:
                j = 0
                index -= 1
    if index == 0:
      sorting = False
      done = True
        

    for i in range(len(nums)):
        if i == j:
            pygame.draw.rect(window, RED, (i * 16, 600 - nums[i] * 6, 15, nums[i] * 6))
        elif i == j + 1:
            pygame.draw.rect(window, GREEN, (i * 16, 600 - nums[i] * 6, 15, nums[i] * 6))
        else:
            pygame.draw.rect(window, WHITE, (i * 16, 600 - nums[i] * 6, 15, nums[i] * 6))
            
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



