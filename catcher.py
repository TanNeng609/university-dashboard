import pygame
import random

pygame.init()

WIDTH=600
HEIGHT=400
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Apple Catcher")

clock= pygame.time.Clock()

SKY_BLUE=(135,206,235)
RED=(255,0,0)
BROWN=(139,69,19)
BLACK=(0,0,0)

player_width=80
player_height=20

player_x=WIDTH//2-player_width//2
player_y=HEIGHT-40
player_speed=7

apple_radius=15
apple_x=random.randint(20,WIDTH-20)
apple_y=-50
apple_speed=5

score=0
Failed_Chance=3
font=pygame.font.SysFont("Arial",28,bold=True)

game_over_font= pygame.font.SysFont("Arial",60,bold=True)
game_over=False

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    if not game_over:
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x>0:
            player_x-=player_speed
        if keys[pygame.K_RIGHT] and player_x <WIDTH-player_width:
            player_x+=player_speed

        apple_y+=apple_speed

        if player_y<apple_y + apple_radius<player_y+player_height:
            if player_x<apple_x<player_x + player_width:
                score+=1
                apple_y=-50
                apple_x=random.randint(20,WIDTH-20)

        if apple_y>HEIGHT:
            score-=1
            Failed_Chance-=1
            apple_y=-50
            apple_x=random.randint(20,WIDTH-20)

        if Failed_Chance<0:
            game_over=True
    else:
        keys=pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over=False
            score=0
            apple_speed=5
            apple_y=-50
            player_x=WIDTH//2-player_width//2
            Failed_Chance=3

    if not game_over:
        screen.fill(SKY_BLUE)

        pygame.draw.rect(screen,BROWN,(player_x,player_y,player_width,player_height))

        pygame.draw.circle(screen,RED,(apple_x,apple_y),apple_radius)

        score_text=font.render(f"Score:{score}",True,BLACK)
        screen.blit(score_text,(10,10))

        lives_text=font.render(f"Lives:{Failed_Chance}",True,RED)
        screen.blit(lives_text,(10,40))
    else:
        screen.fill(BLACK)
        game_over_text=game_over_font.render("GAME OVER",True,RED)

        text_rect=game_over_text.get_rect(center=(WIDTH/2,HEIGHT/2))
        screen.blit(game_over_text,text_rect)

        restart_text=font.render("Press 'R' To Restart",True, SKY_BLUE)
        restart_rect= restart_text.get_rect(center=(WIDTH/2,HEIGHT/2+30))
        screen.blit(restart_text,restart_rect)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()