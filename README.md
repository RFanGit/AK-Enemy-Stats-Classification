# AK-Enemy-Stats-Classification
We perform hierarchial clustering on enemies in the live service mobile game Arknights to put them into categories based off their stats, and infer how their stats have increased over the lifetime of the game.

The source for our enemy data is taken from: https://github.com/Kengxxiao/ArknightsGameData/tree/master/zh_CN/gamedata/levels/enemydata

The sprites collected for visuals are taken from https://prts.wiki/. This was done using enemy_data_spritecollector_run.py, which often slows down when collecting the images and is not that reliable. Because of filezsize limitations, the resulting sprites were reduced in quality and zipped up in sprites LQ.7z. You unzip this into a folder called sprites LQ and the rest of the programs can access and use the images.

# Table of Contents

Raw Data Cleaning contains a program that cleans the enemy data json file, producing a smaller json file that contains only basic statistics (Health, Attack, Defense, Resistance, Movespeed, etc). 

Analysis occurs in Hierarchial Clustering, which contains three programs which visualize the data in different ways. Plot visualizes enemy attack intervals and movespeed data as a scatterplot, clustering saves the data as individual clusters to clusters which can be inspected in detail, and cluster_imagesummary produces an image in cluster summary to summarize the results. These can be run independently to observe each visualization.

# Methods

It is difficult to classify enemies by stats while also being able to make meaningful judgements on the change in stats. However, many enemies in Arknights share similar movespeed and attack intervals, with weaker enemies possessing high movespeed and low attack intervals, together with stronger enemies that move slowly and attack infrequently. We thus attempt to classify the enemies based off these two parameters.

Furthermore, many enemies in Arknights come in two variants (normal and red), the latter of which are versions of the former but with higher ATK, HP and DEF values. These red variants appear in the harder stages. To keep this analysis most relevant to players at high difficulty, we will modify our program to only track the stats of red enemies.

These procedures leave 438 enemies, which correspond to 171 unique atk/mvspd pairs. We attempt to cluster similar groups of atk/mvspd pairs, since many of these groups are fairly similar.

# Results

Our resulting clusters are summarized in the following image:

![alt text](https://raw.githubusercontent.com/RaymondFanGit/AK-Enemy-Stats-Classification/Update/Hierarchial%20Clustering/cluster_summary/Cluster%20Summary%20Fin.png)


# Enemy Numbering

From the json file, we observe that enemies can be broadly classified based on number:

1. 1000-1500 - Normal enemies in the main game (Except Big Bob)
2. 1500-2000 - Boss Enemies (except Big Bob, who was likely an early creation)
3. 2000-3000 - IS enemies
4. 3000-4000 - Civilians (Talulah)
5. 4000-5000 - Coop Enemies
6. 5000-6000 - April Fools Event Enemies
7. 6000-7000 - SSS Enemies
8. 7000-8000 - RA Enemies
9. 8000-9000 - DDOS Enemies

This analysis will focus on 1000-1500. This is because:
1. Boss enemies (1500-2000) are unique and classifying them into clusters with the rest of the enemies serves no purpose
2. 2000-9000 often consist of special enemies that are not useful to classify, such as civilians, bosses, or enemies whose stats are designed for external modifiers
