"""
Gold Runner (Load Runner Redux)
By: Dalton Fox and Nathaniel Craiglow
ETGG1802:52
"""

import time
import pygame
import PaulsEditor
import os.path
import pygame.gfxdraw
import GoldRunnerMethods as methods
import GoldRunnerParticles as particles
import random

filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')  # assets directory for loading assets


class _Player(object):
    """
    The player class is used as a controller for the user to play Gold Runner
    """
    def __init__(self, x, y, lives=5):

        self.x = x
        self.y = y
        self.lives = lives
        self.facing = 0  # 0 is right 1 is left
        self.moving = True
        self.climbing = False
        self.escaping = False
        self.chests_collected = 0
        self.sound_delay = 0

        self.sprite = pygame.image.load(os.path.join(filepath, "sprite_sheet.png"))
        self.animationRight = []
        self.animationRight.append([160, 128])
        self.animationRight.append([160, 160])
        self.animationRight.append([160, 192])
        self.animationRight.append([160, 224])
        self.animationLeft = []
        self.animationLeft.append([160, 256])
        self.animationLeft.append([160, 288])
        self.animationLeft.append([160, 320])
        self.animationLeft.append([160, 352])
        self.animationFrame = 0
        self.animationTimer = time.time()
        self.animationUpdatePeriod = 0.095
        self.collision_set = methods.getCollisionSet(_map, self, tile_lists)

    def animationUpdate(self, surface):
        """
        :param surface: screen
        :return: update the player's animation
        """
        if not self.moving:
            self.animationFrame = 0  # Set the animation to starting position if we aren't moving

        elapsedTime = time.time() - self.animationTimer

        if self.moving and elapsedTime > self.animationUpdatePeriod:
            self.animationFrame += 1
            self.animationTimer = time.time()
            if self.animationFrame > 3:
                self.animationFrame = 0

        if self.climbing:
            self.animationFrame = 2  # If we are climbing set our frame to appear to climb

        if self.facing == 0:  # Set the animation to face left or right
            currentFrame = self.animationRight[self.animationFrame]
        if self.facing == 1:
            currentFrame = self.animationLeft[self.animationFrame]

        surface.blit(self.sprite, (self.x, self.y), (currentFrame[0], currentFrame[1], 32, 32))  # Draw the character

    def render(self, surface):
        """
        :param surface: screen
        :return: render our player, so update its animation and other things
        """
        self.animationUpdate(surface)  # Update our animation

        if debug == True:  # Only draw debug frames if the player is actually our player
            if len(self.collision_set) > 0:
                closestTile = self.collision_set[0]
                for collideTile in self.collision_set:
                    if collideTile.collideDistance < closestTile.collideDistance:
                        closestTile = collideTile

                    pygame.draw.line(screen, (0, 255, 0), (self.x + 16, self.y + 16), (collideTile.mapTileCenterX, collideTile.mapTileCenterY))
                pygame.draw.line(screen, (255, 0, 255), (self.x + 16, self.y + 16), (closestTile.mapTileCenterX, closestTile.mapTileCenterY), 3)
            pygame.draw.rect(screen, (255, 255, 255), (self.x + 5, self.y, 22, 32), 1)

    def update(self, enemies):
        """
        :return: check for collisions, update the player on user input, and update in accordance to other variables
        """
        # If we are touching something and moving left or right say we are moving (used for animation)
        if len(self.collision_set) > 0:
            if keysPressed[pygame.K_LEFT]:
                self.moving = True
            elif keysPressed[pygame.K_RIGHT]:
                self.moving = True
            else:
                self.moving = False
        else:
            self.moving = False

        # Bound the player on the screen
        if self.x < -5:
            self.x = -5
        if self.x > 835:
            self.x = 835
        if self.y > 512:
            self.y = 512

        # Update X
        (self.x, self.facing, self.collision_set, self.sound_delay) = methods.update_x(self, enemies, tile_lists, _map, keysPressed, slime_parts, sound_slime)

        # Update Y
        (self.y, self.climbing, self.collision_set) = methods.update_y(self, enemies, tile_lists, _map, keysPressed)
        if len(self.collision_set) > 0:
            for colliding_tile in self.collision_set:
                if colliding_tile.mapEntryKey == 'escapeLadder':
                    self.escaping = True

        # Check to collect gold
        if len(self.collision_set) > 0:
            for colliding_tile in self.collision_set:
                if colliding_tile.mapEntryKey == "gold":
                    _map.tileMap[colliding_tile.mapRow][colliding_tile.mapCol] = None
                    colliding_tile.mapEntryKey = _map.tileMap[colliding_tile.mapRow][colliding_tile.mapCol]
                    self.chests_collected += 1
                    sound_pop.play()

        # Check for trap doors
        if len(self.collision_set) > 0:
            for colliding_tile in self.collision_set:
                if colliding_tile.mapEntryKey == "trapGrass":
                    _map.tileMap[colliding_tile.mapRow][colliding_tile.mapCol] = 'trapGrassTripped'
                if colliding_tile.mapEntryKey == "trapStone":
                    _map.tileMap[colliding_tile.mapRow][colliding_tile.mapCol] = 'trapStoneTripped'
                if colliding_tile.mapEntryKey == "trapStoneBrick":
                    _map.tileMap[colliding_tile.mapRow][colliding_tile.mapCol] = 'trapStoneBrickTripped'
                if colliding_tile.mapEntryKey == "trapNetherBrick":
                    _map.tileMap[colliding_tile.mapRow][colliding_tile.mapCol] = 'trapNetherBrickTripped'
                if colliding_tile.mapEntryKey == "trapNether":
                    _map.tileMap[colliding_tile.mapRow][colliding_tile.mapCol] = 'trapNetherTripped'
                if colliding_tile.mapEntryKey == "trapObsidian":
                    _map.tileMap[colliding_tile.mapRow][colliding_tile.mapCol] = 'trapObsidianTripped'


class Enemy(object):
    """
    The enemy class is used as a controller for the user to play Gold Runner
    """
    def __init__(self, x, y):

        self.x = x
        self.y = y
        if random.randint(0, 1) == 0:
            self.direction = "right"
        else:
            self.direction = "left"
        self.vertical = "down"
        self.moving = True
        self.climbing = False
        self.has_chest = False
        self.sound_delay = 0
        self.isFroze = False
        self.wiggle = False
        self.freeze_time = time.time() + 3
        r = random.randint(3,5)
        self.dir_time = time.time() + r

        self.sprite = pygame.image.load(os.path.join(filepath, "sprite_sheet.png"))
        self.chest_sprite = pygame.image.load(os.path.join(filepath, "chest_icon.png"))
        self.animation = []
        self.animation.append([160, 0])
        self.animation.append([160, 32])
        self.animation.append([160, 64])
        self.animation.append([160, 96])
        self.wiggleanimation = []
        self.wiggleanimation.append([160, 384])
        self.wiggleanimation.append([160, 416])
        self.animationFrame = 0
        self.animationTimer = time.time()
        self.animationUpdatePeriod = 0.1
        self.collision_set = methods.getCollisionSet(_map, self, tile_lists)

    def animationUpdate(self, surface):
        """
        :param surface: screen
        :return: update the player's animation
        """
        if not self.moving:
            self.animationFrame = 0  # Set the animation to starting position if we aren't moving

        elapsedTime = time.time() - self.animationTimer

        if self.moving and not self.wiggle and elapsedTime > self.animationUpdatePeriod:
            self.animationFrame += 1
            self.animationTimer = time.time()
            if self.animationFrame > 3:
                self.animationFrame = 0
        elif self.wiggle == True and elapsedTime > self.animationUpdatePeriod + 0.05:
            self.animationFrame += 1
            self.animationTimer = time.time()
            if self.animationFrame > 1:
                self.animationFrame = 0

        if self.climbing:
            self.animationFrame = 2  # If we are climbing set our frame to appear to climb

        if self.wiggle == True and self.animationFrame <= 1:
            currentFrame = self.wiggleanimation[self.animationFrame]
        else:
            currentFrame = self.animation[self.animationFrame]

        surface.blit(self.sprite, (self.x, self.y), (currentFrame[0], currentFrame[1], 32, 32))  # Draw the character

    def render(self, surface):
        """
        :param surface: screen
        :return: render our player, so update its animation and other things
        """
        self.animationUpdate(surface)  # Update our animation

        if debug == True:  # Only draw debug frames if the player is actually our player
            if len(self.collision_set) > 0:
                closestTile = self.collision_set[0]
                for collideTile in self.collision_set:
                    if collideTile.collideDistance < closestTile.collideDistance:
                        closestTile = collideTile

                    pygame.draw.line(screen, (0, 255, 0), (self.x + 16, self.y + 16), (collideTile.mapTileCenterX, collideTile.mapTileCenterY))
                pygame.draw.line(screen, (255, 0, 255), (self.x + 16, self.y + 16), (closestTile.mapTileCenterX, closestTile.mapTileCenterY), 3)
            pygame.draw.rect(screen, (255, 255, 255), (self.x + 5, self.y, 22, 32), 1)
       
        if self.has_chest == True:
            self.chest_sprite.set_alpha(165)
            screen.blit(self.chest_sprite, (self.x+8, self.y-15))

    def update(self, index):
        """
        :return: check for collisions, update the player on user input, and update in accordance to other variables
        """
        # bounce enemies off the sides of the screen
        if self.x < -5:
            self.direction = "right"
        if self.x > 835:
            self.direction = "left"
        if self.y > 512:
            self.y = 512

        # check to switch directions
        if time.time() > self.dir_time:
            r = random.randint(3,5)
            self.dir_time = time.time() + r
            if self.direction == "right":
                self.direction = "left"
            elif self.direction == "left":
                self.direction = "right"

        if abs(self.y - Player.y) < 16:
            if Player.x > self.x:
                self.direction = "right"
            if Player.x < self.x:
                self.direction = "left"


        if Player.y < self.y:
            self.vertical = "up"
        if Player.y > self.y + 10:
            self.vertical = "down"

        other_entities = []  # We need to get a list of the other entities
        for enemy in enemy_list:
            other_entities.append(enemy)
        del other_entities[index]  # This makes sure we aren't counting our self in the other entities list

        # Update X
        (self.x, self.collision_set, self.sound_delay, self.direction) = methods.enemy_update_x(self, other_entities, tile_lists, _map, slime_parts, sound_slime)

        # Update Y
        (self.y, self.climbing, self.collision_set) = methods.enemy_update_y(self, other_entities, tile_lists, _map)

        global chests
        # Check to collect gold
        if len(self.collision_set) > 0:
            for colliding_tile in self.collision_set:
                if colliding_tile.mapEntryKey == "gold" and self.has_chest == False:
                    _map.tileMap[colliding_tile.mapRow][colliding_tile.mapCol] = None
                    colliding_tile.mapEntryKey = _map.tileMap[colliding_tile.mapRow][colliding_tile.mapCol]
                    self.has_chest = True
                    sound_pop.play()
                    chests = font.render('Chests Collected: '+str(Player.chests_collected)+'/6', 1, font_color)


class Overlay(object):
    """
    The Overlay class is used for creating a pause menu.
    Initially it was suppose to be usable for any 'menu' like overlay but there was only a need for a pause menu.
    """
    def __init__(self, screen, width = 360, height = 155):

        self.screen = screen
        self.width = width
        self.height = height
        self.halfx = ((screen.get_width() / 2) - (self.width / 2))
        self.halfy = ((screen.get_height() / 2) - (self.height / 2))

    def draw(self):
        # Create a loop within our main loop to "pause" the main loop and follow the "pause menu" loop
        while True:
            pygame.mixer.music.pause()
            # This is like a miniature game loop so we need the same initialization
            clock.tick(60)
            pygame.event.get()
            (mx, my) = pygame.mouse.get_pos()
            pygame.mouse.set_visible(True)
            keysPressed = pygame.key.get_pressed()

            # Draw Background
            if current_level <= 3:  # 1 - 4
                screen.blit(above_background, (0, 0), (0, 0, screen.get_width(), screen.get_height()))
            if current_level == 4 or current_level == 5 or current_level == 6:  # 5 - 7
                screen.blit(cave_background, (0, 0), (0, 0, screen.get_width(), screen.get_height()))
            if current_level == 7 or current_level == 8 or current_level == 9:  # 8 - 10
                screen.blit(nether_background, (0, 0), (0, 0, screen.get_width(), screen.get_height()))
            _map.renderMap(screen)
            pause_hud = pygame.Surface((screen.get_width(), screen.get_height()))  # kill me or let me use pscreen...
            pause_hud.set_alpha(165)
            pause_hud.fill((0, 0, 0))
            screen.blit(pause_hud, (0, 0))  # all that for a transparent rectangle because pygame.gfxdraw.rectangle doesn't fill?
            self.screen.blit(menu_art, (self.halfx, self.halfy), (self.halfx, self.halfy, self.width, self.height))
            pygame.draw.rect(self.screen, (0, 0, 0), (self.halfx, self.halfy, self.width, self.height), 4)  # Draw the text box outline
            pygame.draw.rect(self.screen, (255, 190, 0), (self.halfx, self.halfy, self.width, self.height), 3)

            # Draw Resume Button
            bt_resume_x = (screen.get_width() / 2) - 144
            bt_resume_y = (screen.get_height() / 2) - 75
            menu_actors[0].x = bt_resume_x + 285
            menu_actors[1].x = bt_resume_x - 25
            if mx > bt_resume_x + 10 and mx < bt_resume_x + 266 and my > bt_resume_y + 10 and my < bt_resume_y + 60:
                # When our mouse is over Resume (animate sprite) and if left mouse down break out of our menu loop and enter our game loop.
                if pygame.mouse.get_pressed()[0] == 1:
                    Quit = False
                    return Quit

                self.screen.blit(buttons, (bt_resume_x, bt_resume_y), (370, 70, 286, 70))  # glowing sprite
                for actor in menu_actors:
                    actor.y = bt_resume_y + 25
            else:
                self.screen.blit(buttons, (bt_resume_x, bt_resume_y), (370, 0, 286, 70))  # regular sprite
            if keysPressed[pygame.K_RETURN]:
                Quit = False
                return Quit
            # Draw Exit Button
            bt_exit_x = (screen.get_width() / 2) - 85
            bt_exit_y = (screen.get_height() / 2) + 5
            if mx > bt_exit_x + 10 and mx < bt_exit_x + 160 and my > bt_exit_y + 10 and my < bt_exit_y + 60:
                # When our mouse is over Exit (animate sprite) and if left mouse down break out of our menu loop, game loop, credit loop, and continue to quit.
                if pygame.mouse.get_pressed()[0] == 1:
                    Quit = True
                    self.screen.blit(buttons, (bt_exit_x, bt_exit_y), (0, 70, 180, 70))  # This is here so that the button doesn't disappear
                    return Quit

                self.screen.blit(buttons, (bt_exit_x, bt_exit_y), (0, 70, 180, 70))  # Glowing sprite
                for actor in menu_actors:
                    actor.y = bt_exit_y + 25
            else:
                self.screen.blit(buttons, (bt_exit_x, bt_exit_y), (0, 0, 180, 70))  # Regular sprite
            if keysPressed[pygame.K_RETURN]:
                Quit = False
                return Quit

            # Draw our little actors
            for actor in menu_actors:
                actor.render(screen)

            pygame.display.update()  # Still render things


'''~~~~~ INITIALIZATION ~~~~~'''
# Pygame Set-Up
pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
pygame.init()
screen_size = [864, 576]
font_size = 26
screen = pygame.display.set_mode(screen_size, pygame.SWSURFACE, 32)
font = pygame.font.SysFont("Arial", font_size, bold=True)  # basic font
pygame.display.set_caption('Gold Runner')
pygame.mouse.set_visible(False)


# Options
music = True
debug = False
pygame.mixer.music.set_volume(0.15)


# Game Set-Up`  `Tripped
clock = pygame.time.Clock()  # initialize engine clock
Pause = Overlay(screen)
dig_reload = 0
resetting = False
gameover = False
ground_tiles = ["grass.100", "dirt.100", "stone.100", "gravel.100","mossybrick.100",
                "crackedbrick.100","brick.100","netherbrick.100","netherack.100",
                "soulsand.100",
                "nodigMetal","nodigCoal","nodigGold","nodigDiamond","nodigObsidian","nodigBedrock"]
ladder_tiles = ["ladder", "escapeLadder", "beam"]
decoration_tiles = ["toadstool","mushroom","flowerRed","shrooms","shrub","tall_grass","flowerYellow","torch"]
unbreakable_tiles = ["nodigMetal","nodigCoal","nodigGold","nodigDiamond","nodigObsidian","nodigBedrock"]
trap_tiles = ['trapGrass',"trapStone","trapStoneBrick","trapNetherBrick","trapNether",
              "trapObsidian"]
regen_tiles = []
dev_tiles = ["enemy spawn", "player spawn"]
tile_lists = {'ground_tiles':ground_tiles, 'ladder_tiles':ladder_tiles, 'decoration_tiles':decoration_tiles, 'unbreakable_tiles':unbreakable_tiles, "trap_tiles":trap_tiles}
    # Artwork
menu_art = pygame.image.load(os.path.join(filepath, "Titlescreen.png")).convert()
credit_art = pygame.image.load(os.path.join(filepath, "Creditscreen.png")).convert()
buttons = pygame.image.load(os.path.join(filepath, "Buttons.png"))
above_background = pygame.image.load(os.path.join(filepath, "above_background.png")).convert()
cave_background = pygame.image.load(os.path.join(filepath, "cave_background.png")).convert()
nether_background = pygame.image.load(os.path.join(filepath, "nether_background.png")).convert()
game_over = pygame.image.load(os.path.join(filepath, "game_over.png"))
loading = pygame.image.load(os.path.join(filepath, "loading.png")).convert()
    # Sounds
sound_break_block = pygame.mixer.Sound(os.path.join(filepath, "break.ogg"))
sound_click = pygame.mixer.Sound(os.path.join(filepath, "click.ogg"))
sound_die = pygame.mixer.Sound(os.path.join(filepath, "die.ogg"))
sound_enemy_die = pygame.mixer.Sound(os.path.join(filepath, "enemy_die.ogg"))
sound_next_level = pygame.mixer.Sound(os.path.join(filepath, "next_level.ogg"))
sound_slime = pygame.mixer.Sound(os.path.join(filepath, "slime.ogg"))
sound_pop = pygame.mixer.Sound(os.path.join(filepath, "pop.ogg"))


# Map initialization
map_list = []
for i in range(1,11):
    s = "level "+str(i)+".txt"
    map_list.append(s)
current_level = 0
current_map = map_list[current_level]
current_tiles = "maptiles.txt"
    # Load Map
_map = PaulsEditor.TileMap()
_map.loadTileTypes(current_tiles)
_map.loadMap(current_map)
    # Load Objects
ladders = methods.getEscapeLadder(_map)
init_spawns = methods.spawnEnemies(_map)
respawns = methods.respawnEnemies(_map)


# Entity Initialization
    # Actors
menu_actors = [_Player(575, 225), Enemy(275, 225)]
    # Player
try:
    (spawnx, spawny) = methods.spawnPlayer(_map)
    Player = _Player(spawnx, spawny)
except:
    raise ValueError("Player Spawn does not exist")
    # Enemies
enemy_list = []
for i in range(len(init_spawns)):
    enemy_list.append(Enemy(init_spawns[i-1][1]*32,(init_spawns[i-1][0]*32)-4))

# Particles
block_parts = particles.ParticleSystem()
slime_parts = particles.ParticleSystem()

# updating entity list
entities = [Player]
for enemy in enemy_list:
    entities.append(enemy)

player_died = False

font_color = (255, 190, 0)
level = font.render("Level: "+str(current_level+1)+'/10', 1, font_color)
lives = font.render("Lives Left: "+str(Player.lives), 1, font_color)
chests = font.render('Chests Collected: '+str(Player.chests_collected)+'/6', 1, font_color)

screen.blit(loading, (0, 0))
pygame.display.update()
time.sleep(5)  # To load things


'''~~~~~ MENU LOOP ~~~~~'''
Menu = True
    # Play Music
if music:
    pygame.mixer.music.load(os.path.join(filepath, "minecraft_theme-gold_runner_cut.ogg"))
    pygame.mixer.music.play(-1)
while Menu:

    # Initialization
    clock.tick(60)
    pygame.mouse.set_visible(True)
    pygame.event.get()
    keysPressed = pygame.key.get_pressed()
    (mx, my) = pygame.mouse.get_pos()

    # Escape Sequence
    if keysPressed[pygame.K_ESCAPE]:
        Menu = False
        Game = False
        Credits = False
        sound_click.play()

    # Clear the Frame
    screen.fill((0, 0, 0))
    # Draw Artwork
    screen.blit(menu_art, (0, 0))

    # Draw Play Button
    bt_play_x = 350
    bt_play_y = 200
    if mx > bt_play_x + 10 and mx < bt_play_x + 170 and my > bt_play_y + 10 and my < bt_play_y + 60:
        # When our mouse is over Play (animate sprite) and if left mouse down break out of our menu loop and enter our game loop.
        if pygame.mouse.get_pressed()[0] == 1:
            Menu = False
            Game = True
            sound_click.play()
        screen.blit(buttons, (bt_play_x, bt_play_y), (180, 70, 190, 70))  # glowing sprite
        for actor in menu_actors:
            actor.y = 225
    else:
        screen.blit(buttons, (bt_play_x, bt_play_y), (180, 0, 190, 70))  # regular sprite

    # Draw Exit Button
    bt_exit_x = 353
    bt_exit_y = 325
    if mx > bt_exit_x + 10 and mx < bt_exit_x + 160 and my > bt_exit_y + 10 and my < bt_exit_y + 60:
        # When our mouse is over Exit (animate sprite) and if left mouse down break out of our menu loop, game loop, credit loop, and continue to quit.
        if pygame.mouse.get_pressed()[0] == 1:
            Menu = False
            Game = False
            Credits = False
            sound_click.play()
        screen.blit(buttons, (bt_exit_x, bt_exit_y), (0, 70, 180, 70))  # glowing sprite
        for actor in menu_actors:
            actor.y = 350
    else:
        screen.blit(buttons, (bt_exit_x, bt_exit_y), (0, 0, 180, 70))  # regular sprite

        # screen.blit(font.render(str(mx) + " " + str(my), 1, (255, 255, 255)), (mx, my))  # show our mouse x and mouse y for testing

    for actor in menu_actors:
        actor.render(screen)
    pygame.display.update()

if Game == True:
    screen.blit(loading, (0, 0))
    pygame.display.update()
    pygame.mixer.music.fadeout(3500)
    time.sleep(4)  # load things


'''~~~~~ GAME LOOP ~~~~~'''
    # Play Music
if music:
    pygame.mixer.music.load(os.path.join(filepath, "calm3_remix-gold_runner_cut.ogg"))
    pygame.mixer.music.play(-1)
while Game:

    # Initialize Input
    clock.tick(60)
    pygame.mouse.set_visible(False)
    pygame.event.get()
    keysPressed = pygame.key.get_pressed()
    (mx, my) = pygame.mouse.get_pos()

    # Escape Sequence
    if keysPressed[pygame.K_ESCAPE]:
        Quit = Pause.draw()
        sound_click.play()
        if Quit is True:
            Game = False
            Credits = False
        else:
            pygame.mixer.music.unpause()

    # Testing Code
    if keysPressed[pygame.K_1]:
        debug=True
    if keysPressed[pygame.K_2]:
        debug=False
    if debug == True:
        # Reset Level
        if keysPressed[pygame.K_r]:
            resetting = True
            Player.lives = 5
        # Credits Test
        if keysPressed[pygame.K_c]:
            Game = False
            Credits = True
        # Reset Player
        if keysPressed[pygame.K_h]:
            Player.x = spawnx
            Player.y = spawny
        # Escape ladder test
        if keysPressed[pygame.K_l]:
            methods.makeEscapeLadder(_map, ladders)

    # Breaking Blocks
    if keysPressed[pygame.K_x] and time.time() > dig_reload:
        regen_tiles.append(methods.breakBlock(_map, Player, 0, tile_lists, block_parts, sound_break_block))
        # Limit Input
        dig_reload = time.time() + 0.25
    if keysPressed[pygame.K_z] and time.time() > dig_reload:
        regen_tiles.append(methods.breakBlock(_map, Player, 1, tile_lists, block_parts, sound_break_block))
        # Limit Input
        dig_reload = time.time() + 0.25

    for tile in regen_tiles:
        if tile == None:
            regen_tiles.remove(tile)
    if len(regen_tiles) > 0:
        (regen_tiles, player_died) = methods.regenTiles(regen_tiles, _map, entities, respawns, sound_enemy_die)
        methods.enemyEscape(regen_tiles,entities)

    for enemy in enemy_list:
        if methods.collidingCircles(Player.x + 16, Player.y + 16, 11, enemy.x + 16, enemy.y + 16, 11):
            player_died = True  # THE PLAYER DIED

    # Player has all chest and ladders appears
    if Player.chests_collected == 6:
        methods.makeEscapeLadder(_map, ladders)
    # Load next level
    if Player.y < 0 and Player.escaping:
        if current_level < 9:
            current_level += 1
            Player.lives += 1
            current_map = map_list[current_level]
            _map.loadMap(current_map)
            ladders = methods.getEscapeLadder(_map)
            spawns = methods.spawnEnemies(_map)
            respawns = methods.respawnEnemies(_map)
            resetting = True
        else:
            screen.blit(loading, (0, 0))
            pygame.display.update()
            time.sleep(1)  # load things
            Game = False
            Credits = True

    if player_died:
        sound_die.play()
        Player.lives -= 1
        lives = font.render("Lives Left: "+str(Player.lives), 1, font_color)
        _map.loadMap(current_map)
        Player.x = spawnx
        Player.y = spawny
        regen_tiles = []
        Player.chests_collected = 0
        ladders = methods.getEscapeLadder(_map)
        init_spawns = methods.spawnEnemies(_map)
        respawns = methods.respawnEnemies(_map)
        enemy_list = []
        for i in range(len(init_spawns)):
            enemy_list.append(Enemy(init_spawns[i-1][1]*32,(init_spawns[i-1][0]*32)-4))
        entities = [Player]
        for enemy in enemy_list:
            entities.append(enemy)
        player_died = False

    # reset values
    if resetting:
        _map.loadMap(current_map)
        screen.blit(loading, (0, 0))
        pygame.display.update()
        sound_next_level.play()
        (spawnx, spawny) = methods.spawnPlayer(_map)
        Player = _Player(spawnx, spawny, Player.lives)
        init_spawns = methods.spawnEnemies(_map)
        respawns = methods.respawnEnemies(_map)
        ladders = methods.getEscapeLadder(_map)
        regen_tiles = []
        enemy_list = []
        level = font.render("Level: "+str(current_level+1)+'/10', 1, font_color)
        for i in range(len(init_spawns)):
            enemy_list.append(Enemy(init_spawns[i-1][1]*32,(init_spawns[i-1][0]*32)-4))
        entities = [Player]
        for enemy in enemy_list:
            entities.append(enemy)
        resetting = False
        player_died = False

    # If player has no lives left, end the game
    if Player.lives == 0:
        screen.blit(loading, (0, 0))
        pygame.display.update()
        time.sleep(1)  # load things
        gameover = True
        Game = False
        Credits = True

    # Clear the Frame
    screen.fill((0, 0, 0))
    # Draw Background
    if current_level <= 3:  # 1 - 4
        screen.blit(above_background, (0, 0), (0, 0, screen.get_width(), screen.get_height()))
    if current_level == 4 or current_level == 5 or current_level == 6:  # 5 - 7
        screen.blit(cave_background, (0, 0), (0, 0, screen.get_width(), screen.get_height()))
    if current_level == 7 or current_level == 8 or current_level == 9:  # 8 - 10
        screen.blit(nether_background, (0, 0), (0, 0, screen.get_width(), screen.get_height()))

    _map.renderMap(screen)

    # Player update
    Player.update(enemy_list)
    Player.render(screen)

    # Enemy update
    enemy_index = 0
    for enemy in enemy_list:
        enemy.update(enemy_index)
        enemy.render(screen)
        enemy_index += 1

    block_parts.update_particles()
    block_parts.render_particles(screen)
    slime_parts.update_particles()
    slime_parts.render_particles(screen)

    # Render text at bottom
    font_color = (255, 190, 0)
    hud = pygame.Surface((screen.get_width(), 32))
    hud.set_alpha(200)
    hud.fill((0, 0, 0))
    screen.blit(hud, (0, 544))
    pygame.draw.rect(screen, (0, 0, 0), (0, 544, screen.get_width()-1, 30), 4)
    pygame.draw.rect(screen, (255, 190, 0), (0, 544, screen.get_width()-1, 30), 2)

    # Finish Render and Update
    screen.blit(level, (5, 545))
    screen.blit(lives, (695, 545))
    screen.blit(chests, (345, 545))

    #screen.blit(font.render(str(mx) + " " + str(my), 1, (255, 255, 255)), (mx, my))

    pygame.display.update()

if Credits != False:
    screen.blit(loading, (0, 0))
    pygame.display.update()
    pygame.mixer.music.fadeout(3500)
    time.sleep(2)  # load things


'''~~~~~ CREDIT LOOP ~~~~~'''
    # Play Music
if music:
    pygame.mixer.music.load(os.path.join(filepath, "dead_voxel-gold_runner_cut.ogg"))
    pygame.mixer.music.play(-1)
while Credits:

    # Initialization
    clock.tick(60)
    pygame.mouse.set_visible(True)
    pygame.event.get()
    keysPressed = pygame.key.get_pressed()
    (mx, my) = pygame.mouse.get_pos()

    # Escape Sequence
    if keysPressed[pygame.K_ESCAPE]:
        Credits = False

    # Clear the Frame
    screen.fill((0, 0, 0))
    # Draw Artwork
    screen.blit(credit_art, (0, 0))

    # Draw Exit Button
    bt_exit_x = 350
    bt_exit_y = 485
    if mx > bt_exit_x + 10 and mx < bt_exit_x + 160 and my > bt_exit_y + 10 and my < bt_exit_y + 60:
        # When our mouse is over Exit (animate sprite) and if left mouse down break out of our menu loop, game loop, credit loop, and continue to quit.
        if pygame.mouse.get_pressed()[0] == 1:
            Credits = False
            sound_click.play()
        screen.blit(buttons, (bt_exit_x, bt_exit_y), (0, 0, 180, 70))  # glowing sprite
    else:
        screen.blit(buttons, (bt_exit_x, bt_exit_y), (0, 70, 180, 70))  # regular sprite

        # screen.blit(font.render(str(mx) + " " + str(my), 1, (255, 255, 255)), (mx, my))  # show our mouse x and mouse y for testing

    if gameover == True:
        screen.blit(game_over, (143, 50))

    pygame.display.update()


# Escape Our Program
time.sleep(0.5)  # unload things
pygame.mixer.quit()
pygame.quit()
