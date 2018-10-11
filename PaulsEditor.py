#map tile example using a map of tile objects along with tile collision detection

import pygame
import time
import os.path

filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')  # this joins the path of our script and our new direction 'assets'
try:
    os.makedirs(filepath)  # if the 'assets' directory does not exist create it
except:
    pass

def collideCircleRectangle(circle_x,circle_y,circle_radius,rect_x1,rect_y1,rect_x2,rect_y2):
    """CollideCircleRectangle(circle_x,circle_y,circle_radius,rect_x1,rect_y1,rect_x2,rect_y2) - Returns True if the circle collides with the rectangle, False otherwise """
    if((rect_x1-circle_radius<=circle_x<=rect_x2+circle_radius  or rect_x2-circle_radius<=circle_x<=rect_x1+circle_radius) and  (rect_y1<=circle_y<=rect_y2  or rect_y2<=circle_y<=rect_y1)) or ((rect_x1<=circle_x<=rect_x2  or rect_x2<=circle_x<=rect_x1) and  (rect_y1-circle_radius<=circle_y<=rect_y2+circle_radius  or rect_y2-circle_radius<=circle_y<=rect_y1+circle_radius)):
        return True
    else:
        if collidePointCircle(rect_x1,rect_y1,circle_x,circle_y,circle_radius):
            return True
        elif collidePointCircle(rect_x2,rect_y2,circle_x,circle_y,circle_radius):
            return True
        elif collidePointCircle(rect_x1,rect_y2,circle_x,circle_y,circle_radius):
            return True
        elif collidePointCircle(rect_x2,rect_y1,circle_x,circle_y,circle_radius):
            return True
        else:
            return False

def collidePointCircle(point_x,point_y,circle_x,circle_y,circle_radius):
    """CollidePointCircle(point_x,point_y,circle_x,circle_y,circle_radius) - Returns True if the point collides with the circle, False otherwise."""
    if ((point_x-circle_x)**2 + (point_y-circle_y)**2)**0.5  <= circle_radius:
        return True
    else:
        return False

class TileType(object):
    def __init__(self,tileSourceFilename=None,tileSourceColRow=(0,0),tileWidth=32,tileHeight=32,tileCollides=True,isBack=False,isVisible=True):
        (tileSourceCol,tileSourceRow)=tileSourceColRow
        self.tileSourceFilename=tileSourceFilename
        self.tileSourceCol=tileSourceCol
        self.tileSourceRow=tileSourceRow
        self.tileWidth=tileWidth
        self.tileHeight=tileHeight
        self.tileCollides=tileCollides
        self.isBack=isBack
        self.isVisible=isVisible
        self.mask = pygame.image.load(os.path.join(filepath, "mask.png"))
        if tileSourceFilename!=None:
            tilesetSurf=pygame.image.load(os.path.join(filepath, tileSourceFilename) )
            tilesetSurf.convert_alpha()
            if self.isBack == False:
                self.tileSurf=pygame.Surface((tileWidth,tileHeight)) #make a new surface
                self.tileSurf.blit(tilesetSurf,(0,0),(tileSourceCol*tileWidth,tileSourceRow*tileHeight,tileWidth,tileHeight))
            else:
                self.tileSurf=pygame.Surface((tileWidth,tileHeight)) #make a new surface
                self.tileSurf.blit(tilesetSurf,(0,0),(tileSourceCol*tileWidth,tileSourceRow*tileHeight,tileWidth,tileHeight))
                self.tileSurf.blit(self.mask, (0,0))
            if self.isVisible == False:
                self.tileSurf.set_alpha(0)
            self.tileSurf.set_colorkey((0,0,0))
    def dumpsTileType(self):
        outList=[]
        outList.append("tileSourceFilename="+self.tileSourceFilename)
        outList.append("tileSourceCol="+str(self.tileSourceCol))
        outList.append("tileSourceRow="+str(self.tileSourceRow))
        outList.append("tileWidth="+str(self.tileWidth))
        outList.append("tileHeight="+str(self.tileHeight))
        outList.append("tileCollides="+str(self.tileCollides))
        outList.append("isBack="+str(self.isBack))
        outList.append("isVisible="+str(self.isVisible))
        s=","
        return s.join(outList)  
    def loadsTileType(self,inString):
        inList=inString.split(",")
        for item in inList:
            (key,value)=item.split("=")
            if key=="tileSourceCol":
                self.tileSourceCol=int(value)
            elif key=="tileSourceRow":
                self.tileSourceRow=int(value)
            elif key=="tileWidth":
                self.tileWidth=int(value)
            elif key=="tileHeight":
                self.tileHeight=int(value)
            elif key=="tileCollides":
                if value=="True":
                    self.tileCollides=True
                else:
                    self.tileCollides=False
            elif key=="tileSourceFilename":
                self.tileSourceFilename=value
            elif key=="isBack":
                if value=="True":
                    self.isBack=True
                else:
                    self.isBack=False
            elif key=="isVisible":
                if value=="True":
                    self.isVisible=True
                else:
                    self.isVisible=False

        # reload the surface
        tilesetSurf=pygame.image.load(os.path.join(filepath, self.tileSourceFilename))
        if self.isBack == False:
            self.tileSurf=pygame.Surface((self.tileWidth,self.tileHeight)) #make a new surface
            self.tileSurf.blit(tilesetSurf,(0,0),(self.tileSourceCol*self.tileWidth,self.tileSourceRow*self.tileHeight,self.tileWidth,self.tileHeight))
        else:
            self.tileSurf=pygame.Surface((self.tileWidth,self.tileHeight)) #make a new surface
            mask = pygame.Surface((self.tileWidth, self.tileHeight))
            mask.fill((0,0,0))
            mask.set_alpha(68)
            self.tileSurf.blit(tilesetSurf,(0,0),(self.tileSourceCol*self.tileWidth,self.tileSourceRow*self.tileHeight,self.tileWidth,self.tileHeight))
            self.tileSurf.blit(mask, (0,0))
        if self.isVisible == False:
            self.tileSurf.set_alpha(0)
        self.tileSurf.set_colorkey((0,0,0))

class TileMap(object):
    def __init__(self,mapWidth=27,mapHeight=18,tileWidth=32,tileHeight=32):
        self.mapWidth=mapWidth
        self.mapHeight=mapHeight
        self.tileWidth=tileWidth
        self.tileHeight=tileHeight
        self.tileMap=[]
        for row in range(0,mapHeight):
            self.tileMap.append([None]*mapWidth)
        self.tileTypes={}
    def addTileType(self,tileId,tileType):
        self.tileTypes[tileId]=tileType
    def renderTile(self,screenCol,screenRow,mapEntry,screen):
        screenX=screenCol*self.tileWidth
        screenY=screenRow*self.tileHeight
        screen.blit(mapEntry.tileSurf,(screenX,screenY))
    def setTileMapEntry(self,mapCol,mapRow,tileTypeKey):
        if tileTypeKey==None:
            self.tileMap[mapRow][mapCol]=None
        else:
            self.tileMap[mapRow][mapCol]=tileTypeKey
    def renderMap(self,screen):
        for row in range(0,self.mapHeight):
            for col in range(0,self.mapWidth):
                mapEntryKey=self.tileMap[row][col]
                if mapEntryKey != None:
                    self.renderTile(col,row,self.tileTypes[mapEntryKey],screen)
    def saveTileTypes(self,filename):
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maps')  # this joins the path of our script and our new direction 'maps'
        filename = os.path.join(filepath, filename)
        try:
            os.makedirs(filepath)  # if the 'maps' directory does not exist create it
            os.makedir(filename)
            fp = open(filename, "w")
        except:
            fp = open(filename, "w")  # otherwise continue normally to save the file
        for tileType in sorted(self.tileTypes.keys()):
            fp.write(tileType+":"+self.tileTypes[tileType].dumpsTileType()+"\n")
        fp.close()
    def loadTileTypes(self,filename):
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maps', filename)  # load our file from the 'maps' directory
        fp = open(filename, "r")
        
        for line in fp:
            line=line.strip()
            if len(line)==0 or line[0]=='#': # skip blank lines and comment lines
                continue
            (tileType,tileTypeDumpedString)=line.split(":") # divide the line into the two sides of the :
            self.tileTypes[tileType]=TileType()
            self.tileTypes[tileType].loadsTileType(tileTypeDumpedString)            
        fp.close()
    def saveMap(self,filename):
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maps')  # this joins the path of our script and our new direction 'maps'
        filename = os.path.join(filepath, filename)
        try:
            os.makedirs(filepath)  # if the 'maps' directory does not exist create it
            os.makedir(filename)
            fp = open(filename, "w")
        except:
            fp = open(filename, "w")  # otherwise continue normally to save the file
        fp.write("mapWidth="+str(self.mapWidth)+"\n")
        fp.write("mapHeight="+str(self.mapHeight)+"\n")
        fp.write("tileWidth="+str(self.tileWidth)+"\n")
        fp.write("tileHeight="+str(self.tileHeight)+"\n")
        fp.write("tileMap=\n")
        for row in range(0,self.mapHeight):
            for col in range(0,self.mapWidth):
                if self.tileMap[row][col]==None:
                    fp.write("None")
                else:
                    mapEntry=self.tileMap[row][col]
                    fp.write(mapEntry)
                if col<self.mapWidth-1: #suppress comma on last item in row
                    fp.write(",") # comma is our column field delimiter
            fp.write("\n")
        fp.close()
    def loadMap(self,filename):
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maps', filename)  # load our file from the 'maps' directory
        fp = open(filename, "r")
        for line in fp:
            line=line.strip()
            if len(line)==0 or line[0]=='#': # skip blank lines and comment lines
                continue
            (attribute,value)=line.split("=") # divide the line into the two sides of the equal
            if attribute=="mapWidth":
                self.mapWidth=int(value)
            if attribute=="mapHeight":
                self.mapHeight=int(value)
            if attribute=="tileWidth":
                self.tileWidth=int(value)
            if attribute=="tileHeight":
                self.tileHeight=int(value)
            if attribute=="tileMap":
                for row in range(0,self.mapHeight):
                    mapline=fp.readline().strip() #read in row
                    entry_list=mapline.split(",") #split row on comma
                    for col in range(0,len(entry_list)):
                        if entry_list[col]=="None":
                            self.tileMap[row][col]=None
                        else:
                            self.tileMap[row][col]=entry_list[col]
        fp.close()
    def getCollisionSetCircle(self,testCircleX,testCircleY,testCircleR):
        collisionSet=[]
        for mapRow in range(0,self.mapHeight):
            for mapCol in range(0,self.mapWidth):
                mapEntryKey=self.tileMap[mapRow][mapCol]
                if mapEntryKey!=None:
                    rectY1 = mapRow*self.tileTypes[mapEntryKey].tileHeight
                    rectX1 = mapCol*self.tileTypes[mapEntryKey].tileWidth
                    rectY2 = rectY1 + self.tileTypes[mapEntryKey].tileHeight
                    rectX2 = rectX1 + self.tileTypes[mapEntryKey].tileWidth
                    
                    if collideCircleRectangle(testCircleX,testCircleY,testCircleR,rectX1,rectY1,rectX2,rectY2):
                        tileCenterX=(rectX1+rectX2)/2
                        tileCenterY=(rectY1+rectY2)/2
                        tileDistance=distance(testCircleX,testCircleY,tileCenterX,tileCenterY)
                        collisionSet.append(CollisionTile(mapEntryKey,mapCol,mapRow,tileCenterX,tileCenterY,tileDistance))
        return collisionSet

class CollisionTile(object):
    def __init__(self,mapEntryKey,mapCol,mapRow,mapTileCenterX,mapTileCenterY,collideDistance):
        self.mapEntryKey=mapEntryKey
        self.mapCol=mapCol
        self.mapRow=mapRow
        self.mapTileCenterX=mapTileCenterX
        self.mapTileCenterY=mapTileCenterY
        self.collideDistance=collideDistance

def distance(x1,y1,x2,y2):
    return ((x2-x1)**2+(y2-y1)**2)**0.5
                                            
def nextDictKey(dictionary,key):
    keyList = sorted(dictionary.keys())
    currentIndex=keyList.index(key)
    newIndex=currentIndex+1
    if newIndex>len(keyList)-1:
        newIndex=0
        
    return keyList[newIndex]
def prevDictKey(dictionary,key):
    keyList = sorted(dictionary.keys())
    currentIndex=keyList.index(key)
    newIndex=currentIndex-1
    if newIndex<0:
        newIndex=len(keyList)-1
    return keyList[newIndex]

if __name__ == "__main__":

    current_map = "level 1.txt"
    pygame.init()

    screen = pygame.display.set_mode((864, 576), pygame.SWSURFACE, 32)

    map1 = TileMap()
    map1.loadMap(current_map)

    map1.addTileType("grass_back",TileType("sprite_sheet.png",(0,0),tileCollides=False,isBack=False))
    map1.addTileType("grass.100",TileType("sprite_sheet.png",(0,0), isBack=False))
    map1.addTileType("grass.75",TileType("sprite_sheet.png",(0,1),tileCollides=False, isBack=False))
    map1.addTileType("grass.50",TileType("sprite_sheet.png",(0,2),tileCollides=False, isBack=False))
    map1.addTileType("grass.25",TileType("sprite_sheet.png",(0,3),tileCollides=False, isBack=False))

    map1.addTileType("dirt_back",TileType("sprite_sheet.png",(1,0),tileCollides=False,isBack=True))
    map1.addTileType("dirt.100",TileType("sprite_sheet.png",(1,0)))
    map1.addTileType("dirt.75",TileType("sprite_sheet.png",(1,1),tileCollides=False))
    map1.addTileType("dirt.50",TileType("sprite_sheet.png",(1,2),tileCollides=False))
    map1.addTileType("dirt.25",TileType("sprite_sheet.png",(1,3),tileCollides=False))

    map1.addTileType("stone_back",TileType("sprite_sheet.png",(0,4),tileCollides=False,isBack=True))
    map1.addTileType("stone.100",TileType("sprite_sheet.png",(0,4)))
    map1.addTileType("stone.75",TileType("sprite_sheet.png",(0,5),tileCollides=False ))
    map1.addTileType("stone.50",TileType("sprite_sheet.png",(0,6),tileCollides=False ))
    map1.addTileType("stone.25",TileType("sprite_sheet.png",(0,7),tileCollides=False ))

    map1.addTileType("gravel_back",TileType("sprite_sheet.png",(1,4),tileCollides=False,isBack=True))
    map1.addTileType("gravel.100",TileType("sprite_sheet.png",(1,4)))
    map1.addTileType("gravel.75",TileType("sprite_sheet.png",(1,5),tileCollides=False ))
    map1.addTileType("gravel.50",TileType("sprite_sheet.png",(1,6),tileCollides=False ))
    map1.addTileType("gravel.25",TileType("sprite_sheet.png",(1,7),tileCollides=False ))

    map1.addTileType("mossybrick_back",TileType("sprite_sheet.png",(0,8),tileCollides=False,isBack=True))
    map1.addTileType("mossybrick.100",TileType("sprite_sheet.png",(0,8)))
    map1.addTileType("mossybrick.75",TileType("sprite_sheet.png",(0,9),tileCollides=False ))
    map1.addTileType("mossybrick.50",TileType("sprite_sheet.png",(0,10),tileCollides=False ))
    map1.addTileType("mossybrick.25",TileType("sprite_sheet.png",(0,11),tileCollides=False ))

    map1.addTileType("crackedbrick_back",TileType("sprite_sheet.png",(1,8),tileCollides=False,isBack=True))
    map1.addTileType("crackedbrick.100",TileType("sprite_sheet.png",(1,8)))
    map1.addTileType("crackedbrick.75",TileType("sprite_sheet.png",(1,9),tileCollides=False ))
    map1.addTileType("crackedbrick.50",TileType("sprite_sheet.png",(1,10),tileCollides=False ))
    map1.addTileType("crackedbrick.25",TileType("sprite_sheet.png",(1,11),tileCollides=False ))

    map1.addTileType("brick_back",TileType("sprite_sheet.png",(2,8),tileCollides=False,isBack=True))
    map1.addTileType("brick.100",TileType("sprite_sheet.png",(2,8)))
    map1.addTileType("brick.75",TileType("sprite_sheet.png",(2,9),tileCollides=False ))
    map1.addTileType("brick.50",TileType("sprite_sheet.png",(2,10),tileCollides=False ))
    map1.addTileType("brick.25",TileType("sprite_sheet.png",(2,11),tileCollides=False ))

    map1.addTileType("netherbrick_back",TileType("sprite_sheet.png",(3,8),tileCollides=False,isBack=True))
    map1.addTileType("netherbrick.100",TileType("sprite_sheet.png",(3,8)))
    map1.addTileType("netherbrick.75",TileType("sprite_sheet.png",(3,9),tileCollides=False ))
    map1.addTileType("netherbrick.50",TileType("sprite_sheet.png",(3,10),tileCollides=False ))
    map1.addTileType("netherbrick.25",TileType("sprite_sheet.png",(3,11),tileCollides=False ))

    map1.addTileType("netherack_back",TileType("sprite_sheet.png",(0,12),tileCollides=False,isBack=True))
    map1.addTileType("netherack.100",TileType("sprite_sheet.png",(0,12)))
    map1.addTileType("netherack.75",TileType("sprite_sheet.png",(0,13),tileCollides=False ))
    map1.addTileType("netherack.50",TileType("sprite_sheet.png",(0,14),tileCollides=False ))
    map1.addTileType("netherack.25",TileType("sprite_sheet.png",(0,15),tileCollides=False ))

    map1.addTileType("soulsand.100",TileType("sprite_sheet.png",(1,12)))
    map1.addTileType("soulsand.75",TileType("sprite_sheet.png",(1,13),tileCollides=False ))
    map1.addTileType("soulsand.50",TileType("sprite_sheet.png",(1,14),tileCollides=False ))
    map1.addTileType("soulsand.25",TileType("sprite_sheet.png",(1,15),tileCollides=False ))


    map1.addTileType("torch",TileType("sprite_sheet.png",(4,4),tileCollides=False,isBack=True))
    map1.addTileType("toadstool",TileType("sprite_sheet.png",(4,5),tileCollides=False,isBack=True))
    map1.addTileType("mushroom",TileType("sprite_sheet.png",(4,6),tileCollides=False,isBack=True))
    map1.addTileType("flowerRed",TileType("sprite_sheet.png",(4,7),tileCollides=False,isBack=True))
    map1.addTileType("shrooms",TileType("sprite_sheet.png",(4,8),tileCollides=False,isBack=True))
    map1.addTileType("metalbars",TileType("sprite_sheet.png",(4,9),tileCollides=False,isBack=True))
    map1.addTileType("web",TileType("sprite_sheet.png",(4,11),tileCollides=False,isBack=True))
    map1.addTileType("tall_grass",TileType("sprite_sheet.png",(4,12),tileCollides=False,isBack=True))
    map1.addTileType("flowerYellow",TileType("sprite_sheet.png",(4,13),tileCollides=False,isBack=True))
    map1.addTileType("glowstone",TileType("sprite_sheet.png",(4,14),tileCollides=False,isBack=True))
    map1.addTileType("bookshelf",TileType("sprite_sheet.png",(4,15),tileCollides=False,isBack=True))


    map1.addTileType("trapGrass",TileType("sprite_sheet.png",(0,0))) #game 0,0
    map1.addTileType("trapGrassTripped",TileType("sprite_sheet.png",(2,0),tileCollides=False))
    map1.addTileType("trapStone",TileType("sprite_sheet.png",(0,4))) #game 0,4
    map1.addTileType("trapStoneTripped",TileType("sprite_sheet.png",(2,1),tileCollides=False))
    map1.addTileType("trapStoneBrick",TileType("sprite_sheet.png",(2,8))) #game 3,8
    map1.addTileType("trapStoneBrickTripped",TileType("sprite_sheet.png",(2,2),tileCollides=False))
    map1.addTileType("trapNetherBrick",TileType("sprite_sheet.png",(3,8))) #game 3,8
    map1.addTileType("trapNetherBrickTripped",TileType("sprite_sheet.png",(2,3),tileCollides=False))
    map1.addTileType("trapNether",TileType("sprite_sheet.png",(0,12))) #game 0,12
    map1.addTileType("trapNetherTripped",TileType("sprite_sheet.png",(2,4),tileCollides=False))
    map1.addTileType("trapObsidian",TileType("sprite_sheet.png",(3,6))) #game 3,6
    map1.addTileType("trapObsidianTripped",TileType("sprite_sheet.png",(2,5),tileCollides=False))



    map1.addTileType("nodigMetal",TileType("sprite_sheet.png",(3,2)))
    map1.addTileType("nodigCoal",TileType("sprite_sheet.png",(3,3)))
    map1.addTileType("nodigGold",TileType("sprite_sheet.png",(3,4)))
    map1.addTileType("nodigDiamond",TileType("sprite_sheet.png",(3,5)))
    map1.addTileType("nodigObsidian",TileType("sprite_sheet.png",(3,6)))
    map1.addTileType("nodigBedrock",TileType("sprite_sheet.png",(3,7)))
    map1.addTileType("iron",TileType("sprite_sheet.png",(3,2),tileCollides=False,isBack=True))
    map1.addTileType("coal",TileType("sprite_sheet.png",(3,3),tileCollides=False,isBack=True))
    map1.addTileType("goldore",TileType("sprite_sheet.png",(3,4),tileCollides=False,isBack=True))
    map1.addTileType("diamond",TileType("sprite_sheet.png",(3,5),tileCollides=False,isBack=True))
    map1.addTileType("obsidian",TileType("sprite_sheet.png",(3,6),tileCollides=False,isBack=True))
    map1.addTileType("bedrock",TileType("sprite_sheet.png",(3,7),tileCollides=False,isBack=True))

    map1.addTileType("ladder",TileType("sprite_sheet.png",(3,1)))
    map1.addTileType("escapeLadder",TileType("sprite_sheet.png",(3,1)))

    map1.addTileType("water",TileType("sprite_sheet.png",(4,0)))
    map1.addTileType("lava.1",TileType("sprite_sheet.png",(5,12)))
    map1.addTileType("lava.2",TileType("sprite_sheet.png",(5,13)))
    map1.addTileType("lava.3",TileType("sprite_sheet.png",(5,14)))
    map1.addTileType("lava.4",TileType("sprite_sheet.png",(5,15)))

    map1.addTileType("beam",TileType("sprite_sheet.png",(3,0)))
    map1.addTileType("gold",TileType("sprite_sheet.png",(4,1),tileCollides=False))
    map1.addTileType("enemy spawn",TileType("sprite_sheet.png",(4,2),tileCollides=False,isVisible=False))
    map1.addTileType("player spawn",TileType("sprite_sheet.png",(4,3),tileCollides=False,isVisible=False))

    map1.addTileType("air",TileType("sprite_sheet.png", (0,0), tileCollides=False,isVisible=False))

    clock = pygame.time.Clock()

    curTileKey="grass.100"

    while True:
        pygame.event.pump()
        keysPressed = pygame.key.get_pressed()
        if keysPressed[pygame.K_ESCAPE]:
            break
        if keysPressed[pygame.K_s] and (keysPressed[pygame.K_RCTRL] or keysPressed[pygame.K_LCTRL]):
            map1.saveMap(current_map)
            map1.saveTileTypes("maptiles.txt")
            print("Saved")
            while keysPressed[pygame.K_s] and (keysPressed[pygame.K_RCTRL] or keysPressed[pygame.K_LCTRL]):
                pygame.event.pump()
                keysPressed = pygame.key.get_pressed()

        if keysPressed[pygame.K_l] and (keysPressed[pygame.K_RCTRL] or keysPressed[pygame.K_LCTRL]):
            map1.loadMap(current_map)
            map1.loadTileTypes("maptiles.txt")
            print("Loaded")
            while keysPressed[pygame.K_l] and (keysPressed[pygame.K_RCTRL] or keysPressed[pygame.K_LCTRL]):
                pygame.event.pump()
                keysPressed = pygame.key.get_pressed()

        if keysPressed[pygame.K_LEFT]:
            curTileKey=prevDictKey(map1.tileTypes,curTileKey)
            print("Current Tile:",curTileKey)
            while keysPressed[pygame.K_LEFT]:
                pygame.event.pump()
                keysPressed = pygame.key.get_pressed()

        if keysPressed[pygame.K_RIGHT]:
            curTileKey=nextDictKey(map1.tileTypes,curTileKey)
            print("Current Tile:",curTileKey)
            while keysPressed[pygame.K_RIGHT]:
                pygame.event.pump()
                keysPressed = pygame.key.get_pressed()


        (mx,my)=pygame.mouse.get_pos()
        (lb,mb,rb)=pygame.mouse.get_pressed()
        mouseCol=int(mx/map1.tileWidth)
        mouseRow=int(my/map1.tileHeight)
        if lb==True:
            map1.setTileMapEntry(mouseCol,mouseRow,curTileKey)
        if rb==True:
            map1.setTileMapEntry(mouseCol,mouseRow,None)

        screen.fill((0,5,25))  #clear screen

        map1.renderMap(screen)

        newSurf = map1.tileTypes[curTileKey].tileSurf.copy()
        newSurf.set_alpha(150)
        screen.blit(newSurf,(mouseCol*map1.tileWidth,mouseRow*map1.tileHeight))
        pygame.draw.rect(screen,(0,0,255),(mouseCol*map1.tileWidth,mouseRow*map1.tileHeight,map1.tileWidth,map1.tileHeight),2)

        pygame.draw.circle(screen,(255,50,50),(mx,my),40,1)

        collideTiles=map1.getCollisionSetCircle(mx,my,40)

        #show tiles that we're colliding with by drawing a line to each
        if len(collideTiles)>0:
            closestTile=collideTiles[0]
            for collideTile in collideTiles:
                if collideTile.collideDistance < closestTile.collideDistance:
                    closestTile=collideTile

                pygame.draw.line(screen,(0,255,0),(mx,my),(collideTile.mapTileCenterX,collideTile.mapTileCenterY))
            pygame.draw.line(screen,(255,0,255),(mx,my),(closestTile.mapTileCenterX,closestTile.mapTileCenterY),3)

        pygame.display.flip()

        clock.tick(60)

    pygame.display.quit()
