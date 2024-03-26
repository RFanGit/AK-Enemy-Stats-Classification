import json
import numpy as np

def stat_acquisition(enemydata_table, attribute_type):
    enemy_attribute = enemydata_table[attribute_type]
    #print (enemy_attribute['m_defined'])
    if enemy_attribute['m_defined']:
        return enemy_attribute['m_value']
    return -1

def json_pack(key, name, attributes_to_save, atts):
    cleaned_enemy = {
            'Key': key,
            'Name': name,
        }
    for aspect, value in zip(attributes_to_save, atts):
        cleaned_enemy[aspect] = value
    return cleaned_enemy
 
# Opening JSON file
f = open('enemy_database.json', encoding="UTF-8")
 
# returns JSON object as a dictionary
data = json.load(f)
cleaned_enemydata = []
 
# Iterating through the json list
#Our enemy data consists of a key, value (which distinguishes between lv0 and lv1), and stats
#we'll take the lv0 value always, and then the stats
for enemy in data['enemies']:
    key = enemy['Key']
    enemyData = enemy['Value'][0]['enemyData'] #we only work with the level:0 data
    name = enemyData['name']['m_value']
    #print (key, ' ', name)
    
    ##What data do we want to save from the level 0 data? first the attributes
    attributes = enemyData['attributes']
    
    attributes_to_save = ["maxHp", "atk", "def", "magicResistance", "blockCnt", "moveSpeed", "attackSpeed", "baseAttackTime", "hpRecoveryPerSec","spRecoveryPerSec","massLevel","tauntLevel","epDamageResistance","epResistance","damageHitratePhysical","damageHitrateMagical","stunImmune","silenceImmune","sleepImmune","frozenImmune","levitateImmune", "disarmedCombatImmune"]
    attribute_num = len(attributes_to_save)
    atts = np.zeros(attribute_num)
    for att_num in range(attribute_num):
        atts[att_num] = stat_acquisition(attributes, attributes_to_save[att_num])
        #print (attributes_to_save[att_num], ' ', stat_acquisition(attributes, attributes_to_save[att_num]))
    cleaned_enemydata.append(json_pack(key, name, attributes_to_save, atts))
    
    
with open('cleaned_enemy_full.json', 'w') as file:
    json.dump(cleaned_enemydata, file, indent = 2)
    
# Closing file
f.close()
print ("Done!")
