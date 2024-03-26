# AK-Enemy-Stats-Classification
We classify enemies in the live service mobile game Arknights into categories based off their stats, and infer how their stats have increased over the lifetime of the game.

The source for our enemy data is taken from: https://github.com/Kengxxiao/ArknightsGameData/tree/master/zh_CN/gamedata/levels/enemydata

The sprites collected for visuals are taken from https://prts.wiki/. This was done using the enemy_data_spritecollector_run.py, which often slows down when collecting the images and is not that reliable. Because of filezsize limitations, the resulting sprites were reduced in quality and zipped up in sprites LQ.7z. You unzip this into a folder called sprites LQ and the rest of the programs can access and use the images.
