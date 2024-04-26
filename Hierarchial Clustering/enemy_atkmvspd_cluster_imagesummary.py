import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Function to create a blank canvas with given width and height
def create_canvas(width, height, background_color=(255, 255, 255)):
    return Image.new("RGB", (width, height), background_color)

# Function to add text to the canvas
def add_text(canvas, text, position, font_path, font_size, text_color=(0, 0, 0)):
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("arial.ttf", font_size)  # Use Arial font
    draw.text(position, text, fill=text_color, font=font)
    _, text_height = draw.textsize(text, font=font)
    return text_height

def truncate_tuple(tup):
    truncated_values = [f"{value:.2f}" for value in tup]
    return "(" + ", ".join(truncated_values) + ")"

# Function to combine images and save as a single image
def combine_images(number_of_files, output_path, canvas_width, canvas_height, font_path, font_size, input_directory):
    num_images = (int)(number_of_files/3)
    num_columns = 4
    num_rows = (num_images + 1) // 4  # Adjust for odd number of images

    canvas = create_canvas(canvas_width, canvas_height)
    
    #print (num_images)
    
    for i in range(num_images):
        col = i % num_columns
        row = i // num_columns
        
        x = col * (canvas_width // num_columns)
        y = row * (canvas_height // num_rows)
        
        ##Our files
        textpath = input_directory + "\\keys" + str(i) + ".txt"
        imagepath = input_directory + "\\"+str(i) + ".png"
        clusterpath = input_directory + "\\params" + str(i) + ".txt"
        
        params = np.loadtxt(clusterpath)
        keys = np.loadtxt(textpath)
        image = Image.open(imagepath)
        #print (keys)
        
        id_str = "Cluster " + str(i) #+ "\nMv Spd, Atk Int = " + truncate_tuple(params)
        param_str = truncate_tuple(params)#"Mv Spd, Atk Int = " + truncate_tuple(params)
        key_str = str(np.size(keys)) + " Elements"
        text_height1 = add_text(canvas, id_str, (x, y), font_path, font_size = 40)
        text_height2 = add_text(canvas, param_str, (x, y + text_height1 + 10), font_path, font_size = 30)
        text_height3 = add_text(canvas, key_str, (x, y + text_height1 + text_height2 + 10), font_path, font_size = 30)
        
        image.thumbnail((canvas_width // num_columns, canvas_height // num_rows - text_height1*2))
        canvas.paste(image, (x, y + text_height1*3))

    # Save combined image
    canvas.save(output_path)
# Main function
def main():
    # Directory containing numbered images and text files
    input_directory = "clusters"

    # Output directory
    output_directory = "cluster_summary"
    os.makedirs(output_directory, exist_ok=True)

    # Populate the list with paths of numbered images and text files
    number_of_files = 0
    for filename in sorted(os.listdir(input_directory)):
        number_of_files += 1
            
    # Parameters for the combined image
    canvas_width = 2000
    canvas_height = 100*(int)(number_of_files/4)
    
    font_path = None
    font_size = 24

    # Combine images and save as a single image
    output_path = os.path.join(output_directory, "combined_image.png")
    combine_images(number_of_files, output_path, canvas_width, canvas_height, font_path, font_size, input_directory)
        
    print("Combined image saved at:", output_path)

if __name__ == "__main__":
    main()