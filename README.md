# AK-Enemy-Stats-Classification
We perform hierarchial clustering on enemies in the live service mobile game Arknights to put them into categories based off their stats, and infer how their stats have increased over the lifetime of the game.

The source for our enemy data is taken from: https://github.com/Kengxxiao/ArknightsGameData/tree/master/zh_CN/gamedata/levels/enemydata

The sprites collected for visuals are taken from https://prts.wiki/. This was done using enemy_data_spritecollector_run.py, which often slows down when collecting the images and is not that reliable. Because of filezsize limitations, the resulting sprites were reduced in quality and zipped up in sprites LQ.7z. You unzip this into a folder called sprites LQ and the rest of the programs can access and use the images.

# Table of Contents

Data Reading contains a basic program for reading a cleaned enemy json file.
Hierarchial Clustering contains 

# Enemy Numbering

From the json file, we observe that enemies can be broadly classified based on number:

1000-1500 - Normal enemies in the main game (Except Big Bob)
1500-2000 - Boss Enemies (except Big Bob, who was likely an early creation)
2000-3000 - IS enemies
3000-4000 - Civilians (Talulah)
4000-5000 - Coop Enemies
5000-6000 - April Fools Event Enemies
6000-7000 - SSS Enemies
7000-8000 - RA Enemies
8000-9000 - DDOS Enemies

This analysis will focus on 1000-1500. This is because:
1. Boss enemies (1500-2000) are unique and classifying them into clusters with the rest of the enemies serves no purpose
2. 2000-9000 often consist of special enemies that are not useful to classify, such as civilians, bosses, or enemies whose stats are designed for external modifiers

# Data Cleaning

We clean the 

# Classification Method

It is difficult to classify enemies by stats while also being able to make meaningful judgements on the change in stats. However, many enemies in Arknights share similar movespeed and attack intervals, with weaker enemies possessing high movespeed and low attack intervals, together with stronger enemies that move slowly and attack infrequently. We will thus classify enemies based off these two parameters and observe the results.

Furthermore, many enemies in Arknights come in two variants (normal and red), the latter of which are versions of the former but with higher ATK, HP and DEF values. These red variants appear in the harder stages. To keep this analysis most relevant to players at high difficulty, we will modify our program to only track the stats of red enemies.

## Naive Classification

As a preliminary analysis, we classify all the enemies into groups based off their atk interval and movement speed. After eliminating 1500-9000 from our list and removing non-red variants, we are left with 438 enemies left. These 438 enemies correspond to 171 unique atk/mvspd pairs. Howeve, it is premature to stop the analysis here, since many of these 171 pairs are very similar in value
