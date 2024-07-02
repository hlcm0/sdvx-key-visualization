import pygame
import win32api

pygame.init()
clock = pygame.time.Clock()

done = False

#分别对应 start A B C D FXL FXR 键
key_values = [ord('A'), ord('D'), ord('F'), ord('J'), ord('K'), ord('C'), ord('M')]
button_state = [0, 0, 0, 0, 0, 0, 0]  # 按键目前的状态

screen_width = 800
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("KEY STATE")

while not done:
    event = pygame.event.poll()  # User did something.
    if event.type == pygame.QUIT:  # If user clicked close.
        done = True # Flag that we are done so we exit this loop.

    #读取按键状态
    for i in range(7):
        button_state[i] = 1 if win32api.GetAsyncKeyState(key_values[i]) else 0

    #绘制按键框
    pygame.draw.rect(screen, [0,0,0], [210,60,80,80], 5)
    pygame.draw.rect(screen, [0,0,0], [310,60,80,80], 5)
    pygame.draw.rect(screen, [0,0,0], [410,60,80,80], 5)
    pygame.draw.rect(screen, [0,0,0], [510,60,80,80], 5)
    pygame.draw.rect(screen, [0,0,0], [260,180,80,50], 5)
    pygame.draw.rect(screen, [0,0,0], [460,180,80,50], 5)
    
    #绘制按键按下状态
    if button_state[1]:
        pygame.draw.rect(screen, [0,0,0], [210,60,80,80], 0)
    if button_state[2]:
        pygame.draw.rect(screen, [0,0,0], [310,60,80,80], 0)
    if button_state[3]:
        pygame.draw.rect(screen, [0,0,0], [410,60,80,80], 0)
    if button_state[4]:
        pygame.draw.rect(screen, [0,0,0], [510,60,80,80], 0)
    if button_state[5]:
        pygame.draw.rect(screen, [0,0,0], [260,180,80,50], 0)
    if button_state[6]:
        pygame.draw.rect(screen, [0,0,0], [460,180,80,50], 0)

    pygame.display.flip()
    screen.fill((255, 255, 255))

    #以120帧绘制
    clock.tick(120)
