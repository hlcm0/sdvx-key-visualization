import pygame
import time
import win32api

pygame.init()
clock = pygame.time.Clock()

done = False

#用于存储目前
key_object_list = []

#分别对应 start A B C D FXL FXR 键
key_values = [ord('A'), ord('D'), ord('F'), ord('J'), ord('K'), ord('C'), ord('M')]

#按键的前一次状态
button_last_state = [0, 0, 0, 0, 0, 0, 0]

#按键目前的状态
button_state = [0, 0, 0, 0, 0, 0, 0]

#可视化展示音符的持续时间(在key_object_list中的保留时间)，同时也是屏幕显示的时间长度，同时也是窗口的高度（1毫秒对应1像素）
show_duration = 1000

screen_width = 400
screen_height = show_duration
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SDVX INPUT")

while not done:
    event = pygame.event.poll()  # User did something.
    if event.type == pygame.QUIT:  # If user clicked close.
        done = True # Flag that we are done so we exit this loop.

    now_t = int(round(time.time() * 1000))

    for i in range(7):                            # 检测按键上升下降沿，对key_object_list进行相应更新

        button_state[i] = 1 if win32api.GetAsyncKeyState(key_values[i]) else 0

        if button_state[i] == 1:
            if button_last_state[i] == 0:  # 假如按键从松开转变为按下，则在key_object_list里添加新的object
                key_object_list.append([i, now_t, now_t, True])  # [按键轨道序号，按下开始时间，按下结束时间，是否正在被按着]
            for key_object_list_num in range(len(key_object_list) - 1, -1, -1):  # 假如按键持续按下，更新key_object_list中对应的end时间戳
                if key_object_list[key_object_list_num][0] == i:
                    key_object_list[key_object_list_num][2] = now_t
                    break

        if (button_last_state[i] == 1) and (button_state[i] == 0):  # 假如按键从按下变为松开
            for key_object_list_num in range(len(key_object_list) - 1, -1, -1):  # 将key_object_list中对应的object的持续状态设为False
                if key_object_list[key_object_list_num][0] == i:
                    key_object_list[key_object_list_num][3] = False
                    break
        button_last_state[i] = button_state[i]

    # 要删除的object的下标列表
    delete_list = []
    for i in range(len(key_object_list)):   # 删除key_object_list中已经超出屏幕的object
        if (key_object_list[i][3] == False) and (key_object_list[i][2] < (now_t - show_duration)):  # 同时还要判断这个键是否还在被按着
            delete_list.append(i)
    delete_list.reverse()
    for i in delete_list:
        key_object_list.pop(i)



    fx_long = []
    bt_long = []
    fx_chip = []
    bt_chip = []

    for i in key_object_list:  # 将key_object_list中的键分类，序号0为start键，1~4为bt，5~6为fx
        if i[0] != 0:
            start = show_duration + i[1] - now_t
            end = show_duration + i[2] - now_t
            length = end - start

            # 根据按下长度区分chip和long
            if length < 200:
                # 为chip
                if 0 < i[0] < 5:
                    bt_chip.append([i[0], start])
                else:
                    fx_chip.append([i[0], start])
            else:
                # 为long
                if 0 < i[0] < 5:
                    bt_long.append([i[0], start, length])
                else:
                    fx_long.append([i[0], start, length])

    # 绘制fx_long
    for i in fx_long:
        x = (i[0] - 5) * 200
        y = i[1]
        length = i[2]
        pygame.draw.rect(screen, [200, 200, 0], [x, y, 200, length], 0)

    # 绘制bt_long
    for i in bt_long:
        x = (i[0] - 1) * 100 + 10
        y = i[1]
        length = i[2]
        pygame.draw.rect(screen, [255, 255, 255], [x, y, 80, length], 0)

    # 绘制fx_chip
    for i in fx_chip:
        x = (i[0] - 5) * 200 + 10
        y = i[1]
        length = 10
        pygame.draw.rect(screen, [200, 200, 0], [x, y, 180, length], 0)

    # 绘制bt_chip
    for i in bt_chip:
        x = (i[0] - 1) * 100 + 10
        y = i[1]
        length = 10
        pygame.draw.rect(screen, [255, 255, 255], [x, y, 80, length], 0)

    pygame.display.flip()
    screen.fill((0, 0, 0))

    clock.tick(1000)
