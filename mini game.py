import time

def show_instruction():
    print("--- 🏰 ESCAPE THE HAUNTED HOUSE 🏰 ---")
    print("Commands:")
    print("  go [direction] (north, south, east, west)")
    print("  get [item]")
    print("  quit")
    print("Goal: Find the key and reach the Garden to escape!")
    print("------------------------------------------")

def show_status(current_room,inventory,rooms):
    print("\n--------------------")
    print(f"You are in the {current_room}")
    print(f"Inventory:{inventory}")
    
    print("This is what you see...")
    for x,y in rooms[current_room].items():
        print(x,":",y)
    print("-------------------------")

def play_game():
    rooms ={
        'Hall':{
            'south':'Kitchen',
            'east':'Dining Room',
            'item':'key'
        },
        'Kitchen':{
            'north':'Hall',
            'item':'monster'
        },
        'Dining Room':{
            'west':'Hall',
            'south':'Garden',
            'item':'portion'
        },
        'Garden':{
            'north':'Dining Room'
        }
    }

    current_room='Hall'
    inventory =[]
    show_instruction()

    while True:
        show_status(current_room,inventory,rooms)

        move=input("What do you want to do(quit or go or get)? > ").lower().strip().split()

        if not move:
            continue

        action = move[0]

        if action=="quit":
            print("You gave up, thanks for playing")
            break

        elif action=="go":
            if len(move)<2:
                print("go where?(north,south,east, or west)")
                continue

            direction = move[1]
            if direction in rooms[current_room]:
                current_room=rooms[current_room][direction]
                print("Walking...")
                time.sleep(3)
            else :
                print("You cannot go that way")
        
        elif action=="get":
            if len(move)<2:
                print("Get What?")
                continue

            item = move[1]
            if 'item' in rooms[current_room] and item == rooms[current_room]['item']:
                inventory.append(item)
                print(f"You picked up the {item}!")
                del rooms[current_room]['item']
            else:
                print(f"There is no {item} there")
        
        else:
            print("I do not understand that command")

        if current_room=='Kitchen' :
            if 'portion' in inventory:
                print("\n A terrible monster hurt you and you heal yourself with the portion.")
                inventory.remove('portion')
                print("Portion used...")
                time.sleep(3)
                print("You run back to Hall")
                current_room= "Hall"
                time.sleep(3)
            else:
                print("\n💀 A terrible monster eats you! GAME OVER.")
                break

        if current_room == 'Garden':
            if 'key' in inventory:
                print("\nYou unlock the garden gate and escape!@!@@!!")
                break
            else:
                print("The gate is locked and you need to find the key")
                print("You walked back to dining room.")
                current_room='Dining Room'
                time.sleep(3)

play_game()