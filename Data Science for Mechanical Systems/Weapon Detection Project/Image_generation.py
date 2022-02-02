from os import path, mkdir, makedirs
from PIL import Image
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
import concurrent.futures
import os
import threading
import random

#creating all the class output subfolders if not already present
output_folder = "output/a"
if not path.exists(output_folder):
    os.makedirs(output_folder)
output_folder = "output/b"
if not path.exists(output_folder):
    os.makedirs(output_folder)
output_folder = "output/c"
if not path.exists(output_folder):
    os.makedirs(output_folder)
output_folder = "output/d"
if not path.exists(output_folder):
    os.makedirs(output_folder)

#defining two variables based on the options available for creating the images
police_options = ['equipped_p','unarmed_p']
civilian_options = ['equipped_c','unarmed_c']

#counting the number of image vectors available for each of the image elements
backgrounds_count = 0
equipped_p_count = 0
unarmed_p_count = 0
equipped_c_count = 0
unarmed_c_count = 0
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        #print(os.path.join(root, name))
        if "backgrounds" in os.path.join(root, name):
            backgrounds_count += 1
        if "equipped_c" in os.path.join(root, name):
            equipped_c_count += 1
        if "unarmed_c" in os.path.join(root, name):
            unarmed_c_count += 1
        if "equipped_p" in os.path.join(root, name):
            equipped_p_count += 1
        if "unarmed_p" in os.path.join(root, name):
            unarmed_p_count += 1
terrorist_count = equipped_c_count + unarmed_c_count
police_count = equipped_p_count + unarmed_p_count

def generate_image(classes, background_file_name, police_file_name, civilian_file_name, file_name): #function for generating one image based on arguments indicating presence of various elements
    background_file = path.join("backgrounds", background_file_name) #background file path
    background_image = Image.open(background_file) #open background image in pillow
    background_image = background_image.resize((1920,1080)) #set resolution for background image

    police_character_file = path.join("characters/police_chars", police_file_name) #police image file path
    police_character_image = Image.open(police_character_file)#open police image in pillow
    police_character_image = police_character_image.resize((int(police_character_image.size[0]/3),int(police_character_image.size[1]/3))) #set resolution for police image
    police_character_coordinates = (int(1920/2-police_character_image.width*1.6), int(1080-police_character_image.height*1.1)) #x, y co-ordinates for police image
    
    civilian_character_file = path.join("characters/civilian_chars", civilian_file_name)#civilian image file path
    civilian_character_image = Image.open(civilian_character_file)#open civilian image in pillow
    civilian_character_image = civilian_character_image.resize((int(civilian_character_image.size[0]/3),int(civilian_character_image.size[1]/3)))#set resolution for civilian image
    civilian_character_coordinates = (int(1920/2+civilian_character_image.width*1.6), int(1080-civilian_character_image.height)) #x, y co-ordinates for civilian image
    
    background_image.paste(police_character_image, police_character_coordinates, mask=police_character_image) #paste police image onto background
    background_image.paste(civilian_character_image, civilian_character_coordinates, mask=civilian_character_image) #paste civilian image onto background
    
    output_file = path.join("output/"+classes, f"{file_name}") #create output path based on arguments and classes
    background_image.save(output_file) #save to the output directory

def generate_random_imgs(total_imgs,num): #function for generating multiple images as passed through arguments
    df = pd.DataFrame(columns = ["image", "class", "civilian_present?", "civilian_armed?", "police_present?","police_armed?", "action"]) #create a table for  future reference
    for img in tqdm(range(num, num+total_imgs)): #running for the number of iterations as chosen
        background_character_number = random.randint(0,backgrounds_count-1) #choose a random background image
        background_file_name = "background" + str(background_character_number) + ".png" #find the background image in the input folder
        police_option = random.choice(police_options) #choose a random police image
        police_character_number = random.randint(0,globals()['%s_count'% police_option]-1) #randomly choose armed or unarmed police character
        police_file_name = police_option + "/" + police_option + "_" + str(police_character_number) + ".png" #find the police image in the input folder
        civilian_option = random.choice(civilian_options) #choose a random civilian image
        civilian_character_number = random.randint(0,globals()['%s_count'% civilian_option]-1) #randomly choose armed or unarmed civilian character
        civilian_file_name = civilian_option + "/" + civilian_option + "_" + str(civilian_character_number) + ".png" #find the civilian image in the input folder
        
        civilian_armed = 1 if civilian_option == "equipped_c" else 0 #set variables for classification
        police_armed = 1 if police_option == "equipped_p" else 0 set variables for classification
        #create classes based on equipment status of the characters
        if civilian_armed==1 and police_armed==1: 
            classes = "a"
        if civilian_armed==1 and police_armed==0:
            classes = "b" 
        if civilian_armed==0 and police_armed==1:
            classes = "c" 
        if civilian_armed==0 and police_armed==0:
            classes = "d"
        
        generate_image(classes, background_file_name, police_file_name, civilian_file_name, f"img{img}.png") #generate the image
        
        data = [f"img{img}.png",classes, 1,civilian_armed,1,police_armed,"TBD"] 
        s = pd.Series(data, index=df.columns)
        df = df.append(s, ignore_index=True) #append the row data of the specific image to the table

    df.to_csv('data' + str(num)+ '.csv', index=False) #creating a datafile for reference on inidividual objects

#using multithreading on 20 threads for parallel processing 
if __name__ == "__main__":
    #generate_all_imgs()
    for i in range(1,number_of_threads+1):
        globals()['t%s'% str(i)] = threading.Thread(target=generate_random_imgs, args=(1000,(i-1)*1000))
    # starting threads
    for i in range(1,number_of_threads+1):
        globals()['t%s'% str(i)].start()
    # wait until threads are completely executed
    for i in range(1,number_of_threads+1):
        globals()['t%s'% str(i)].join()
    print("All threads suucessfully executed")

#execute the code
main()
  
    
    