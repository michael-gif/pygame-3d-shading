import pygame, math, sys, time
def rotate2d(pos,rad): x,y=pos; s,c = math.sin(rad),math.cos(rad); return x*c-y*s,y*c+x*s
class light:
    def __init__(self,pos=(0,0,0)):
        self.pos = list(pos)
class cam:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)
    def events(self,event):
        if event.type == pygame.MOUSEMOTION:
            x,y = event.rel
            x/=200
            y/=200
            self.rot[0]+=y
            self.rot[1]+=x
    def update(self,dt,key):
        s = dt*10
        if key[pygame.K_q]: self.pos[1]+=s
        if key[pygame.K_e]: self.pos[1]-=s
        x,y = s*math.sin(self.rot[1]),s*math.cos(self.rot[1])
        if key[pygame.K_w]: self.pos[0]+=x; self.pos[2]+=y
        if key[pygame.K_s]: self.pos[0]-=x; self.pos[2]-=y
        if key[pygame.K_a]: self.pos[0]-=y; self.pos[2]+=x
        if key[pygame.K_d]: self.pos[0]+=y; self.pos[2]-=x




class cube:
    #vertices = (-1,-1,-1),(1,-1,-1),(-1,1,-1),(1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)
    vertices = (-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)
    edges = (0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)
    #faces = (0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,3,7,4),(1,2,6,5)
    colours = (255,0,0),(255,128,0),(255,255,0),(255,255,255),(0,0,255),(0,255,0)
    midpoints = []
    def __init__(self,x,y,z,pixelsperside):
        self.x,self.y,self.z = x,y,z
        self.pixelsperside = pixelsperside
        self.corners = [(x+X/2,y+Y/2,z+Z/2) for X,Y,Z in self.vertices]
        frontface = []
        fraction = 2/pixelsperside
        for a in range(pixelsperside+1):
            componenty = fraction * a
            for b in range(pixelsperside+1):
                componentx = fraction * b
                point = (-1 + componentx,-1 + componenty,-1)
                frontface.append(point)
        for vertice in self.vertices:
            frontface.append(vertice)
        self.newverts = tuple(frontface)
        self.verts = [(x+X/2,y+Y/2,z+Z/2) for X,Y,Z in self.newverts]
        half_fraction = fraction * 0.5
        #midvalue = -1 + half_fraction
        for c in range(pixelsperside):
            componenty = fraction * c
            for d in range(pixelsperside):
                componentx = fraction * d
                midpoint = (-1 + half_fraction + componentx,-1 + half_fraction + componenty,-1)
                self.midpoints.append(midpoint)
        self.midpoints = tuple(self.midpoints)
                
pygame.init()
width = 800
height = 600
cx = width//2
cy = height//2
fov = min(width,height)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Game Engine')
crashed = False
clock = pygame.time.Clock()
cam = cam((0,0,-5))
light = light((0,0,-5))
pygame.event.get(); pygame.mouse.get_rel()
shapes = [cube(0,0,0,45)]
#print(shapes[0].midpoints)
play = False
while not crashed:
    dt = clock.tick()/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mouse.set_visible(1); pygame.event.set_grab(0)
                play = False
        cam.events(event)
    screen.fill((255,255,255))
    if play == True:
        for obj in shapes:
            allpoints = []
            for x,y,z in obj.verts:
                x -= cam.pos[0]
                y -= cam.pos[1]
                z -= cam.pos[2]
                x,z = rotate2d((x,z),cam.rot[1])
                y,z = rotate2d((y,z),cam.rot[0])
                f = fov/z
                x,y = x*f,y*f
                allpoints.append((cx+int(x),cy+int(y)))
                #pygame.draw.circle(screen,(0,0,0),(cx+int(x),cy+int(y)),5)
            for edge in obj.edges:
                points = []
                for x,y,z in (obj.corners[edge[0]],obj.corners[edge[1]]):
                    x -= cam.pos[0]
                    y -= cam.pos[1]
                    z -= cam.pos[2]
                    x,z = rotate2d((x,z),cam.rot[1])
                    y,z = rotate2d((y,z),cam.rot[0])
                    f = fov/z
                    x,y = x*f,y*f
                    points += [(cx+int(x),cy+int(y))]
                pygame.draw.line(screen,(0,0,0),points[0],points[1],1)

            #allmidpoints = [(-0.75,-0.75,-1),(-0.25,-0.75,-1),(0.25,-0.75,-1),(0.75,-0.75,-1),(-0.75,-0.25,-1),(-0.25,-0.25,-1),(0.25,-0.25,-1),(0.75,-0.25,-1),(-0.75,0.25,-1),(-0.25,0.25,-1),(0.25,0.25,-1),(0.75,0.25,-1),(-0.75,0.75,-1),(-0.25,0.75,-1),(0.25,0.75,-1),(0.75,0.75,-1)]
            allmidpoints = obj.midpoints
            distances = []
            for a in range(obj.pixelsperside**2):
                diffx = cam.pos[0] - obj.midpoints[a][0]
                diffz = cam.pos[2] - obj.midpoints[a][2]
                diffxsquared = diffx * diffx
                diffzsquared = diffz * diffz
                hypotenuse = diffxsquared + diffzsquared
                diffy = cam.pos[1] - obj.midpoints[a][1]
                diffysquared = diffy * diffy
                hypotenuse = hypotenuse + diffysquared
                distance = math.sqrt(hypotenuse)
                distances.append(distance)
            colours = []
            for distance in distances:
                fraction = distance/3
                fraction = 1 - fraction
                colour = fraction * 255
                if colour < 0 :
                    colour = 0
                colours.append((colour,colour,colour))
            polygons = []
            sidelength = obj.pixelsperside + 1
            for b in range(obj.pixelsperside):
                thing = b + 1
                currentrow = sidelength * b
                nextrow = sidelength * thing
                for a in range(obj.pixelsperside):
                    polygons.append((allpoints[a+currentrow],allpoints[a+1+currentrow],allpoints[a+1+nextrow],allpoints[a+nextrow]))
            for a in range(obj.pixelsperside**2):
                pygame.draw.polygon(screen,colours[a],polygons[a])

        key = pygame.key.get_pressed()
        cam.update(dt,key)
    else:
        pygame.draw.rect(screen,(0,0,0),(350,275,100,50))
        pygame.draw.rect(screen,(0,0,0),(350,350,100,50))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 450 > mouse[0] > 350 and 325 > mouse[1] > 275:
            pygame.draw.rect(screen,(100,100,100),(350,275,100,50))
            if click[0] == 1:
                play = True
                pygame.mouse.set_visible(0); pygame.event.set_grab(1)
        elif 450 > mouse[0] > 350 and 400 > mouse[1] > 350:
            pygame.draw.rect(screen,(100,100,100),(350,350,100,50))
            if click[0] == 1:
                pygame.quit()
                sys.exit()
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textsurf = smallText.render("Play",True,(255,255,255))
        textrect = textsurf.get_rect()
        textrect.center = (400,300)
        screen.blit(textsurf, textrect)
        textsurf = smallText.render("Quit",True,(255,255,255))
        textrect = textsurf.get_rect()
        textrect.center = (400,375)
        screen.blit(textsurf, textrect)
    pygame.display.flip()
pygame.quit()
