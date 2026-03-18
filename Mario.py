import pygame
import random
import os

pygame.init()
pygame.mixer.init()
WIDTH=800
HEIGHT=600

screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()

BLACK=(0,0,0)
BLUE=(50,50,255)
GREEN=(50,255,50)
RED=(255,0,0)
WHITE=(255,255,255)

font=pygame.font.SysFont("Arial",28,bold=True)
title_font=pygame.font.SysFont("Arial",64,bold=True)
score=0
high_score=0
game_state="start"

if os.path.exists("highscore.txt"):
    with open("highscore.txt","r") as file:
        high_score=int(file.read())

walk1=pygame.image.load("walk1.png").convert_alpha()
walk2=pygame.image.load("walk2.png").convert_alpha()
walk3=pygame.image.load("walk3.png").convert_alpha()
walk4=pygame.image.load("walk4.png").convert_alpha()
walk5=pygame.image.load("walk5.png").convert_alpha()
walk6=pygame.image.load("walk6.png").convert_alpha()


walk1=pygame.transform.scale(walk1,(40,40))
walk2=pygame.transform.scale(walk2,(40,40))
walk3=pygame.transform.scale(walk3,(40,40))
walk4=pygame.transform.scale(walk4,(40,40))
walk5=pygame.transform.scale(walk5,(40,40))
walk6=pygame.transform.scale(walk6,(40,40))

walk_right=[walk1,walk2,walk3,walk4,walk5,walk6]
walk_left=[
    pygame.transform.flip(walk1,True,False),
    pygame.transform.flip(walk2,True,False),
    pygame.transform.flip(walk3,True,False),
    pygame.transform.flip(walk4,True,False),
    pygame.transform.flip(walk5,True,False),
    pygame.transform.flip(walk6,True,False),

]

plat_img=pygame.image.load("float.png").convert_alpha()
plat_img=pygame.transform.scale(plat_img,(150,20))

bounce_img=pygame.image.load("bounce.png").convert_alpha()
bounce_img=pygame.transform.scale(bounce_img,(150,20))

break_img=pygame.image.load("fragile.png").convert_alpha()
break_img=pygame.transform.scale(break_img,(150,20))

lava_img=pygame.image.load("lava.jpg")
lava_img=pygame.transform.scale(lava_img,(WIDTH,60))

sky_img=pygame.image.load("sky.jpg")
sky_img=pygame.transform.scale(sky_img,(WIDTH,HEIGHT))
sky_img_flipped=pygame.transform.flip(sky_img,False,True)


try:
    jump_sound=pygame.mixer.Sound("jump.wav")
    break_sound=pygame.mixer.Sound("break.wav")
    death_sound=pygame.mixer.Sound("death.wav")

    jump_sound.set_volume(0.4)
    break_sound.set_volume(0.5)
    death_sound.set_volume(0.6)

    pygame.mixer.music.load("battle.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

except FileNotFoundError:
    print("Audio file not found! Game run without sound")
    class DummySound:
        def play(self):pass
    jump_sound=DummySound()
    break_sound=DummySound()
    death_sound=DummySound()

frame_index=0
animation_timer=0
animation_speed=2
facing_right=True


START_X=350
START_Y=400
player=pygame.Rect(START_X,START_Y,40,40)

player_vel_y=0
gravity=0.5
jump_strength=-15
is_grounded=False
player_speed=5

platforms = [
    {"rect": pygame.Rect(300, 500, 150, 20), "speed": 0, "type":"normal"},  # Still
    {"rect": pygame.Rect(100, 350, 150, 20), "speed": 3, "type":"normal"},  # Moves Right!
    {"rect": pygame.Rect(400, 250, 150, 20), "speed": -3, "type":"normal"}, # Moves Left!
    {"rect": pygame.Rect(250, 50, 150, 20),  "speed": 0, "type":"normal"},   # Still
    {"rect": pygame.Rect(150, 150, 150, 20), "speed":1, "type":"normal"},
    {"rect": pygame.Rect(0, 0, 150, 20), "speed":2, "type":"normal"},

]

lava=pygame.Rect(0,540,WIDTH,60)

bg_scroll=0
particles=[]

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                if game_state=="start":
                    game_state="playing"
                elif game_state=="gameover":
                    player.x=START_X
                    player.y=START_Y
                    player_vel_y=0
                    score=0
                    standing_on=None

                    platforms = [
                        {"rect": pygame.Rect(300, 500, 150, 20), "speed": 0, "type":"normal"},  # Still
                        {"rect": pygame.Rect(100, 350, 150, 20), "speed": 3, "type":"normal"},  # Moves Right!
                        {"rect": pygame.Rect(400, 250, 150, 20), "speed": -3, "type":"normal"}, # Moves Left!
                        {"rect": pygame.Rect(250, 50, 150, 20),  "speed": 0, "type":"normal"},   # Still
                        {"rect": pygame.Rect(150, 150, 150, 20), "speed":1, "type":"normal"},
                        {"rect": pygame.Rect(0, 0, 150, 20), "speed":2, "type":"normal"}

                        ]
                    game_state="playing"

            elif event.key==pygame.K_SPACE:
                if game_state=="playing" and is_grounded:
                    player_vel_y=jump_strength
                    is_grounded=False
                    jump_sound.play()

                    if standing_on and standing_on["type"]=="breakable":
                        if standing_on in platforms:

                            for _ in range(15):
                                p_x=standing_on["rect"].x+random.randint(0,150)
                                p_y=standing_on["rect"].y+random.randint(0,20)
                                p_vx=random.randint(-5,5)
                                p_vy=random.randint(-10,-2)
                                particles.append([p_x,p_y,p_vx,p_vy,255])
                            platforms.remove(standing_on)
                            break_sound.play()
    
    
    if game_state!="playing":
        screen.blit(sky_img,(0,0))

        if game_state=="start":
            title_text=title_font.render("LAVA JUMPER",True,WHITE)
            prompt_text=font.render("Press Enter to Start",True,WHITE)
            screen.blit(title_text,(WIDTH//2-title_text.get_width()//2,200))
            screen.blit(prompt_text,(WIDTH//2-prompt_text.get_width()//2,300))
        elif game_state=="gameover":
            title_text=title_font.render("GAME OVER",True,RED)
            score_text=font.render(f"Final Score: {score}",True,WHITE)
            prompt_text=font.render("Press Enter to Restart",True,WHITE)
    
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 150))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 250))
            screen.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, 350))    
        
        pygame.display.flip()
        clock.tick(60)
        continue
    
    dx=0
    keys=pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx= -player_speed
        facing_right=False
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx=player_speed
        facing_right=True

    player.x+=dx

    for p in platforms:
        plat=p["rect"]
        plat.x+=p["speed"]

        if plat.left<0 or plat.right>WIDTH:
            p["speed"] *=-1

    for p in platforms:
        plat=p["rect"]
        if player.colliderect(plat):
            if dx>0:
                player.right=plat.left
            elif dx<0:
                player.left=plat.right

    if player.colliderect(lava):
        death_sound.play()
        
        if score>high_score:
            high_score=score

            with open("highscore.txt","w") as file:
                file.write(str(high_score))
        game_state="gameover"
        
    if player.right<0:
        player.left=WIDTH
    if player.left>WIDTH:
        player.right=0

    player_vel_y+=gravity
    player.y+=player_vel_y

    is_grounded=False
    standing_on=None

    for p in platforms:
        plats=p["rect"]
        if player.colliderect(plats):
            if player_vel_y>0:
                player.bottom=plats.top
                player_vel_y=0
                is_grounded=True
                player.x+=p["speed"]

                standing_on=p

                if p["type"]=="bouncy":
                    player_vel_y=-25
                    is_grounded=False

            elif player_vel_y<0:
                player.top=plats.bottom
                player_vel_y=0

    if player.y<150:
        scroll=150-player.y
        player.y=150
        for p in platforms:
            p["rect"].y+=scroll

        for p in particles:
            p[1]+=scroll

        bg_scroll+=scroll*0.2
        if bg_scroll>=HEIGHT*2:
            bg_scroll=0

    for p in platforms[:]:
        plat=p["rect"]
        if plat.top>HEIGHT:
            platforms.remove(p)
            score+=1

    if len(platforms)>0:
        highest_plat=min(platforms,key=lambda p:p["rect"].y)

        while highest_plat["rect"].y>-50:
            highest_y=highest_plat["rect"].y
            last_x=highest_plat["rect"].x


            new_y=highest_y-random.randint(100,150)

            while True:
                new_x=random.randint(0,WIDTH-150)
                dist=abs(new_x-last_x)
                wrap_dist=WIDTH-dist
                shortest_dist=min(dist,wrap_dist)

                if 100<shortest_dist<350:
                    break

            random_speed=random.choice([0,0,0,3,-3,4,-4])

            dice_roll=random.randint(1,100)
            if dice_roll<70:
                plat_type="normal"
            elif dice_roll<95:
                plat_type="breakable"
            else:
                plat_type="bouncy"

            new_platform = {"rect": pygame.Rect(new_x, new_y, 150, 20), "speed": random_speed, "type": plat_type}
            platforms.append(new_platform)

            highest_plat=new_platform

    if dx!=0 and is_grounded:
        animation_timer+=1
        if animation_timer>=animation_speed:
            frame_index+=1
            if frame_index>=len(walk_right):
                frame_index=0
            animation_timer=0
    else:
            frame_index=0

    screen.blit(sky_img,(0,bg_scroll))
    screen.blit(sky_img_flipped,(0,bg_scroll-HEIGHT))
    screen.blit(sky_img, (0,bg_scroll-HEIGHT*2))

    for p in particles[:]:
        p[0]+=p[2]
        p[3]+=gravity
        p[1]+=p[3]
        p[4]-=5

        if p[4]<=0:
            particles.remove(p)
        else:
            pygame.draw.rect(screen,(139,69,19),(p[0],p[1],6,6))
    
    for p in platforms: 
        plat=p["rect"]
        if p["type"] == "bouncy":
            screen.blit(bounce_img, (plat.x, plat.y))
        elif p["type"] == "breakable":
            screen.blit(break_img, (plat.x, plat.y))
        else:
            screen.blit(plat_img, (plat.x, plat.y))
    
    screen.blit(lava_img,(lava.x,lava.y))


    score_text=font.render(f"Score: {score}",True,WHITE)
    screen.blit(score_text,(10,10))

    high_score_text = font.render(f"Best: {high_score}", True, WHITE)
    screen.blit(high_score_text, (10, 40))

    if facing_right:
        screen.blit(walk_right[frame_index],(player.x,player.y))
    else:
        screen.blit(walk_left[frame_index],(player.x,player.y))
    
    
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

