import json
import time
import random
import sched
import requests
from bs4 import BeautifulSoup
import os
import datetime
from PIL import Image

##This code looks at the provided URL and it's related webpage source before saving the image
##that likely has the enemy icon.

def download_page_source(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch webpage. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_image_url(page_source):
    if page_source:
        soup = BeautifulSoup(page_source, 'html.parser')
        # Find the meta tag with property="og:image"
        meta_tag = soup.find('meta', {'property': 'og:image'})
        if meta_tag and meta_tag.has_attr('content'):
            return meta_tag['content']
    return None

##This function saves the image
def save_image(image_url, folder, filename):
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Download the image
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(os.path.join(folder, filename), 'wb') as file:
                file.write(response.content)
            print(f"Image saved successfully as {filename}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while saving the image: {e}")

##Some URLs don't work. We save a blank image for the enemy icon in this case.
def save_blank_image(folder, filename):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Construct the full path to save the image
    filepath = os.path.join(folder, filename)
    # Create a new blank image with grey pixels
    image = Image.new('RGB', (200, 200), color=(128, 128, 128))
    # Save the image to the specified filepath
    image.save(filepath)
    print(f"Blank image saved as '{filename}' in folder '{folder}'.")

#The code for downloading.
def download_sprite(enemy_name, key):
    url =  "https://prts.wiki/w/" + enemy_name
    folder = "sprites"
    filename = str(key)+".png"
    page_source = download_page_source(url)
    if page_source:
        image_url = extract_image_url(page_source)
        if image_url:
            print(f"Found image URL: {image_url}")
            
            # Save the image with specified filename
            save_image(image_url, folder, filename)
            return True
        else:
            print("There was no image URL found with key ", key)
    print ("Could not download source!")
    return False
   
def check_png_exists(folder, filename):
    file_path = os.path.join(folder, filename)
    return os.path.exists(file_path) and os.path.isfile(file_path)

def icon_capture():
    # Opening JSON file
    f = open('enemy_database.json', encoding="UTF-8")
     
    # returns JSON object as a dictionary
    data = json.load(f)
     
    # Iterating through the json list
    #Our enemy data consists of a key, value (which distinguishes between lv0 and lv1), and stats
    #we'll take the lv0 value always, and then the stats
    for enemy in data['enemies']:
        key = enemy['Key']
        enemyData = enemy['Value'][0]['enemyData'] #we only work with the level:0 data
        name = enemyData['name']['m_value']
        print (key, ' ', name)
        ##We check if we already downloaded this sprite or not. If it hasn't, we'll download
        filename = str(key)+".png"
        folder = "sprites"
        if check_png_exists(folder, filename) == False:
            if download_sprite(name, key):
                min_delay = 5
                max_delay = 20
                delay = random.uniform(min_delay, max_delay) #implement a random delay to not get outed as a bot
                # Get the current time
                current_time = datetime.datetime.now()
                print("Current time:", current_time)
                
                time.sleep(delay)
            else:
                print ("This URL doesn't work! The enemy is not named correctly.")
                save_blank_image(folder, filename)
        else:
            print ("We already have this image!")
        
    # Closing file
    f.close()
    print ("Done!")

icon_capture()

# ##This program frequently gets stuck at a given URL. It works again if we rerun the program.
# ##This is code to make it automatically restart after 10 minutes.
# def repeat_function(sc):
#     icon_capture()
#     # Schedule the next call
#     scheduler.enter(600, 1, repeat_function, (sc,))

# # Create a scheduler instance
# scheduler = sched.scheduler(time.time, time.sleep)

# # Schedule the initial call of the function
# scheduler.enter(0, 1, repeat_function, (scheduler,))

# # Start the scheduler
# print("Program started.")
# scheduler.run()
