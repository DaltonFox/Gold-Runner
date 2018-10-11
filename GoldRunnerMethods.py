"""
This is a collection of methods used for Gold Runner.py
Created this to create some space in Gold Runner.py as it was getting kind of stuffy
"""

import pygame
import time
import PaulsEditor
import random


class brokenblock(object):
    def __init__(self, key, col, row, regen_time):
        (self.key, self.percent) = key.split('.')
        self.percent = 0
        self.col = col
        self.row = row
        self.regen_time = regen_time
        self.start_time = time.time()


def collideRectangles(rect1_x1,rect1_y1,rect1_x2,rect1_y2, rect2_x1,rect2_y1,rect2_x2,rect2_y2 ):
    """
    Returns True if the two orthogonal rectangles collide, False otherwise.
    """
    r1 = pygame.Rect(int(rect1_x1),int(rect1_y1),int(rect1_x2)-int(rect1_x1),int(rect1_y2)-int(rect1_y1))
    r2 = pygame.Rect(int(rect2_x1),int(rect2_y1),int(rect2_x2)-int(rect2_x1),int(rect2_y2)-int(rect2_y1))

    return r1.colliderect(r2)


def collidingCircles(c1x, c1y, c1r, c2x, c2y, c2r):
    """
    :param c1x: x of the first circle region
    :param c1y: y of the first circle region
    :param c1r: radius of the first circle region
    :param c2x: x of the second circle region
    :param c2y: y of the second circle region
    :param c2r: radius of the first circle region
    :return: This returns True if we the two circle regions are colliding and False if they are not.
    """
    if (int(c1x) - int(c2x)) ** 2 + (int(c1y) - int(c2y)) ** 2 <= (int(c1r) + int(c2r)) ** 2:
        return True
    return False


def getCollisionSet(map, player, tiles):
    """
    :param map: the map for access to its data
    :param player: the player
    :param tiles: a list of tile sets
    :return: This will return a list of CollisionTile objects from PaulsEditor which can be used for collision checks
    """
    collisionSet = []
    for mapRow in range(0, map.mapHeight):
        for mapCol in range(0, map.mapWidth):

            tile=map.tileMap[mapRow][mapCol]


            if tile != None and map.tileTypes[tile].tileCollides == True and tile != 'gold' or tile in tiles.get('trap_tiles'):
                if tile == "beam":  # Beams have a unique collision
                    if collideRectangles(player.x + 5, player.y + 16, player.x + 22, player.y + 16, mapCol * 32, mapRow * 32, (mapCol+1) * 32, (mapRow+1) * 32):
                        tileCenterX = (player.x+32 + mapCol*32) / 2  # ^ We have to adjust the player's "bounding box" so that it collides with the sprite
                        tileCenterY = (player.y+32 + mapRow*32) / 2
                        tileDistance = PaulsEditor.distance(player.x, player.y, tileCenterX, tileCenterY)
                        collisionSet.append(PaulsEditor.CollisionTile(tile, mapCol, mapRow, tileCenterX, tileCenterY, tileDistance))  # Create a CollisionTile object from PaulsEditor for our list collisionSet.
                elif tile in tiles.get('ladder_tiles'):  # Ladders have a unique collision
                    if collideRectangles(player.x + 5, player.y, player.x + 22, player.y + 32, (mapCol * 32) - 1, (mapRow * 32) - 4, ((mapCol+1) * 32) + 1, (mapRow+1) * 32):
                        tileCenterX = (player.x+32 + mapCol*32) / 2
                        tileCenterY = (player.y+32 + mapRow*32) / 2
                        tileDistance = PaulsEditor.distance(player.x, player.y, tileCenterX, tileCenterY)
                        collisionSet.append(PaulsEditor.CollisionTile(tile, mapCol, mapRow, tileCenterX, tileCenterY, tileDistance))
                else:  # Collision for everything else
                    if collideRectangles(player.x + 5, player.y, player.x + 22, player.y + 32, (mapCol*32) - 5, mapRow * 32, ((mapCol+1) * 32) + 1, (mapRow+1) * 32):
                        tileCenterX = (player.x+32 + mapCol*32) / 2
                        tileCenterY = (player.y+32 + mapRow*32) / 2
                        tileDistance = PaulsEditor.distance(player.x, player.y, tileCenterX, tileCenterY)
                        collisionSet.append(PaulsEditor.CollisionTile(tile, mapCol, mapRow, tileCenterX, tileCenterY, tileDistance))
            else:  # Gold is in none_tiles to avoid physical collision with it, so we have to check it separately.
                if tile == 'gold':
                    if collideRectangles(player.x + 3, player.y-2, player.x + 24, player.y + 34, mapCol * 32, mapRow * 32, (mapCol+1) * 32, (mapRow+1) * 32):
                        tileCenterX = (player.x+32 + mapCol*32) / 2
                        tileCenterY = (player.y+32 + mapRow*32) / 2
                        tileDistance = PaulsEditor.distance(player.x, player.y, tileCenterX, tileCenterY)
                        collisionSet.append(PaulsEditor.CollisionTile(tile, mapCol, mapRow, tileCenterX, tileCenterY, tileDistance))


    return collisionSet


def spawnPlayer(map):
    """
    :param map: the map for access to its data
    :return: this gets the location to spawn our player
    """
    for row in range(0, map.mapHeight):
            for col in range(0, map.mapWidth):
                mapEntryKey = map.tileMap[row][col]
                if mapEntryKey == 'player spawn':
                    return col*32, row*32


def spawnEnemies(map):
    """
    :param map: the map for access to its data
    :return: this gets the location of our enemy spawns
    """
    spawn_points = []
    # only gets spawns below the 3rd row
    for row in range(3, map.mapHeight):
            for col in range(0, map.mapWidth):
                mapEntryKey = map.tileMap[row][col]
                if mapEntryKey == 'enemy spawn':
                    spawn_points.append([row, col])

    return spawn_points


def respawnEnemies(map):
    """
    :param map: the map for access to its data
    :return: this puts the enemies at respawn locations
    """
    respawn_points = []
    # only gets spawns above the 3rd row
    for row in range(0, 3):
            for col in range(0, map.mapWidth):
                mapEntryKey=map.tileMap[row][col]
                if mapEntryKey == 'enemy spawn':
                    respawn_points.append([row, col])

    return respawn_points


def getEscapeLadder(map):
    """
    :param map: the map for access to its data
    :return: this finds where our escape ladder should be
    """
    ladder_points = []
    for row in range(0, map.mapHeight):
            for col in range(0, map.mapWidth):
                mapEntryKey = map.tileMap[row][col]
                if mapEntryKey == 'escapeLadder':
                    ladder_points.append([row, col])
                    map.tileMap[row][col] = None

    return ladder_points


def makeEscapeLadder(map, ladder_points):
    """
    :param map: the map for access to its data
    :param ladder_points: data of escape ladders saved from getEscapeLadder
    :return: this creates our escape ladders
    """
    for ladder in ladder_points:
        row = ladder[0]
        col = ladder[1]
        map.tileMap[row][col] = 'escapeLadder'


def breakBlock(map, player, direction, tiles, particle_system, sound):
    """
    :param map: the map for access to its data
    :param player: the player
    :param direction: the direction the player is breaking a block
    :param tiles: a list of tile sets
    :return: This finds the correct block to break depending on direction, if it can be broken, and also breaks decoration blocks if applicable
    """
    # direction: 0 is right, 1 is left
    mapRow = int(player.y/32) + 1
    # if x is pressed, dig right
    if direction == 0:
        mapCol = int((player.x+16)/32) + 1
    # if z is pressed, dig left
    if direction == 1:
        mapCol = int((player.x+16)/32) - 1

    # check to see if player is on the edge of the screen and tries to dig
    if mapCol > 26:
        mapCol = 26
    if mapCol < 0:
        mapCol = 0

    mapEntryKey=map.tileMap[mapRow][mapCol]
    # check to see if player is on edge of the screen
    # check to see if tile is dig-able
    if mapEntryKey in tiles.get('ground_tiles') and mapEntryKey not in tiles.get('unbreakable_tiles'):

        # check to see if tile above is None and if its a decoration block
        above_block = map.tileMap[mapRow-1][mapCol]
        if above_block in tiles.get('decoration_tiles'):
            map.setTileMapEntry(mapCol,mapRow-1,'air')
        if above_block == None or above_block == "player spawn" or map.tileTypes[above_block].tileCollides == False:

            # check to see if player is on a beam
            if 'beam' not in player.collision_set:

                #check to see what tile to place
                if mapEntryKey in tiles.get('ground_tiles') and mapEntryKey not in tiles.get('unbreakable_tiles'):
                    sound.play()
                    # snow particles (x, y, direction, speed, lifespan, size, color, alpha, type)
                    for i in range(random.randint(4,6)):
                        particle_system.emit_particle((mapCol*32)+16, (mapRow*32)+2, random.randint(45, 135), random.uniform(2.5, 2.6), 6, random.randint(2, 3), (55, 55, 55), random.randint(220, 255), random.randint(1, 2))
                    return brokenblock(mapEntryKey, mapCol, mapRow, time.time()+2)


def update_x(entity, enemies, tiles, map, keysPressed, particle_system, sound):
    """
    :param collision_set: the current collisions
    :param entity: the actor object we are updating values for
    :param tiles: a list of tile sets
    :param map: the map for access to its data
    :param keysPressed: the current keys pressed
    :return: This checks the entity's x and moves it on input or on command, it also checks the facing direction of the entity and creates 'physical' collisions
    """
    old_x = entity.x
    if len(entity.collision_set) > 0:
        for colliding_tile in entity.collision_set:
            entity.collision_set = getCollisionSet(map, entity, tiles)
            if colliding_tile not in tiles.get('ground_tiles'):  # If we are touching at x don't even allow movement
                if keysPressed[pygame.K_RIGHT] or keysPressed[pygame.K_d]:
                    entity.x += 2.5
                    entity.facing = 0
                    if time.time() > entity.sound_delay and not entity.climbing:
                            sound.play()
                            entity.sound_delay = time.time() + 0.6
                            for i in range(random.randint(3,5)):
                                particle_system.emit_particle((entity.x)+16, (entity.y)+33, random.randint(45, 135), random.uniform(3.5, 3.6), random.randint(2,4), random.randint(1, 2), (55, 205, 55), random.randint(170, 210), 2)
                    break
                if keysPressed[pygame.K_LEFT] or keysPressed[pygame.K_a]:
                    entity.x -= 2.5
                    entity.facing = 1
                    if time.time() > entity.sound_delay and not entity.climbing:
                            sound.play()
                            entity.sound_delay = time.time() + 0.6
                            for i in range(random.randint(4,6)):
                                particle_system.emit_particle((entity.x)+16, (entity.y)+33, random.randint(45, 135), random.uniform(3.5, 3.6), random.randint(2, 4), random.randint(1, 2), (55, 205, 55), random.randint(170, 210), 2)
                    break
            else:
                break
    # Check x collision
    if entity.x != old_x:
        entity.collision_set = getCollisionSet(map, entity, tiles)  # Get a new set of collisions
        if len(entity.collision_set) > 0:
            for colliding_tile in entity.collision_set:
                if colliding_tile.mapEntryKey in tiles.get('ground_tiles') or colliding_tile.mapEntryKey in tiles.get("trap_tiles"):  # If we are colliding reset our X so we appear to collide physically
                    entity.x = old_x
                    break
    return (entity.x, entity.facing, entity.collision_set, entity.sound_delay)


def update_y(entity, enemies, tiles, map, keysPressed):
    """
    :param collision_set: the current collisions
    :param entity: the actor object we are updating values for
    :param tiles: a list of tile sets
    :param map: the map for access to its data
    :param keysPressed: the current keys pressed
    :return: This checks the entity's y and moves it on input or on command, it also checks if the entity is 'climbing' or not and creates 'physical' collisions
    """
    old_y = entity.y
    if len(entity.collision_set) > 0:
        for colliding_tile in entity.collision_set:
            entity.collision_set = getCollisionSet(map, entity, tiles)
            if colliding_tile.mapEntryKey in tiles.get('ladder_tiles'):
                if colliding_tile.mapEntryKey != 'beam':  # Y movement is only allowed on Ladder type tiles
                    if keysPressed[pygame.K_UP] or keysPressed[pygame.K_w]:
                        entity.y -= 2
                        break
                    if keysPressed[pygame.K_DOWN] or keysPressed[pygame.K_s]:
                        entity.y += 2
                        break
                else:  # If we have a beam tile only allow downward movement to "let go" of the beam
                    entity.climbing = True
                    entity.y = colliding_tile.mapRow * 32
                    if keysPressed[pygame.K_DOWN] or keysPressed[pygame.K_s]:
                        entity.y += 20
                        break
            else:
                entity.climbing = False  # If we are no longer on a ladder tile we aren't "climbing"
    else:
        entity.climbing = False
        entity.y += 2  # If we aren't touching anything effect the Y

    # Check y collision
    if entity.y != old_y:
        for enemy in enemies:
            if collideRectangles(entity.x+5,entity.y,entity.x+27,entity.y+32,enemy.x+5,enemy.y,enemy.x+27,enemy.y+32):  # Make sure we aren't going into other enemies
                if entity.facing == 0:
                    entity.x += 2  # Slide the entity so it doesn't get stuck
                if entity.facing == 1:
                    entity.x -= 2  # Slide the entity so it doesn't get stuck
                entity.y = old_y - 2
                entity.collision_set = getCollisionSet(map, entity, tiles)
                break
        entity.collision_set = getCollisionSet(map, entity, tiles)  # Get a new set of collisions
        if len(entity.collision_set) > 0:
            for colliding_tile in entity.collision_set:
                if colliding_tile.mapEntryKey in tiles.get('ground_tiles'):  # If we are colliding reset our Y so we appear to collide physically
                    entity.y = old_y
                    break
    return (entity.y, entity.climbing, entity.collision_set)


def enemy_update_x(entity, other_entities, tiles, map, particle_system, sound):
    """
    :param collision_set: the current collisions
    :param entity: the actor object we are updating values for
    :param tiles: a list of tile sets
    :param map: the map for access to its data
    :param keysPressed: the current keys pressed
    :return: This checks the entity's x and moves it on input or on command, it also checks the facing direction of the entity and creates 'physical' collisions
    """
    old_x = entity.x
    if entity.x == old_x:
        entity.moving = False

    if len(entity.collision_set) > 0:
        for colliding_tile in entity.collision_set:
            entity.collision_set = getCollisionSet(map, entity, tiles)
            if colliding_tile not in tiles.get('ground_tiles'):  # If we are touching something at x don't even allow movement
                if entity.direction == "right" and entity.isFroze == False:
                    entity.x += 1.5
                    entity.facing = 0
                    entity.moving = True
                    if time.time() > entity.sound_delay and not entity.climbing:
                            entity.sound_delay = time.time() + 0.6
                            for i in range(random.randint(3,5)):
                                particle_system.emit_particle((entity.x)+16, (entity.y)+33, random.randint(45, 135), random.uniform(3.5, 3.6), random.randint(2,4), random.randint(1, 2), (255, 55, 5), random.randint(170, 210), 2)
                    break
                if entity.direction == "left" and entity.isFroze == False:
                    entity.x -= 1.5
                    entity.facing = 1
                    entity.moving = True
                    if time.time() > entity.sound_delay and not entity.climbing:
                            entity.sound_delay = time.time() + 0.6
                            for i in range(random.randint(4,6)):
                                particle_system.emit_particle((entity.x)+16, (entity.y)+33, random.randint(45, 135), random.uniform(3.5, 3.6), random.randint(2, 4), random.randint(1, 2), (255, 55, 5), random.randint(170, 210), 2)
                    break
            else:
                break
    # Check x collision
    if entity.x != old_x:
        for other_entity in other_entities:
            if collideRectangles(entity.x-5,entity.y+2,entity.x+37,entity.y+32,other_entity.x-5,other_entity.y,other_entity.x+37,other_entity.y+30):  # Make sure we aren't going into other enemies
                if entity.direction == "left":
                    entity.x = old_x - 1.5
                if entity.direction == "right":
                    entity.x = old_x + 1.5
                entity.collision_set = getCollisionSet(map, entity, tiles)
                break

        entity.collision_set = getCollisionSet(map, entity, tiles)  # Get a new set of collisions
        if len(entity.collision_set) > 0:
            for colliding_tile in entity.collision_set:
                if colliding_tile.mapEntryKey in tiles.get('ground_tiles') or colliding_tile.mapEntryKey in tiles.get("trap_tiles"):  # If we are colliding reset our X so we appear to collide physically
                    entity.x = old_x
                    break
    return (entity.x, entity.collision_set, entity.sound_delay, entity.direction)


def enemy_update_y(entity, other_entities, tiles, map):
    """
    :param collision_set: the current collisions
    :param entity: the actor object we are updating values for
    :param tiles: a list of tile sets
    :param map: the map for access to its data
    :param keysPressed: the current keys pressed
    :return: This checks the entity's y and moves it on input or on command, it also checks if the entity is 'climbing' or not and creates 'physical' collisions
    """
    old_y = entity.y
    if len(entity.collision_set) > 0:
        for colliding_tile in entity.collision_set:
            entity.collision_set = getCollisionSet(map, entity, tiles)
            if colliding_tile.mapEntryKey in tiles.get('ladder_tiles'):
                if colliding_tile.mapEntryKey != 'beam':  # Y movement is only allowed on Ladder type tiles
                    if entity.vertical == "up" and entity.isFroze == False:
                        entity.y -= 2
                        break
                    if entity.vertical == "down" and entity.isFroze == False:
                        entity.y += 2
                        break
                else:  # If we have a beam tile only allow downward movement to "let go" of the beam
                    entity.climbing = True
                    entity.y = colliding_tile.mapRow * 32
                    if entity.vertical == "down":
                        entity.y += 20
                        entity.vertical = "up"
                        break
            else:
                entity.climbing = False  # If we are no longer on a ladder tile we aren't "climbing"
    elif entity.isFroze == False:
        entity.climbing = False
        entity.y += 2  # If we aren't touching anything effect the Y

    # Check y collision
    if entity.y != old_y:
        for other_entity in other_entities:
            if collideRectangles(entity.x+5,entity.y,entity.x+27,entity.y+32,other_entity.x+5,other_entity.y,other_entity.x+27,other_entity.y+32):  # Make sure we aren't going into other enemies
                if entity.direction == "right":
                    entity.x += 1  # Slide the entity so it doesn't get stuck
                if entity.direction == "left":
                    entity.x -= 1  # Slide the entity so it doesn't get stuck
                entity.y = old_y - 2
                entity.collision_set = getCollisionSet(map, entity, tiles)
                break
        entity.collision_set = getCollisionSet(map, entity, tiles)  # Get a new set of collisions
        if len(entity.collision_set) > 0:
            for colliding_tile in entity.collision_set:
                if colliding_tile.mapEntryKey in tiles.get('ground_tiles') or colliding_tile.mapEntryKey in tiles.get("trap_tiles"):  # If we are colliding reset our Y so we appear to collide physically
                    entity.y = old_y
                    break

    return (entity.y, entity.climbing, entity.collision_set)


def regenTiles(tiles, map, entities, respawns, sound):
    player_killed = False
    if len(tiles) > 0:
        for tile in tiles:
            #print(time.time() - tiles[0].start_time)
            if tile.percent == 0 and time.time() > tile.regen_time:
                tile.percent = 25
                tile.regen_time = time.time() + 1
            elif tile.percent == 25 and time.time() > tile.regen_time:
                tile.percent = 50
                tile.regen_time = time.time() + 1
            elif tile.percent == 50 and time.time() > tile.regen_time:
                tile.percent = 75
                tile.regen_time = time.time() + 1
            elif tile.percent == 75 and time.time() > tile.regen_time:
                tile.percent = 100
                tile.regen_time = time.time() + 2

            if tile.percent == 0:
                map.setTileMapEntry(tile.col, tile.row, 'air')
            else:
                map.setTileMapEntry(tile.col, tile.row, str(tile.key) + '.' + str(tile.percent))
            if tile.percent >= 100:
                for entity in entities:
                    if collidingCircles(entity.x + 16, entity.y + 16, 14, (tile.col*32) + 16, (tile.row*32) + 16, 14):
                            if entity == entities[0]:
                                player_killed = True
                                break
                            else:
                                if entity.has_chest == True:
                                    map.setTileMapEntry(int(entity.x / 32)+1, int(entity.y / 32)-1, 'gold')
                                    entity.has_chest = False

                                sound.play()  # play the kill sound
                                entity.isFroze = False
                                entity.wiggle = False
                                entity.x = respawns[random.randint(0, len(respawns)-1)][1] * 32
                                entity.y = respawns[random.randint(0, len(respawns)-1)][0] * 32
                                break
                tiles.remove(tile)

        if player_killed == True:
            return tiles, True
        else:
            return tiles, False


def enemyEscape(regen_tiles,entities):

    for i in range(1,len(entities)):
        for tile in regen_tiles:
            # check to see if enemy is on the bottom of any regen tile
            if collideRectangles(entities[i].x, entities[i].y+2, entities[i].x+32, entities[i].y+32, tile.col*32, (tile.row+1)*32, (tile.col+1)*32, (tile.row+1)*32) and entities[i].isFroze == False:
                entities[i].isFroze = True
                entities[i].freeze_time = time.time() + 3
                break

        # check to free enemies
        if time.time() > entities[i].freeze_time-1 and entities[i].isFroze == True:
            entities[i].wiggle = True
        if time.time() > entities[i].freeze_time and entities[i].isFroze == True:
            if entities[0].x > entities[i].x:
                entities[i].y -= 34
                entities[i].x += 32
                entities[i].freeze_time = time.time() + 3
                entities[i].isFroze = False
                entities[i].wiggle = False
            else:
                entities[i].y -= 34
                entities[i].x -= 32
                entities[i].freeze_time = time.time() + 3
                entities[i].isFroze = False
                entities[i].wiggle = False
