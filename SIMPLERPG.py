import pygame
import random

pygame.init()

info= pygame.display.Info()
WIDTH =info.current_w
HEIGHT=info.current_h
screen=pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)
clock=pygame.time.Clock()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("Arial", 28, bold=True)
battle_font= pygame.font.SysFont("Arial",50,bold=True)

TILE_SIZE=60

player_speed=5
player_rect= pygame.Rect(0,0,40,40)
chest_rect=pygame.Rect(0,0,30,30)
monster_rect=pygame.Rect(0,0,40,40)

img1=pygame.image.load("walk1.jpg")
img2=pygame.image.load("walk2.jpg")
img3=pygame.image.load("walk3.jpg")
img4=pygame.image.load("walk4.jpg")
img5=pygame.image.load("walk5.jpg")
img6=pygame.image.load("walk6.jpg")

img1=pygame.transform.scale(img1,(40,40))
img2=pygame.transform.scale(img2,(40,40))
img3=pygame.transform.scale(img3,(40,40))
img4=pygame.transform.scale(img4,(40,40))
img5=pygame.transform.scale(img5,(40,40))
img6=pygame.transform.scale(img6,(40,40))

player_frames=[img1,img2,img3,img4,img5,img6]


hit_sound=pygame.mixer.Sound("hit.wav")
heal_sound=pygame.mixer.Sound("heal.wav")

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)

current_frame=0
animation_timer=0
facing_left=False
startx=0
starty=0
step_counter=0

chest_img=pygame.image.load("chest.png")
wall_img=pygame.image.load("wall.jpg")
grass_img=pygame.image.load("grass.jpg")
monster_img=pygame.image.load("monster.png")
menu_bg=pygame.image.load("unnamed.png")
NPC1_img=pygame.image.load("NPC1.jpeg")

chest_img=pygame.transform.scale(chest_img,(30,30))
wall_img=pygame.transform.scale(wall_img,(TILE_SIZE,TILE_SIZE))
grass_img=pygame.transform.scale(grass_img, (TILE_SIZE,TILE_SIZE))
monster_img=pygame.transform.scale(monster_img,(TILE_SIZE,TILE_SIZE))
menu_bg=pygame.transform.scale(menu_bg,(WIDTH,HEIGHT))
NPC1_img=pygame.transform.scale(NPC1_img,(TILE_SIZE,TILE_SIZE))


boss_img=pygame.image.load("boss.jpg")
boss_img=pygame.transform.scale(boss_img,(120,120))

monsters=[]
constant_monster=[]
current_monster=None

level_map=[
    "........................................................",
    "........................................................",
    "........................................................",
    "........................................................",
    "........................................................",
    "........................................................",
    "...........WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW..............",
    "...........WS.....W......................W..............",
    "...........W..P...W.......C..............W..............",
    "...........W......W......................W..............",
    "...........WWWW..WWWWWWWWWWWWMMWWWWWWWWWWW..............",
    "...........W......................W......W..............",
    "...........W......................W......W..............",
    "...........W......................W......W..............",
    "...........W.........B............M......W..............",
    "...........W......................W......W..............",
    "...........W......................W......W..............",
    "...........WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW..............",
    "........................................................",
    "........................................................",
    "........................................................",
    "........................................................",
    "........................................................",
    "........................................................"


]

walls=[]

boss_rect=pygame.Rect(0,0,120,120)
boss_alive=True

shop_rect= pygame.Rect(0,0,TILE_SIZE,TILE_SIZE)

y=0
for row in level_map:
    x=0
    for tile in row:
        if tile =="W":
            walls.append(pygame.Rect(x,y,TILE_SIZE,TILE_SIZE))
        elif tile =="P":
            player_rect.x=x
            player_rect.y=y
            startx=x
            starty=y
        elif tile =="C":
            chest_rect.x=x
            chest_rect.y=y
        elif tile =="M":
            monsters.append(pygame.Rect(x,y,TILE_SIZE,TILE_SIZE))
            constant_monster.append(pygame.Rect(x,y,TILE_SIZE,TILE_SIZE))
        elif tile =="B":
            boss_rect.x=x
            boss_rect.y=y
        elif tile =="S":
            shop_rect.x=x
            shop_rect.y=y

        x+=TILE_SIZE
    y+=TILE_SIZE

chest_opened=False
gold_coins=0

game_state="MENU"
player_level=1
player_max_hp=100
player_hp=player_max_hp
monster_hp=50
action_message="Press Shift to start the battle!!!"
reaction_message=""

inventory=[{
    "name":"Rusty Dagger",
    "min_dmg":5,
    "max_dmg":15
}]
current_weapon=inventory[0]

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running=False

            if event.key==pygame.K_c:
                if game_state=="MAP":
                    game_state="STATUS"
                elif game_state=="STATUS":
                    game_state="MAP"
            if game_state=="MENU":
                if event.key==pygame.K_RETURN:
                    game_state="MAP"

            if event.key==pygame.K_i:
                if game_state=="MAP":
                    game_state="INVENTORY"
                elif game_state=="INVENTORY":
                    game_state="MAP"
            if game_state=="INVENTORY":
                if pygame.K_1<=event.key<=pygame.K_9:
                    index_to_equip=event.key-pygame.K_1

                    if index_to_equip<len(inventory):
                        current_weapon=inventory[index_to_equip]                

            if game_state=="BATTLE":
                if event.key== pygame.K_a:
                    hit_sound.play()

                    wep_min=current_weapon["min_dmg"]
                    wep_max=current_weapon["max_dmg"]
                    player_damage=random.randint(wep_min,wep_max)+player_level*10
                    monster_hp-=player_damage
                    action_message = f"You hit the monster for {player_damage}!"                    

                    if monster_hp>0:
                        if current_monster=="BOSS":
                            monster_damage=random.randint(45,55)+player_level*10
                        else:
                            monster_damage=random.randint(15,25)+player_level*10
                        player_hp-=monster_damage
                        reaction_message = f"Monster hit you back for {monster_damage}!"
                    else:
                        reaction_message = ""

                elif event.key==pygame.K_h:
                    heal_sound.play()
                    wep_min=current_weapon["min_dmg"]
                    wep_max=current_weapon["max_dmg"]
                    heal_amount=random.randint(wep_min+20,wep_max+40)+player_level*10
                    player_hp+=heal_amount

                    if player_hp>player_max_hp:
                        player_hp=player_max_hp
                    action_message = f"You healed for {heal_amount} HP!"

                    if current_monster=="BOSS":
                        monster_damage=random.randint(45,55)+player_level*10
                    else:
                        monster_damage=random.randint(15,25)+player_level*10                    
                    player_hp-=monster_damage
                    reaction_message = f"Monster hit you for {monster_damage} while healing!"

            if game_state=="GAMEOVER":
                if event.key==pygame.K_r:
                    player_hp=100
                    player_max_hp=100
                    player_level=1
                    gold_coins=0
                    boss_alive=True

                    inventory=[
                        {
                            "name":"Rusty Dagger",
                            "min_dmg":5,
                            "max_dmg":15
                        }
                    ]
                    current_weapon=inventory[0]

                    step_counter=0
                    monsters=constant_monster.copy()

                    
                    pygame.mixer.music.load("background.mp3")
                    pygame.mixer.music.play(-1)
                    chest_opened=False
                    player_rect.x=startx
                    player_rect.y=starty
                    game_state="MAP"

            if game_state=="SHOP":
                if event.key==pygame.K_x:
                    game_state="MAP"
                elif event.key==pygame.K_1:
                    already_owned=False
                    for w in inventory:
                        if w["name"]=="Flaming Axe":
                            already_owned=True
                    if gold_coins>= 1500 and not already_owned:
                        gold_coins-=1500
                        new_axe={
                            "name":"Flaming Axe",
                            "min_dmg":50,
                            "max_dmg":80
                        }
                        inventory.append(new_axe)
                        current_weapon=new_axe
                        heal_sound.play()
                                    
                elif event.key==pygame.K_2:
                    already_owned=False
                    for w in inventory:
                        if w["name"]=="Magic Wand":
                            already_owned=True
                    if gold_coins>= 2000 and not already_owned:
                        gold_coins-=2000
                        new_wep={
                            "name":"Magic Wand",
                            "min_dmg":40,
                            "max_dmg":100
                        }
                        inventory.append(new_wep)
                        current_weapon=new_wep
                        heal_sound.play()

                elif event.key==pygame.K_3:
                    already_owned=False
                    for w in inventory:
                        if w["name"]=="Dragon Spear":
                            already_owned=True
                    if gold_coins>= 5000 and not already_owned:
                        gold_coins-=5000
                        new_wep={
                            "name":"Dragon Spear",
                            "min_dmg":70,
                            "max_dmg":120
                        }
                        inventory.append(new_wep)
                        current_weapon=new_wep
                        heal_sound.play()

    if game_state=="MAP":

        keys=pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running=False

        old_x=player_rect.x
        old_y=player_rect.y

        is_moving=False

        if keys[pygame.K_LEFT]:
            player_rect.x-=player_speed
            is_moving=True
            facing_left=True
        if keys[pygame.K_RIGHT]:
            player_rect.x+=player_speed
            is_moving=True
            facing_left=False
        if keys[pygame.K_UP]:
            player_rect.y-=player_speed
            is_moving=True
        if keys[pygame.K_DOWN]:
            player_rect.y+=player_speed    
            is_moving=True

        if is_moving:
            animation_timer+=1
            step_counter+=1
            if animation_timer>2:
                current_frame+=1
                if current_frame>5:
                    current_frame=0
                animation_timer=0

            if step_counter>300:
                step_counter=0

                safe_spot=False
                while not safe_spot:
                    rand_x=random.randint(12,40)*TILE_SIZE
                    rand_y=random.randint(7,16)*TILE_SIZE

                    new_monster =pygame.Rect(rand_x,rand_y,TILE_SIZE,TILE_SIZE)

                    hit_wall=False
                    for wall in walls:
                        if new_monster.colliderect(wall):
                            hit_wall=True
                            break
                        
                    if not hit_wall and not new_monster.colliderect(player_rect) and not new_monster.colliderect(chest_rect):
                            monsters.append(new_monster)
                            safe_spot=True
        else:
                current_frame=0
                animation_timer=0

        for wall in walls:
            if player_rect.colliderect(wall):
                player_rect.x=old_x
                player_rect.y=old_y

        if player_rect.colliderect(shop_rect):
            player_rect.x=old_x
            player_rect.y=old_y
            game_state="SHOP"

        if player_rect.colliderect(chest_rect) and not chest_opened:
            chest_opened=True
            gold_coins+=1000

            new_sword={
                "name":"Steel Broadsword",
                "min_dmg":25,
                "max_dmg":40
            }
            inventory.append(new_sword)
            current_weapon=new_sword

            heal_sound.play()

        for m in monsters:
            if player_rect.colliderect(m):
                current_monster=m
                game_state="BATTLE"

                pygame.mixer.music.load("battle.mp3")
                pygame.mixer.music.play(-1)

                monster_hp=50+player_level*10
                action_message = "A wild monster appears!"
                reaction_message = "Press Shift to start the battle!!!"
                break
        if player_rect.colliderect(boss_rect) and boss_alive:
            current_monster="BOSS"
            game_state="BATTLE"

            pygame.mixer.music.load("battle.mp3")
            pygame.mixer.music.play(-1)

            monster_hp=500
            action_message="THE BOSS APPEAR!!!"
            reaction_message="Preparee to fight for your life!"

    
    elif game_state =="BATTLE":
        if monster_hp<=0:
            if current_monster=="BOSS":
                boss_alive=False
                gold_coins+=5000
                player_level+=5
                player_max_hp+=100
            else:
                monsters.remove(current_monster)
                gold_coins+=500
                player_level+=1
                player_max_hp+=20

            player_hp=player_max_hp

            pygame.mixer.music.load("background.mp3")
            pygame.mixer.music.play(-1)

            game_state="MAP"

        elif player_hp<=0:
            game_state="GAMEOVER"

    screen.fill(BLACK)

    if game_state=="MENU":
        screen.blit(menu_bg,(0,0))

        title=battle_font.render("MY EPIC RPG",True,(255,215,0))
        screen.blit(title,(WIDTH//2-150,HEIGHT//2-100))

        start_text=font.render("Press [ENTER] to Play", True,WHITE)
        screen.blit(start_text,(WIDTH//2-120,HEIGHT//2+50))

    elif game_state=="MAP":
        camera_x= player_rect.centerx-(WIDTH/2)
        camera_y= player_rect.centery-(HEIGHT/2)


        draw_y=0
        for row in level_map:
            draw_x=0
            for tile in row:
                screen_x=draw_x-camera_x
                screen_y=draw_y-camera_y
                if tile=="W":
                    screen.blit(wall_img,(screen_x,screen_y))
                else:
                    screen.blit(grass_img,(screen_x,screen_y))
                draw_x+=TILE_SIZE
            draw_y+=TILE_SIZE


        screen.blit(NPC1_img,(shop_rect.x-camera_x,shop_rect.y-camera_y))

        if not chest_opened:
            screen.blit(chest_img,(chest_rect.x-camera_x,chest_rect.y-camera_y))

        if boss_alive:
            screen.blit(boss_img,(boss_rect.x-camera_x,boss_rect.y-camera_y))

        for m in monsters:
            screen.blit(monster_img,(m.x-camera_x,m.y-camera_y))

        current_image=player_frames[current_frame]

        if facing_left:
            current_image=pygame.transform.flip(current_image,True,False)
        
        screen.blit(current_image,(player_rect.x-camera_x,player_rect.y-camera_y))

        ui_text=font.render(f"Gold: {gold_coins}",True,(255,255,255))
        screen.blit(ui_text,(10,10))

    elif game_state=="BATTLE":
        title=battle_font.render("A WILD MONSTER APPEAR!",True, RED)
        screen.blit(title,(WIDTH//2-300,100))

        stats= battle_font.render(f"Player HP:{player_hp}        Monster HP:{monster_hp}",True,WHITE)
        screen.blit(stats,(WIDTH//2-350,300))

        msg1 = font.render(action_message, True, (255, 255, 0)) 
        screen.blit(msg1, (WIDTH//2-200, 400))
        
        msg2 = font.render(reaction_message, True, RED)
        screen.blit(msg2, (WIDTH//2-200, 450))

        menu= battle_font.render("Press [A] to Attack or [H] to Heal",True,WHITE)
        screen.blit(menu,(WIDTH//2-350,500))

    elif game_state=="GAMEOVER":
        title=battle_font.render("GAMEOVER",True,RED)
        screen.blit(title,(WIDTH//2-150,HEIGHT//2-100))
        menu=font.render("Press [R] to Restart",True,WHITE)
        screen.blit(menu,(WIDTH//2-120,HEIGHT//2+50))

    elif game_state=="STATUS":
        title= battle_font.render("CHARACTER STATUS",True,(255,215,0))
        screen.blit(title,(WIDTH//2-250,100))

        lvl_text=font.render(f"Level: {player_level}",True,WHITE)
        hp_text = font.render(f"Health Points: {player_hp}/{player_max_hp}",True,WHITE)
        gold_text = font.render(f"Wealth: {gold_coins} Gold Coins",True,(255,215,0))
        weapon_text = font.render(f"Weapon: {current_weapon['name']} ({current_weapon['min_dmg']}-{current_weapon['max_dmg']} DMG)", True, WHITE)

        screen.blit(lvl_text,(WIDTH//2-150,250))
        screen.blit(hp_text,(WIDTH//2-150,320))
        screen.blit(gold_text,(WIDTH//2-150,390))        
        screen.blit(weapon_text, (WIDTH//2 - 150, 460))


        Close_text = font.render("Press [C] to return to the Map",True,WHITE)
        screen.blit(Close_text,(WIDTH//2-180,550))

    elif game_state=="SHOP":
        title=battle_font.render("THE MERCHANT",True,(255,215,0))
        screen.blit(title,(WIDTH//2-200,100))

        wallet_text=font.render(f"Your Wallet: {gold_coins} Gold", True,WHITE)
        screen.blit(wallet_text,(WIDTH//2-150,250))

        item1 = font.render("[1] Flaming Axe (50-80 DMG) - Cost: 1500 Gold", True, RED)
        screen.blit(item1, (WIDTH//2 - 300, 280))

        item2 = font.render("[2] Magic Wand (40-100 DMG) - Cost: 2000 Gold", True, (0, 255, 255)) 
        screen.blit(item2, (WIDTH//2 - 300, 350))

        item3 = font.render("[3] Dragon Spear (70-120 DMG) - Cost: 5000 Gold", True, (255, 165, 0)) 
        screen.blit(item3, (WIDTH//2 - 300, 420))
        buy_text=font.render("Press [B] to Buy",True,(0,255,0))
        leave_text=font.render("Press [X] to Leave",True,WHITE)

        screen.blit(buy_text,(WIDTH//2-100,450))
        screen.blit(leave_text,(WIDTH//2-120,500))

    elif game_state=="INVENTORY":
        title = battle_font.render("YOUR BACKPACK", True, (255, 215, 0))
        screen.blit(title, (WIDTH//2 - 200, 100))

        instruction = font.render("Press [1], [2], or [3] to Equip a Weapon!", True, WHITE)
        screen.blit(instruction, (WIDTH//2 - 250, 200))

        y_offset=300
        for index in range(len(inventory)):
            weapon=inventory[index]        

            if weapon== current_weapon:
                color=(0,255,0)
            else:
                color=WHITE

            wep_text=font.render(f"[{index+1}] {weapon['name']} ({weapon['min_dmg']}-{weapon['max_dmg']} DMG)",True,color)
            screen.blit(wep_text,(WIDTH//2-200,y_offset))
            y_offset+=60

        close_text=font.render("Press [I] to close backpack",True,WHITE)
        screen.blit(close_text,(WIDTH//2-150,550))
    pygame.display.flip()
    clock.tick(60)


pygame.quit()