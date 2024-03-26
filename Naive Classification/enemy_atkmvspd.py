import json
import numpy as np
import matplotlib.pyplot as plt
import random
import os
from PIL import Image

##Pseudocode
##The most similar features of enemy types are their movespeed and attack intervals.
##We'll thus list all enemies which have the same pairs as well as their indices.
 
##Function that removes all the yellow variants of red enemies
def red_enemy_only(enemies):
    red_enemy_list = []
    for enemy in enemies:
        if enemy["Key"][-2:] == "_2": 
            #If this is a red enemy, then delete the enemy entry directly before
            red_enemy_list.pop()
        red_enemy_list.append(enemy)
    return red_enemy_list

def isnot_mainboss(key): #Remove standard bosses
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
enemies = red_enemy_only(enemies)
enemycount = len(enemies)

##We got through all the enemies and create a dictionary of atk/mmvspeed pairs
##This dictionary contains a list for each entry of all the keys.
atkmvspd_pairs = {}
for cyc in range(enemycount):
    state = enemies[cyc]["moveSpeed"], enemies[cyc]['baseAttackTime']
    if state in atkmvspd_pairs:
        atkmvspd_pairs[state].append(cyc)
    else:
        atkmvspd_pairs[state] = [cyc]  

pair_num = len(atkmvspd_pairs)
print ("There are ", pair_num, " number of unique move speed + attack interval pairs.")

##make this into a code that checks the number of pairs with a certain number of elements
##and plot how the number decreases as we impose popularity
##also have code that can print the members.

def min_pops(dictionary, min_val):
    popular_pairs = []
    for pairval, numpairs in dictionary.items():
        if len(numpairs) > min_val:
            popular_pairs.append(pairval)
    return popular_pairs, len(popular_pairs)

##we have a list of indices, we randomly pick 5 of them, and then proceed
def random_keys(data, indices, N):
    if N > len(indices):
        raise ValueError("N should not exceed the number of available indices.")
    # Select N random indices without replacement
    selected_indices = random.sample(indices, N)
    #print (selected_indices)
    image_names = []
    for cyc1 in range(N):
        image_names.append(data[selected_indices[cyc1]]["Key"])

    return image_names

def display_images(image_names, sprites_folder):
    num_images = len(image_names)
    fig, axes = plt.subplots(1, num_images, figsize=(3*num_images, 3))
    for i, image_name in enumerate(image_names):
        # Open the image file
        img = Image.open(sprites_folder+image_name+".png")
        axes[i].imshow(img)
        axes[i].axis('off') 
    
    # Adjust layout to prevent overlapping
    plt.tight_layout()
    plt.show()

pair_sizes = 50
popularity = np.zeros(pair_sizes)

pairs, _ = min_pops(atkmvspd_pairs, 10)
#print (pairs)

for cyc in range(pair_sizes):
    _, popularity[cyc] = min_pops(atkmvspd_pairs, cyc)

# for pop in popular_pairs2:
#     print (pop, ' ', atkmvspd_pairs[pop])

print (popularity)

fig, ax = plt.subplots(figsize=[12, 9])
ax.tick_params(axis='both', which='major', labelsize=20)
ax.xaxis.set_major_locator(plt.MaxNLocator(5))

plt.plot(range(pair_sizes), popularity, lw = 5)
ax.set_xlabel(r"Minimum Number of Elements", fontsize = 37)
ax.set_ylabel(r'Number of (MV/ATK) SPD pairs', fontsize = 37)
plt.xlim(0, 25)
plt.ylim(0, 200)
plt.show()

fig, ax = plt.subplots(figsize=[12, 9])
ax.tick_params(axis='both', which='major', labelsize=20)
ax.xaxis.set_major_locator(plt.MaxNLocator(5))

plt.plot(range(pair_sizes), popularity, lw = 5)
ax.set_xlabel(r"Minimum Number of Elements", fontsize = 37)
ax.set_ylabel(r'Number of (MV/ATK) SPD pairs', fontsize = 37)
plt.title(r'Number of (MV/ATK) SPD pairs', fontsize = 37)
plt.xlim(5, 20)
plt.ylim(0, 25)
plt.show()

#Let's see how many categories have 5 enemies
min_encount = 5
pop_pair, number = min_pops(atkmvspd_pairs, min_encount)
print ("The number of atk movespeed pairs with at least ", min_encount, " enemies are ", number)
#print (pop_pair)
for cyc1 in range(number):
    print (pop_pair[cyc1], ' ', atkmvspd_pairs[pop_pair[cyc1]])
    #print (cyc)

sprites_folder = '..\Sprite Collection\sprites\\'
print (sprites_folder)

# Find the random keys for a given list of indices and then display them 
listofkeys = random_keys(enemies, atkmvspd_pairs[pop_pair[0]], 3)
display_images(listofkeys, sprites_folder)

        