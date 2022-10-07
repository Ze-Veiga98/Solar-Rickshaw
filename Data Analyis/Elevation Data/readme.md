
# Digital elevation map for the Lisbon city center

![Alt Text](altitude_top.png?raw=true)


As it is well known, the altitude GPS data is not accurate enough to be used in the modeling , so I needed to came up to another solution that corrected the low-quality of altitude data. I have built a digital elevation data for the Lisbon city center, i.e., the region where the tuk-tuk usually operates in. This map was built we help of mapbox in python 3 by using their mapbox-terrain-RGB API. This API provides one heigh measurement increment of 0.1-meter for each square area of 17.5 m2. It is an easy-to-use API, so obtaining the altitudes data is as straightforward as simply
passing the pair of coordinate of points (latitude, longitude). Nevertheless, Mapbox obtains the elevation data thanks to the realization of the Copernicus EU program, which is an international research effort that provides the Digital Elevation Model (DEM) almost all over the land (from 56◦S to 60◦N). These data are generated from a weighted average of Shuttle Radar Topography Mission (SRTM) and Advanced Spaceborne Thermal Emission and Reflection Radiometer (ASTERM) [54]. Both datasets provide one altitude measurement for every square area of 900 m2, which translates into one measurement for every  30 m.


<img src="twin-satellites-terrasar-x-tandem-x.jpg" width="500" height="300">


## Usage


```python
# Import the necessary packages
import seaborn as sns
import mercantile # convert lat/lon to tilesets
import PIL
from TilesDownloader import build_canvas
from TilesDownloader import get_image_matrix

# Scan the range you would like to view
# Select the area you are interested in
zoom = 15                   
top_left = mercantile.tile(-9.367633, 38.618097, zoom)
bottom_right = mercantile.tile(-9.052183, 38.8207215, zoom) 

# Pulling the images data from the mapbox url and save it in a specific folder. This can be done calling the function 'build_canvas'
build_canvas(top_left, bottom_right)

# The next step is to compose all of the smaller images into a very large image of very high resolution. This can be achieved through
# 'get_image_matrix' function

im_mat = get_image_matrix(top_left, bottom_right)
height = (top_left.y - bottom_right.y) * 256
width  = (bottom_right.x - top_left.x) *256
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

# plot altitude heat map
sns.heatmap(matrix, cmap = 'plasma')


## Authors
José Veiga &
David Neto

