import json
import numpy as np

 
# Opening JSON file
f = open('cleaned_enemy.json', encoding="UTF-8")
 
# returns JSON object as a dictionary
data = json.load(f)
 
for entry in data:
    print (entry['Key'])


    
# Closing file
f.close()
print ("Done!")
