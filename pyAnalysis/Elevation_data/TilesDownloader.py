import mercantile # to convert lat/lon to tilesets
import PIL # for images processing
import requests # send requests to mapbox-api
import os

from PIL import Image

# For plot-related
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Your own mapbox token...
TOKEN = "pk.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
##########################################################################################################################
# This function downloads the altitude data in tileset format (RGB colours) as well as the correspoding sattelite images 
# And saves them in a folder...
##########################################################################################################################

def build_canvas(top_left, bottom_right):
    for i in range(top_left.x, bottom_right.x):
        for j in range(bottom_right.y, top_left.y):
            endpoint = 'https://api.mapbox.com/v4/mapbox.terrain-rgb/' + str(zoom) + '/' +str(i) + '/' + str(j) + '.pngraw?access_token=' + TOKEN
            response = requests.get(endpoint, stream=True)
            
            if response.status_code  == 200:
                file =  open('./altitude_images_' + str(zoom) + '_' +str(i) + '_' + str(j) + '.png', 'wb').write(response.content)
            
            endpoint1 = 'https://api.mapbox.com/v4/mapbox.satellite/' + str(zoom) + '/' +str(i) + '/' + str(j) + '.pngraw?access_token=' + TOKEN
            response1 = requests.get(endpoint1, stream=True)
            
            if response1.status_code  == 200:
                file1 =  open('./satellite_images_' + str(zoom) + '_' +str(i) + '_' + str(j) + '.png', 'wb').write(response1.content)
                    
                
                
                
                    
                    
def get_image_matrix(top_left, bottom_right):
    images = []
    for i in range(top_left.x, bottom_right.x):
        image_line = []
        for j in range(bottom_right.y, top_left.y):
           # image_files = ['Tilesets/altitude_images_' + f for f in listdir('IMAGES/'+img_name+'_images/')]
            image = Image.open('./altitude_images_' + str(zoom) + '_' +str(i) + '_' + str(j) + '.png')
            print('./altitude_images' + str(zoom) + '_' +str(i) + '_' + str(j) + '.png')
            image_line.append(image)
            # pix = image.load()
        images.append(image_line)
    return images                    
                    

zoom = 15                   
top_left = mercantile.tile(-9.367633, 38.618097, zoom)
bottom_right = mercantile.tile(-9.052183, 38.8207215, zoom) 
build_canvas(top_left, bottom_right)



im_mat = get_image_matrix(top_left, bottom_right)

height = (top_left.y - bottom_right.y) * 256
width  = (bottom_right.x - top_left.x) *256

print(height, width)

final_image = Image.new('RGB', (width, height))

y_offset = 0
for line in im_mat:
    x_offset = 0
    for element in line:
        # final_image.paste(element, (x_offset, y_offset ))
        final_image.paste(element, (y_offset, x_offset ))
        x_offset += element.size[0]
    y_offset += 256

final_image.save('full_image.png')

final = Image.open('full_image.png')
pix = final.load()

matrix =np.zeros([width, height])


for i in range(0, width):
    for j in range(0, height):
        pixel = pix[i,j]
        matrix [i,j]  = -10000 + ((pixel[0] * 256 * 256 + pixel[1] * 256 + pixel[2]) * 0.1)

        if matrix[i,j] > 1000:
            matrix[i,j] = 0
# plot 
sns.heatmap(matrix, cmap = 'coolwarm')
plt.show()
            

          
                    
               




















