import json
import numpy as np


##Pseudocode
##The most similar features of enemy types are their movespeed and attack intervals.
##We'll thus try to classify the enemies into types based off these parameters.
##We'll also allow for a small dependence on HP.
##To compute the distance between two clusters, we'll thus use

## (movespeed1 - movespeed2)**2 + weightA*(atkint1 - atkint2)**2 + weightB*(HP1 - HP2)**2

##Where weight B is relatively small, and weight A is less than 1.
##We normalize movespeed, atkint, and HP, so that excessive values doesn't affect our results

##Because a large number of arknights enemies are unique, whereas known enemy types might have
##small numerical differences, we'll want to increase the cost of merging large clusters together.
##To do this, we'll multiple the 'distance' between two clusters by a factor proportional to the size
##of the small cluster. We'll choose the square root of the number of elements in the smaller cluster.

##So the distance between two clusters is (using their respective average stats):
## ((movespeed1 - movespeed2)**2 + weightA*(atkint1 - atkint2)**2 + weightB*(HP1 - HP2)**2) 
##*sqrt(min (cluster_num))
##we then merge clusters that are closest. To compute the new average movespeed, atk interval, and HP are easier
##since we multiply both by the number of elements, add, and divide by the number of elements


##Unfortunately this is a very customized clustering algorithm. The obvious scipy options
##don't support these custom methods for making clusters and custom distances, so we'll
##have to write our own algorithm.
 
# Opening JSON file
f = open('cleaned_enemy.json', encoding="UTF-8")
 
# returns JSON object as a dictionary
data = json.load(f)

##Parameters from each enemy that we'll actually use in training
enemycount = len(data) 
enemies = []

index = 0
for entry in data: ##We all the enemy data into a dictionary
    enemies.append(entry) 
# Closing file
f.close()
print ("Done!")

##we should have all the data now. We can print say the key of the first enemy
print (enemies[0]["Key"])

##Now we begin clustering. 
def cluster_distance(cparams1, cparams2):
    movespeeds_diff = (cparams1['moveSpeed'] - cparams2['moveSpeed'])**2
    atkint_diff = (cparams1['baseAttackTime'] - cparams2['baseAttackTime'])**2
    hp_diff = (cparams1['maxHp'] - cparams2['maxHp'])**2
    min_elem = min(cparams1['Elements'], cparams2['Elements'])
    weight1 = 0.5
    weight2 = 0.1
    return (movespeeds_diff + weight1*atkint_diff + weight2*hp_diff)*np.sqrt(min_elem)

##Our data structure for clusters has 5 parameters
#numbers for mvspd, atk, hp, and number of elements
#and finally a list of strings of the original indices of all elements in the cluster.

##Here, we convert our dictionaries into clusters
clusters = []
for cyc in range(enemycount):
    cluster = {
        'moveSpeed': enemies[cyc]['moveSpeed'],
        'baseAttackTime': enemies[cyc]['baseAttackTime'],
        'maxHp': enemies[cyc]['maxHp'],
        'Elements': 1,
        'Members': cyc}
    clusters.append(cluster)
print (clusters[0])

##We first go through each element, and compute it's distance with every other element.
##Then we look for the closest pair, and merge those two.
##We then remove those pairs elements from the distance matrix, pass it on to the function again
##and generate the distances for the new cluster to everything else, and then look for the minimum again

##At what part do we do recursion...
    
    
