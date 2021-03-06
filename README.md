# 3d Pygame cube shading
Basic shading of a face of a cube in pygame.
### Usage:
- Change the fourth parameter of the cube object on line 76 to change the pixel depth of the face.
- Change the denominator of he fraction on line 132 to change the maximum range of the light.
### Screenshots:
![alt text](https://github.com/michael-gif/pygame-shading/blob/master/game%20engine%20screenshots.png "The shaded cube face")
### How it works:
- The number of pixels on the face is determined by the fourth parameter of the cube class.
- The face is split into a grid of polygons, each with a different greyscale value.
- The distance between the camera and the center of each polygon is calculated.
- There is a hard coded distance from the cube which you need to be inside of to see the face be shaded.
- The distances between you and the pixels is calculated as a proportion of the minimum distance.
- The colour of each pixel is the proportion of the distance multiplied by 255.  
For example, if you are 2 units away from the cube, then the colour of the closest pixel is 2/5 * 255  

The code behind the projection of the 3d coords is from another 3d engine that can be seen in this video:
https://www.youtube.com/watch?v=g4E9iq0BixA  
The rest of the code that draws the pixels and colours them is by me.
