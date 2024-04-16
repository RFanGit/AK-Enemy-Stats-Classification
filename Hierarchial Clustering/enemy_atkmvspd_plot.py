import json
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image
from scipy.cluster.hierarchy import dendrogram

##Reading in enemy data
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
    if int(key[7]) < 5:
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

##We now have all the attack movespeed pairs in our data
pair_num = len(atkmvspd_pairs)
print ("There are ", pair_num, " number of unique move speed + attack interval pairs.")

x_coords = []
y_coords = []
sizes = []
# Sample data (list of tuples and lists)
for atkmvspd in atkmvspd_pairs:
    x_coords.append(atkmvspd[0])
    y_coords.append(atkmvspd[1])
    sizes.append(np.size(atkmvspd_pairs[atkmvspd])*10)
    #print (atkmvspd)
    #print (atkmvspd_pairs[atkmvspd])

#colors = np.random.rand(len(x_coords), 3)  # Generate random RGB values for each data point

# Set figure size
plt.figure(figsize=(12, 12))  # Adjust the width and height as needed

# Plot data points
plt.scatter(x_coords, y_coords, s=sizes, color='blue', alpha=0.7)

# Add labels and title
plt.xticks(fontsize=20)  # Adjust the fontsize as needed
plt.yticks(fontsize=20)  # Adjust the fontsize as needed

plt.xlabel('Movement Speed', fontsize = 30)
plt.ylabel('Attack Interval', fontsize = 30)
plt.title('Arknights Enemy Data', fontsize = 50)

# Save the plot
plt.grid(True)
plt.savefig('Arknights Enemy Stats Scatterplot.png')  # Save the plot as a PNG file
plt.show()


# Set figure size
plt.figure(figsize=(12, 12))  # Adjust the width and height as needed

# Plot data points
plt.scatter(x_coords, y_coords, s=np.array(sizes)*3, color='blue', alpha=0.7)

# Add labels and title
plt.xlim(0, 3)
plt.ylim(0, 8)


plt.xticks(fontsize=20)  # Adjust the fontsize as needed
plt.yticks(fontsize=20)  # Adjust the fontsize as needed

plt.xlabel('Movement Speed', fontsize = 30)
plt.ylabel('Attack Interval', fontsize = 30)
plt.title('Arknights Enemy Data', fontsize = 50)

# Save the plot
plt.grid(True)
plt.savefig('Arknights Enemy Stats Scatterplot_focused.png')  # Save the plot as a PNG file
plt.show()