import pygame
import random
import os
import math

pygame.init()
pygame.mixer.init()
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 800
dis_height = 600


dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('貪吃蛇遊戲')
clock = pygame.time.Clock()


snake_block = 20
snake_speed = 10

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

high_score=0


def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(None,size)
    text_surface=font.render(text,True,white)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)

#取得圖片絕對位置並設置相對位置
current_dir = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(current_dir, "img","background.png")
apple_path=os.path.join(current_dir,"img","apple.png")
headright_path=os.path.join(current_dir, "img", "headright.png")
headup_path=os.path.join(current_dir, "img", "headup.png")
headdown_path=os.path.join(current_dir, "img", "headdown.png")
headleft_path=os.path.join(current_dir, "img", "headleft.png")
bodyvertical_path=os.path.join(current_dir, "img", "body_vertical.png")
bodyhorizontal_path=os.path.join(current_dir, "img", "body_horizontal.png")
tailup_path=os.path.join(current_dir, "img", "tail_up.png")
taildown_path=os.path.join(current_dir, "img", "tail_down.png")
tailright_path=os.path.join(current_dir, "img", "tail_right.png")
tailleft_path=os.path.join(current_dir, "img", "tail_left.png")
burger_path=os.path.join(current_dir, "img", "burger.png")
goldapp_path=os.path.join(current_dir, "img", "goldapp.png")
#取得音樂絕對位置並設置相對位置
bgm1_path=os.path.join(current_dir, "music", "bgm1.mp3")
sound1_path=os.path.join(current_dir, "music", "victory01.wav")
#載入圖片
background_png = pygame.image.load(background_path).convert()
apple_png=pygame.image.load(apple_path).convert()
apple_png.set_colorkey(black)
headright_png=pygame.image.load(headright_path).convert()
headup_png=pygame.image.load(headup_path).convert()
headdown_png=pygame.image.load(headdown_path).convert()
headleft_png=pygame.image.load(headleft_path).convert()
headright_png.set_colorkey(white)
headup_png.set_colorkey(white)
headdown_png.set_colorkey(white)
headleft_png.set_colorkey(white)
bodyvertical_png=pygame.image.load(bodyvertical_path).convert()
bodyhorizontal_png=pygame.image.load(bodyhorizontal_path).convert()
bodyvertical_png.set_colorkey(white)
bodyhorizontal_png.set_colorkey(white)
tailup_png=pygame.image.load(tailup_path).convert()
taildown_png=pygame.image.load(taildown_path).convert()
tailright_png=pygame.image.load(tailright_path).convert()
tailleft_png=pygame.image.load(tailleft_path).convert()
tailup_png.set_colorkey(white)
taildown_png.set_colorkey(white)
tailleft_png.set_colorkey(white)
tailright_png.set_colorkey(white)
burger_png = pygame.image.load(burger_path).convert()
burger_png.set_colorkey(black)
goldapp_png=pygame.image.load(goldapp_path).convert()
goldapp_png.set_colorkey(black)
#載入音樂
bgm1=pygame.mixer.music.load(bgm1_path)
sound1 = pygame.mixer.Sound(sound1_path)

def snake(snake_block, snake_list, snake_head_image, tail_image):
    resized_snake_head = pygame.transform.scale(snake_head_image, (snake_block, snake_block))
    resized_tail=pygame.transform.scale(tail_image, (snake_block, snake_block))
    for i, x in enumerate(snake_list):
        if i == 0:
            dis.blit(resized_snake_head, (x[0], x[1]))

        elif i == len(snake_list) - 1:  # 最尾端
            dis.blit(resized_tail, (x[0], x[1]))  

        else:
            if snake_list[i - 1][0] != x[0]: 
               bodyhorizontal=pygame.transform.scale(bodyhorizontal_png, (20, 20))
               dis.blit( bodyhorizontal, [x[0], x[1], snake_block, snake_block])
            else:
                bodyvertical=pygame.transform.scale(bodyvertical_png, (20, 20))
                dis.blit( bodyvertical, [x[0], x[1], snake_block, snake_block])

food_types = ["apple", "burger","goldapp"]  # 添加食物类型
food_probabilities = [0.5,0.3,0.2]   #食物機率
current_food_image = apple_png

#蛇頭與食物碰撞                
def eat_food(foodx, foody, snake_head, offset):
    distance = math.sqrt((foodx - snake_head[0])**2 + (foody - snake_head[1])**2)
    return distance < snake_block + offset
 
def message(msg, x, y, width, height, color,font_size):
    font = pygame.font.Font(None, font_size)
    mesg = font.render(msg, True, color)
    text_rect = mesg.get_rect(center=(x + width // 2, y + height // 2))
    dis.blit(mesg, text_rect)

def button(msg, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, inactive_color, (x, y, w, h))

    text = font_style.render(msg, True, black)
    text_rect = text.get_rect(center=(x + w / 2, y + h / 2))
    dis.blit(text, text_rect)
# 播放bgm
pygame.mixer.music.play(-1)
# 開始介面
def game_intro():
    intro = True
    while intro:
        dis.fill(blue)
        message("snake", 300, 150, 200, 50, green,100)
        button("start", 300, 300, 200, 50, 21000, red, gameLoop)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  
def gameLoop():
    score=0 
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    snake_head_image = headright_png 
    tail_image=tailleft_png


    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0


    global high_score

    while not game_over: 
        while game_close:
            
            
            dis.fill(blue)
            message("pres  R to retry",  dis_width/2, dis_height/2, 0, 50, red, 70)
            draw_text(dis, "Score: " + str(score), 80, dis_width/2, 60)
            draw_text(dis, "High Score: " + str(high_score), 30, dis_width/2, 200)
            pygame.display.update()
         
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        score = 0 
                        gameLoop()
                if event.type == pygame.QUIT:        
                     game_over = True
                     game_close =False
        if score > high_score:
            high_score = score
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                    snake_head_image = headleft_png
                    tail_image = tailright_png
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                    snake_head_image = headright_png
                    tail_image = tailleft_png
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                    snake_head_image = headup_png
                    tail_image = taildown_png
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                    snake_head_image = headdown_png
                    tail_image = tailup_png
    
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
             game_close = True

        global current_food_image
        #背景
        dis.blit(background_png,(0,0))
        #食物
        dis.blit(current_food_image, (foodx,foody))
        #分數
        draw_text(dis,str(score),40,dis_width/2,10)

        

        x1 += x1_change
        y1 += y1_change

        snake_Head = [x1, y1]
        snake_List.insert(0, snake_Head)

        
        if len(snake_List) > Length_of_snake:
            snake_List.pop()
           

        #碰到自己的身體，遊戲結束
        for x in snake_List[1:]:
            if x == snake_Head:
                game_close = True
        #吃到食物後
        if eat_food(foodx, foody, snake_Head,20):
            sound1.play() 
            if current_food_image== apple_png:
               Length_of_snake += 1
               score+= 5
               foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
               foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
               nextfood_image= random.choices(food_types, weights=food_probabilities)[0]
            elif current_food_image ==burger_png :
               Length_of_snake += 1
               score+= 20
               foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
               foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
               nextfood_image= random.choices(food_types, weights=food_probabilities)[0]
            elif current_food_image ==goldapp_png : 
               score+= 40
               foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
               foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
               nextfood_image= random.choices(food_types, weights=food_probabilities)[0]

            if  nextfood_image=="apple":
                current_food_image= apple_png
            elif nextfood_image=="burger":  
                 current_food_image =burger_png
            elif nextfood_image=="goldapp":  
                 current_food_image =goldapp_png     
        clock.tick(snake_speed)
        
        #程式更新
        snake(snake_block, snake_List, snake_head_image,tail_image)
        pygame.display.update()
    pygame.quit()
    quit()
   

game_intro()
gameLoop()
