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


## Code for analyzing the attack movespeed pairs
## Clustering function: we create clusters based off only attack and movespeed
def distance_atkmvspd(cluster1, cluster2): #Computes the distance between two clusters
    atkspdweight = 0.7
    mvspd1 = cluster1[0][0]
    atkspd1 = cluster1[0][1]
    mvspd2 = cluster2[0][0]
    atkspd2 = cluster2[0][1]
    return atkspdweight *(atkspd1 - atkspd2)**2 + (mvspd1 - mvspd2)**2

##Calculcates the closest valid clusters
##merged is a list that keeps track of which clusters have already been merged
##and thus cannot be merged again
def closest_calc(clusters, merged):
    cluster_num = len(clusters)
    dmat = np.zeros((cluster_num, cluster_num))
    lowest_dist = 99999990 #we assume all things will be closer than this
    closest = (0, 0)
    for i in range(cluster_num):
        if merged[i] == 0:
            # mvspd1 = atkmvspd_list[i][0][0]
            # atkspd1 = atkmvspd_list[i][0][1]
            cluster1 = clusters[i]
            for j in np.arange(i+1, cluster_num):
                if merged[j] == 0:
                    # mvspd2 = atkmvspd_list[j][0][0]
                    # atkspd2 = atkmvspd_list[j][0][1]
                    cluster2 = clusters[j]
                    dmat[i, j] = distance_atkmvspd(cluster1, cluster2)
                    if lowest_dist > dmat[i, j]:
                        lowest_dist = dmat[i, j]
                        closest = (i, j)
    return dmat, closest, lowest_dist

##Merges two clusters from the list of clusters with index1, index2
##The resulting cluster has the avg atkspd and mvspd of the intermediates
def merge_cluster(clusters, index1, index2):
    oldaspd1 = clusters[index1][0][1]
    oldaspd2 = clusters[index2][0][1]
    oldmvspd1 = clusters[index1][0][0]
    oldmvspd2 = clusters[index2][0][0]
    oldkeys1 = clusters[index1][1]
    oldkeys2 = clusters[index2][1]
    size1 = len(oldkeys1)
    size2 = len(oldkeys2)
    newatkspd = (oldaspd1*size1 + oldaspd2*size2) / (size1 + size2)
    newmvspd = (oldmvspd1*size1 + oldmvspd2*size2) / (size1 + size2)
    newkeys = oldkeys1 + oldkeys2
    newtuple = (newmvspd, newatkspd)
    newclusterlist = [[newtuple, newkeys]]
    #print (newclusterlist)
    clusters = clusters + newclusterlist
    new_cluster_size = size1 + size2
    return clusters, new_cluster_size

##Finds the closest clusters, merges them, keeps track of the merge
##Returns the new list of clusters, a list stating which clusters have been merged, and the history of merges 
def clusterstep(clusters, merged):
    dmat, closest, lowest_dist = closest_calc(clusters, merged)
    index1 = closest[0]
    index2 = closest[1]
    clusters, new_cluster_size = merge_cluster(clusters, index1, index2)
    merged[index1] = 1 #These clusters have been merged and thus should not be considered for future merges
    merged[index2] = 1
    newmerge = np.array([index1, index2, lowest_dist, new_cluster_size])
    return clusters, merged, newmerge

##Merge clusters number_of_merges times.
##Returns all historical clusters, which clusters have been merged
##the history of merges, and the total number of merges done
def agglom_cluster(clusters, merged, number_of_merges):
    if len(clusters) == number_of_merges:
        print ("This is impossible! We can't perform that many merges.")
    clusters, merged, merge_hist = clusterstep(clusters, merged)
    mergenumber = 1
    while mergenumber < number_of_merges:
        clusters, merged, newmerge = clusterstep(clusters, merged)
        merge_hist = np.vstack([merge_hist, newmerge])
        mergenumber += 1
    return clusters, merged, merge_hist, mergenumber

##Using the historical list of clusters and the merge history
##reconstructs the clusters existing after a certain number of merges have occurred.
def merged_clusters(clusters, merge_hist, number_of_merges):
    indices_to_remove = []
    ##Removing the clusters that have been merged at this time
    for cyc1 in range(number_of_merges):
        indices_to_remove.append((int)( merge_hist[cyc1, 0]))
        indices_to_remove.append((int)( merge_hist[cyc1, 1]))
    ##Removing clusters that exist in the future of this specific time
    total_cluster_number = len(clusters)
    initial_cluster_number = total_cluster_number - len(merge_hist)
    for cyc2 in np.arange(initial_cluster_number + number_of_merges, total_cluster_number):
        indices_to_remove.append((int)(cyc2))
    new_clusters = [elem for i, elem in enumerate(clusters) if i not in indices_to_remove]
    return new_clusters

##Returns the first merge to occur between clusters of a certain distance apart
def close_merge_find(distance, merge_hist):
    number_of_merges = len(merge_hist)
    close_merge_ind = -1
    for cyc in range(number_of_merges):
        if merge_hist[cyc][2] >= distance and close_merge_ind == -1: #if this merge was between clusters more distant than distance
            close_merge_ind = cyc
    return close_merge_ind

##From the list of indices (corresponding to entries in the original dictionary, data)
##we randomly pick N of them and obtain their key names
def random_keys(data, indices, N):
    if N > len(indices):
        raise ValueError("N should not exceed the number of available indices.")
    # Select N random indices without replacement
    selected_indices = random.sample(indices, N)
    image_names = []
    for cyc1 in range(N):
        image_names.append(data[selected_indices[cyc1]]["Key"])
    return image_names

##From a list of image names and a sprite folder location
##display the images in a row
def display_images(image_names, sprites_folder, counter):    
    num_images = len(image_names)
    if num_images > 1:
        fig, axes = plt.subplots(1, num_images, figsize=(2*num_images, 2))
        for i, image_name in enumerate(image_names):
            # Open the image file
            img = Image.open(sprites_folder+image_name+".png")
            axes[i].imshow(img)
            axes[i].axis('off') 
    else:
        fig = plt.figure(figsize = (2, 2))
        img = Image.open(sprites_folder+image_names[0]+".png")
        plt.axis('off')
        plt.imshow(img)
    
    # Adjust layout to prevent overlapping
    plt.tight_layout()
    fig_num = "clusters\\" +str(counter)+".png"
    plt.savefig(fig_num)
    plt.show()
    
def display_clusters(clusters, displaynum):
    number = len(clusters)
    sprites_folder = '..\sprites LQ\\'
    for cyc1 in range(number):
        print ("Cluster number ", cyc1)
        print ("This cluster has average (mvspd, atkint) ", clusters[cyc1][0] ,' with ', len(clusters[cyc1][1]) ," members.")
        print ("The keys are ", clusters[cyc1][1])
        display_images_num = min(len(clusters[cyc1][1]), displaynum)
        listofkeys = random_keys(enemies, clusters[cyc1][1], display_images_num)
        #print (listofkeys)
        display_images(listofkeys, sprites_folder, cyc1)
        
        #We'll save the cluster data into a txt too
        file_name = "clusters\\keys" +str(cyc1)+".txt"
        np.savetxt(file_name, clusters[cyc1][1])
        
        file_name2 = "clusters\\params" +str(cyc1)+".txt"
        np.savetxt(file_name2, clusters[cyc1][0])
    
# Convert dictionary to a list of lists (key-value pairs)
atkmvspd_list = [[key, value] for key, value in atkmvspd_pairs.items()]

##example of how to read this data
# print (atkmvspd_list[0]) ##raw entry
# print (atkmvspd_list[0][0]) ##attack movespeed tuple
# print (atkmvspd_list[0][0][0]) #attack interval
# print (atkmvspd_list[0][0][1]) #movespeed
# print (atkmvspd_list[0][1]) #indices for entries in enemies with this attack interval and movespeed

##the maximum number of possible clusters
merged = np.zeros(2*pair_num)

##Agglomerative clustering, merge 170 clusters (which is 1 less than the total number of clusters, 171)
clusters, merged, merge_hist, mergenumber = agglom_cluster(atkmvspd_list, merged, 170)

# fig = plt.figure(figsize = (25, 10))
# dn = dendrogram(merge_hist)
# plt.savefig("Arknights Enemy Dendrogram.png")

distance = 0.05 #This seems most effective
close_merge_ind = close_merge_find(distance, merge_hist)
print ("At merge number ", close_merge_ind, " we started merging clusters more than ", distance ," distance apart.")
print ("If we stop merging at this cluster number, our resulting clusters are:")

new_clusters = merged_clusters(clusters, merge_hist, close_merge_ind)
displaynum = 5
display_clusters(new_clusters, displaynum)


        