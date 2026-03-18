import pygame
import sys
import random

pygame.init()
WIDTH,HEIGHT=800,600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Meteor Dodger!")
clock=pygame.time.Clock()

BLACK=(20,20,20)
CYAN=(0,255,255)
RED=(255,50,50)
WHITE=(255,255,255)
font=pygame.font.SysFont("Arial",36,bold=True)
using_images=True

stars=[]
for _ in range (100): 
    s_x=random.randint(0,WIDTH)
    s_y=random.randint(0,HEIGHT)
    s_speed_x=random.randint(-1,1)
    s_speed_y=random.randint(1,3)
    stars.append([s_x,s_y,s_speed_x,s_speed_y])

bullets=[]
bullet_speed=10
bullet_cooldown=0

particles=[]

player_SIZE=50
player_x=WIDTH//2-player_SIZE//2
player_y=HEIGHT-player_SIZE-20
player_speed=8

meteor_size=40
meteor_speed=5
meteor_list=[]

for _ in range(6):
    m_x=random.randint(0,WIDTH-meteor_size)
    m_y=random.randint(-600,50)
    meteor_list.append([m_x,m_y])

try:
    plane =pygame.image.load("plane.png").convert_alpha()
    meteor_img=pygame.image.load("meteor.png").convert_alpha()

    plane=pygame.transform.scale(plane,(player_SIZE,player_SIZE))
    meteor_img=pygame.transform.scale(meteor_img,(meteor_size,meteor_size))

    meteor_img=pygame.transform.rotate(meteor_img,45)
except:
    print("Warning , Image not found")
    using_images=False

score=0

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x>0:
        player_x-=player_speed
    if keys[pygame.K_RIGHT] and player_x<WIDTH-player_SIZE:
        player_x+=player_speed

    if keys[pygame.K_SPACE] and bullet_cooldown==0:
        bullet_x=player_x+(player_SIZE//2)-2
        bullet_y=player_y
        bullets.append(pygame.Rect(bullet_x,bullet_y,4,5))
        bullet_cooldown=15

    if bullet_cooldown>0:
        bullet_cooldown-=1

    player_rect=pygame.Rect(player_x,player_y,player_SIZE,player_SIZE)

    for meteor in meteor_list:
        meteor[1]+=meteor_speed

        meteor_rect=pygame.Rect(meteor[0],meteor[1],meteor_size,meteor_size)

        if player_rect.colliderect(meteor_rect):
            print(f"GAME OVER. Final Score:{score}")
            running=False
        
        if meteor[1]>HEIGHT:
            meteor[0]=random.randint(0,WIDTH-meteor_size)
            meteor[1]=random.randint(-200,-50)
            score+=1
            if score%20==0:
                meteor_speed+=1

    for bullet in bullets[:]:
        bullet.y-=bullet_speed

        if bullet.y<0:
            bullets.remove(bullet)
            continue

        for meteor in meteor_list:
            meteor_rect=pygame.Rect(meteor[0],meteor[1],meteor_size,meteor_size)
            if bullet.colliderect(meteor_rect):
                if bullet in bullets:
                    bullets.remove(bullet)
                
                for _ in range(20):
                    p_x = meteor[0]+(meteor_size//2)
                    p_y = meteor[1]+(meteor_size//2)
                    p_vx= random.uniform(-5,5)
                    p_vy= random.uniform(-5,5)
                    p_timer= random.randint(15,30)

                    particles.append([p_x,p_y,p_vx,p_vy,p_timer])


                meteor[0]=random.randint(0,WIDTH-meteor_size)
                meteor[1]=random.randint(-200,-50)

                score+=5
                break

    screen.fill(BLACK)
    
    for star in stars:
        star[0] +=star[2]
        star[1] +=star[3]
        if star[1]> HEIGHT or star[0]>WIDTH or star[0]<0:
            star[0] = random.randint(0,WIDTH)
            star[1]=0
        pygame.draw.rect(screen,WHITE,(star[0],star[1],2,2))

    for particle in particles:
        particle[0]+=particle[2]
        particle[1]+=particle[3]
        particle[4]-=1

        if particle[4]<=0:
            particles.remove(particle)
        else:
            pygame.draw.rect(screen,(255,150,0),(particle[0],particle[1],4,4))
    for bullet in bullets:
        pygame.draw.rect(screen,(255,255,0),bullet)


    if using_images:
        screen.blit(plane,(player_x,player_y))

        for meteor in meteor_list:
            screen.blit(meteor_img,(meteor[0],meteor[1]))

    else:
        pygame.draw.rect(screen,CYAN,player_rect)
        for meteor in meteor_list:
            pygame.draw.rect(screen,RED,(meteor[0],meteor[1],meteor_size,meteor_size))
    
    score_text=font.render(f"Score:{score}",True,WHITE)
    screen.blit(score_text,(10,10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()