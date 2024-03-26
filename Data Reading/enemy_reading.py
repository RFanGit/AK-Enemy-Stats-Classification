import json

##In this program, we'll be reading in entries in cleaned_enemy_full.json
##And we'll be writing programs with a couple flags to only analyze specific enemies
 
def isnot_mainboss(key):
    if int(key[7]) <= 5:
        return True
    return False

def enemy_origin_filter(key, IS_enemy, Civ_enemy, Coop_enemy, AprilFool_enemy, SSS_enemy, RA_enemy, DOS_enemy):
    origin = key[6]
    if origin == "1":
        return True
    elif origin == "2" and IS_enemy:
        return True
    elif origin == "3" and Civ_enemy:
        return True
    elif origin == "4" and Coop_enemy:
        return True
    elif origin == "5" and AprilFool_enemy:
        return True
    elif origin == "6" and SSS_enemy:
        return True
    elif origin == "7" and RA_enemy:
        return True
    elif origin == "8" and DOS_enemy:
        return True
    return False

##We don't want any of those special enemies so set all the flags to false
IS_enemy = False
Civ_enemy = False
Coop_enemy = False
AprilFool_enemy = False
SSS_enemy = False
RA_enemy = False
DOS_enemy = False

# Opening JSON file
f = open('cleaned_enemy_full.json', encoding="UTF-8")
data = json.load(f)
enemies = []
for entry in data: ##Put all the enemy data into a list of dictionaries
    enemy_key = entry["Key"]
    # print (enemy_key)
    # print (enemy_key[6])
    if enemy_origin_filter(enemy_key, IS_enemy, Civ_enemy, Coop_enemy, AprilFool_enemy, SSS_enemy, RA_enemy, DOS_enemy):
        #print (enemy_key[7])
        if isnot_mainboss(enemy_key):
            enemies.append(entry) 
f.close()
print ("Done loading all the data!")

print ("The number of enemies remaining are ", len(enemies))

##Now we remove all the yellow variants of red enemies
def red_enemy_only(enemies):
    red_enemy_list = []
    for enemy in enemies:
        if enemy["Key"][-2:] == "_2": 
            #If this is a red enemy, then delete the enemy entry directly before
            red_enemy_list.pop()
        red_enemy_list.append(enemy)
    return red_enemy_list
red_enemies = red_enemy_only(enemies)

# print (red_enemies[0]["Key"])
# print (red_enemies[1]["Key"])
print ("The number of enemies remaining after removing yellow variants is ", len(red_enemies))

##we should have all the data now. We can print say the key of the first enemy
# print (enemies[0]["Key"])
# print (enemies[1]["Key"])
# print (enemies[1]["Key"][:-2])
# print (enemies[1]["Key"][-2:])
# print (enemies[1]["Key"][6])

##This goes through the dictionary and removes all elements from the dictionary
##that correspond to enemies that are not red

# def red_enemy_only(enemies):
#     red_enemy_list = []
#     for enemy in enemies:
#         if enemy["Key"][-2:] == "_2": 
#             #If this is a red enemy, then delete the enemy entry directly before
#             red_enemy_list.pop()
#         red_enemy_list.append(enemy)
#     return red_enemy_list
            

# no_boss = remove_mainboss(main_enemies)


# red_enemies = red_enemy_only(no_boss)

# print (red_enemies[0]["Key"])
# print (red_enemies[1]["Key"])



# def enemy_origin_filter(enemies, IS_enemy, Civ_enemy, Coop_enemy, AprilFool_enemy, SSS_enemy, RA_enemy, DOS_enemy):
#     filtered_list = []
#     for enemy in enemies:
#         origin = enemy["Key"][6]
#         if origin == 1:
#             filtered_list.append(enemy)
#         elif origin == 2 and IS_enemy:
#             filtered_list.append(enemy)
#         elif origin == 3 and Civ_enemy:
#             filtered_list.append(enemy)
#         elif origin == 4 and Coop_enemy:
#             filtered_list.append(enemy)
#         elif origin == 5 and AprilFool_enemy:
#             filtered_list.append(enemy)
#         elif origin == 6 and SSS_enemy:
#             filtered_list.append(enemy)
#         elif origin == 7 and RA_enemy:
#             filtered_list.append(enemy)
#         elif origin == 8 and DOS_enemy:
#             filtered_list.append(enemy)
#     return filtered_list
    
# IS_enemy = False
# Civ_enemy = False
# Coop_enemy = False
# AprilFool_enemy = False
# SSS_enemy = False
# RA_enemy = False
# DOS_enemy = False
# main_enemies = enemy_origin_filter(enemies, IS_enemy, Civ_enemy, Coop_enemy, AprilFool_enemy, SSS_enemy, RA_enemy, DOS_enemy)

    
