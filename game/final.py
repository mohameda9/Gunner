import pygame
import random as rand
import sys

pygame.init()
clock = pygame.time.Clock()

Screen_Width = 1024

play = True
Screen_Height = 512

screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption('Game') 


moving_left = False
moving_right = False
x = 200
y =200
scale =10

bullets = []
mapTiles = []

section = 0
offsetX = 0

mapscale = 2
tileWidth, tileHeight = 16 * mapscale, 16 * mapscale


def generateMap():
    xRange, yRange = ((int)(4 * Screen_Width / tileWidth), (int)(Screen_Height / tileHeight))
    tileSprite = pygame.image.load('./pics/Tileset/GroundTileset_16x16.png').convert_alpha()
    tileSprite = pygame.transform.scale(tileSprite, (tileSprite.get_width()*mapscale, tileSprite.get_height()*mapscale)) 
    
    tiles = []
    islands = []
    
    start = 2
    prevStart = start
    
    def findStretch(xStart, yLevel):
        length = 0
        for x in range(xStart, 0, -1):
            if tiles[x][yLevel] != -1:
                length += 1
            else:
                break
            
        return length
    
    for x in range(xRange):
        c = [-1] * (yRange)
        hasIsland = False
        
        for y in range(0, yRange):
            isStart = (y >= start and (rand.randrange(10) <= (2) or  y >= start + 3)) or findStretch(x-1, y) == 1
            
            try:
                val = tiles[x-1][y]
                if val == 0:
                    #mapTiles.append(Tile((x-1, y), (tileWidth, tileHeight), 7, tileSprite))
                    tiles[x-1][y] = 7
                elif val == 1 and not isStart:
                    tiles[x-1][y] = 3
                    pass
            except:
                pass
            
            if x > 0 and y >= 1 and y <= 3 and rand.randrange(50) <= 1 and not hasIsland:
                islands.append((x, y))
                
                hasIsland = True

            if isStart:
                if (rand.randrange(10) <= 1):
                    enemies.append(Enemy((x * tileWidth, (y - 1) * tileHeight), 20))
                                         
                c[y] = 1 #Dirt with grass layer on the top (16, 0)
                
                try:
                    if (tiles[x-1][y] == -1):
                        c[y] = 6 #Dirt with grass layer on the top and left (0, 0)
                    elif (tiles[x-1][y] == 0):
                        mapTiles.append(Tile((x-1, y), (tileWidth, tileHeight), 0, tileSprite))
                        tiles[x-1][y] = 6
                    elif (tiles[x-1][y] == 7):
                        mapTiles.append(Tile((x-1, y), (tileWidth, tileHeight), 7, tileSprite))
                        tiles[x-1][y] = 6
    
                except:
                    pass
                
                start = y - 2
                prevStart = y
                
                if (start < 5):
                    start = 5

                for j in range(y + 1, yRange):
                    c[j] = 0 #Dirt (16, 16)
                    
                    try:
                        if (tiles[x-1][j] == -1):
                            c[j] = 4 #Dirt with grass layer on left (0, 16)
  
                        elif (c[j-1] == 4):
                            mapTiles.append(Tile((x, j), (tileWidth, tileHeight), 4, tileSprite))
                            c[j] = 5;
                            print((x + 1, j + 1))
                        elif (c[j-1] == 6):
                            mapTiles.append(Tile((x, j), (tileWidth, tileHeight), 0, tileSprite))
                            c[j] = 1
                            print((x + 1, j + 1))
                    except:
                        continue
                    '''
                    if (c[j] == 0):
                        try:
                            if (tiles[x-1][j] != 0):
                                tiles[x-1][j] = 3
                        except:
                            pass
                            
                    try:
                        if (tiles[x-1
                    except:
                        pass
                        '''
                break;
            else:
                try:
                    toLeft = tiles[x-1][y]
                    
                    if (toLeft == 0):
                        toLeft = 2 #Dirt with grass layer on right (32, 16)
                    elif (toLeft == 1):
                        toLeft = 3 #Dirt with grass layer on top and right (32, 0)
                    
                    tiles[x-1][y]
                except:
                    pass
        tiles.append(c)
                  
    for x in range(len(tiles)):
        for y in range(len(tiles[x])):
            if tiles[x][y] != -1:
                mapTiles.append(Tile((x, y), (tileWidth, tileHeight), tiles[x][y], tileSprite))
                
            #print(tiles[x])
            #print("------------\n")                
                    
        #mapTiles.append(Tile((x, j), (tileWidth, tileHeight), c[j], tileSprite))
    
    for island in islands:
        off = rand.random() * 16
        mapTiles.append(Tile(island, (tileWidth, tileHeight), 3, tileSprite, off))
        mapTiles.append(Tile((island[0]-1, island[1]), (tileWidth, tileHeight), 6, tileSprite, off))
        
    print(len(mapTiles))
 
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, tType, sprite, off = 0):
        self.is_collided = False
        self.gpos = pos
        self.pos = (pos[0] * size[0] + off, pos[1] * size[1])
        self.sprite = sprite
        
        #print(self.pos)
        
        if tType == 0:
            self.image = sprite.subsurface(size[0], size[1], *size)
        elif tType == 1:
            self.image = sprite.subsurface(size[0], 0, *size)
        elif tType == 2:
            self.image = sprite.subsurface(size[0] * 2, 0, *size)
        elif tType == 3:
            self.image = sprite.subsurface(size[0] * 2, 0, *size)
        elif tType == 4:
            self.image = sprite.subsurface(0, size[1], *size)
        elif tType == 5:
            self.image = sprite.subsurface(size[0]*2, 0, *size)
        elif tType == 6:
            self.image = sprite.subsurface(0, 0, *size)
        elif tType == 7:
            self.image = sprite.subsurface(size[0]*2, size[1], *size)
        elif tType == 8:
            self.image = sprite.subsurface(0, size[1] * 2, *size)
        elif tType == 9:
            self.image = sprite.subsurface(size[0]*2, size[1]*2, *size)
            
        self.rect = pygame.rect.Rect(*self.pos, *size)
            
            
        #self.rect = (0, 0, 16 * size[0], 16 * size[1])
            
    def update(self):
        if screen.get_rect().colliderect(self.rect):
            self.show()
        self.rect.x = self.pos[0] - offsetX
        
        #if self.is_collided:
         #   pygame.draw.rect(screen, (0, 255, 0), self.rect, 5)
        #else:
         #   pygame.draw.rect(screen, (200, 200, 200), self.rect, 3)
        
    def show(self):
        screen.blit(self.image, (self.pos[0] - offsetX, self.pos[1]))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, vel, bType, shotByPlayer=False):
        self.x, self.y = pos
        self.velX, self.velY = vel
        self.is_done = False
        self.shotByPlayer = shotByPlayer

        self.bulletImpact = []
        
        if (bType == "Gunner"):
            self.bulletImg = pygame.image.load('./pics/FX/PlayerProjectile.png')
            for i in range(3):
                self.bulletImpact.append(pygame.image.load('./pics/FX/Projectile_Impact_'+str(i+1)+'.png'))
            
            self.biidx = 0
            self.maxbiidx = 2
            
        self.rect = self.bulletImg.get_rect()
        self.rect.center = pos
        
        self.has_impacted = False
        self.image = self.bulletImg
        self.lastTime = 0
        
    def update(self, dt):
        self.show()
        
        if (not self.has_impacted):
            self.checkCollision()
            self.move(dt)
        else:
            self.image = self.bulletImpact[self.biidx]
            currentTime = pygame.time.get_ticks()
            
            if currentTime-self.lastTime >= 100:
                self.biidx+=1
                self.lastTime = currentTime
        
        if self.biidx>= len(self.bulletImpact):
            self.biidx = 0
            self.is_done = True
            
        if self.rect.x > Screen_Width or self.rect.x < 0:
            self.is_done = True

        
    def show(self):
        screen.blit(self.image, self.rect)
        
    def move(self, dt):
        self.velY += 9.8 * dt / 4
        
        self.rect.x += self.velX
        self.rect.y += self.velY
        
    def checkCollision(self):
        gx = (int)(self.rect.centerx / tileWidth)
        
        if (self.shotByPlayer):
            for enemy in enemies:
                if (abs((int)(enemy.rect.centerx / tileWidth) - gx) > 1):
                    continue;
                
                if enemy.rect.colliderect(self.rect):
                    self.has_impacted = True
                    self.lastTime = pygame.time.get_ticks()
                    enemy.index = 0
                    enemy.lastTime = 0
                    
                    if self.velX > 0:
                        self.x = enemy.rect.x
                    else:
                        self.x = enemy.rect.x + enemy.rect.w
                    
                    self.velX = 0
                    self.velY = 0
                    
                    enemy.alive = False
                    return
        else:
            if player.rect.colliderect(self.rect):
                self.has_impacted = True
                self.lastTime = pygame.time.get_ticks()
                player.health -= 15
                
                if self.velX > 0:
                    self.x = player.rect.x
                else:
                    self.x = player.rect.x + player.rect.w
                
                self.velX = 0
                self.velY = 0
                return            
        
        for tile in mapTiles:
            tile.is_collided = False
            
            if (abs((int)(tile.rect.centerx / tileWidth) - gx) > 1):
                continue
            
            if tile.rect.colliderect(self.rect):
                self.has_impacted = True
                self.lastTime = pygame.time.get_ticks()
                
                if self.velX > 0:
                    self.x = tile.rect.x
                else:
                    self.x = tile.rect.x + tile.rect.w
                
                self.velX = 0
                self.velY = 0
                break

class Player(pygame.sprite.Sprite) :
    def __init__(self,pace, x,y, scale, Type):
        pygame.sprite.Sprite.__init__(self)
        self.pace = pace
        self.Type = Type
        #print(self.Type)
        self.idle_list =[]
        self.walk_list =[]
        self.animation_list= []
        self.jump_list = [];
        self.index =0
        self.health = 100
        
        self.behavior = 0
        
        self.velY = 0
        
        self.is_moving_right = False
        self.is_moving_left = False
        self.is_jumping = False
        self.is_grounded = True;
        
        self.is_allowed = [True] * 2
        
        scale = 1
        
        for i in range(4):
            directory = './pics/'+str(self.Type)+'/idle/'+str(i)+'.png'
            print(directory)
            image = pygame.image.load(directory)
            image = pygame.transform.scale(image, ((int)(image.get_width()*scale), (int)(image.get_height()*scale))) 
            self.idle_list.append(image)
        
        for i in range(8):
            directory = './pics/'+str(self.Type)+'/Walk/Gunner_Walk_'+str(i)+'.png'
            print(directory)
            image = pygame.image.load(directory)
            image = pygame.transform.scale(image, ((int)(image.get_width()*scale), (int)(image.get_height()*scale))) 
            self.walk_list.append(image)
        
        jumpImg = pygame.image.load('./pics/'+str(self.Type)+'/Gunner_Rise.png')
        jumpImg = pygame.transform.scale(jumpImg, ((int)(jumpImg.get_width()*scale), (int)(jumpImg.get_height()*scale)))
        self.jump_list.append(jumpImg)
        
        del jumpImg
            
        self.animation_list.append(self.idle_list)
        self.animation_list.append(self.walk_list)
        self.animation_list.append(self.jump_list)
        
        self.image = self.animation_list[self.behavior][self.index]
        
        self.image2 = pygame.transform.flip(self.image, True, False)        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)   
        self.flip = False
        self.lastTime = pygame.time.get_ticks()
        
        self.time_since_key_press = 0
        
        self.col_points = [(self.rect.centerx + self.rect.w / 2, self.rect.centery), (self.rect.centerx - self.rect.w / 2, self.rect.centery), (self.rect.centerx, self.rect.y + self.rect.h)]
        
    
    def update(self, dt):
        self.col_points = [(self.rect.centerx + self.rect.w / 2, self.rect.centery), (self.rect.centerx - self.rect.w / 2, self.rect.centery), (self.rect.centerx, self.rect.y + self.rect.h + 4), (self.rect.centerx, self.rect.y)]
        #print(self.col_points)
        
        Animation_timer = 50
        currentTime = pygame.time.get_ticks()
                
        
        if currentTime-self.lastTime >=Animation_timer:
            self.index+=1
            self.lastTime = currentTime
        
        if self.index>= len(self.animation_list[self.behavior]):
            self.index = 0

        self.image = self.animation_list[self.behavior][self.index]
        self.image2 = pygame.transform.flip( self.image, True, False) 
        
        self.checkCollisions()
        self.show()
        self.checkKeyInput(dt)
        self.move(dt)
        
        
    def show(self):
        
        if self.flip ==False:
            image = self.image
        else:
            image = self.image2
        
        
        #pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(image, self.rect)
        
    
    def move(self, dt):
        x_change = 0
        
        if self.is_moving_left == False and self.is_moving_right == False and self.is_grounded == True:
            self.behavior=0
            
        if self.is_moving_left ==True:
            x_change = -self.pace
            self.flip = True
            self.behavior=1
            
        elif self.is_moving_right ==True:
            x_change = self.pace
            self.flip = False
            self.behavior=1
         
        if self.is_jumping == True:
            self.velY = -5
            self.is_jumping = False
        
        if self.is_grounded == False:
            self.behavior = 2
            self.velY += 9.8 * dt
        else:
            self.velY = 0;
            
        #print(x_change)
        self.rect.x = self.rect.x + x_change
        self.rect.y = self.rect.y + self.velY
    
    def checkCollisions(self):
        gx = (int)(self.rect.centerx / tileWidth)
        
        allow = [True] * 2
        self.is_grounded = False;
        
        for tile in mapTiles:
            tile.is_collided = False
            if (abs((int)(tile.rect.centerx / tileWidth) - gx) > 1):
                continue
            
            if tile.rect.collidepoint(self.col_points[0]):
                allow[0] = False
                tile.is_collided = True
            
            if tile.rect.collidepoint(self.col_points[1]):
                allow[1] = False    
                tile.is_collided = True
        
            if tile.rect.collidepoint(self.col_points[2]):
                self.is_grounded = True
                self.rect.y = tile.rect.y - self.rect.h
                tile.is_collided = True
                
            if tile.rect.collidepoint(self.col_points[3]):
                self.velY *= -1
                self.rect.y += self.velY
                
        self.is_allowed = allow
        
        
    def checkKeyInput(self, dt):
        #print(self.is_grounded)
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT] and self.is_allowed[0]:
            self.is_moving_right = True
        else:
            self.is_moving_right = False
            
        if keys[pygame.K_LEFT] and self.is_allowed[1]:
            self.is_moving_left = True
        else:
            self.is_moving_left = False
        
        if keys[pygame.K_UP] and self.is_grounded:
            self.is_jumping = True
            self.is_grounded = False;
            
        if keys[pygame.K_SPACE] and self.time_since_key_press > 0.05:
            if self.flip:
                bullets.append(Bullet((self.rect.centerx - self.rect.w/2, self.rect.centery - self.rect.h / 8), (-15, 0), "Gunner", True))
            else:
                bullets.append(Bullet((self.rect.centerx + self.rect.w/2, self.rect.centery - self.rect.h / 8), (15, 0), "Gunner", True))
            self.time_since_key_press = 0
        
        self.time_since_key_press += dt
        
    def UI(self):
        pygame.draw.rect(screen, (100, 100, 100), (10, 10, 200, 30))
        pygame.draw.rect(screen, (0, 200, 0), (15, 15, 190 * self.health/100, 20))
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        self.alive = True
        self.is_done = False
        self.pos = pos
        self.speed = speed
        self.Type = "Gunner"
        
        self.idle_list =[]
        self.hurt_list =[]
        self.animation_list= []
        self.index =0
        
        self.behavior = 0        
        
        for i in range(4):
            directory = './pics/'+str(self.Type)+'/idle/'+str(i)+'.png'
            image = pygame.image.load(directory)
            image.fill((255, 0, 0), special_flags=pygame.BLEND_ADD)
            #image = pygame.transform.scale(image, ((int)(image.get_width()*scale), (int)(image.get_height()*scale))) 
            image = pygame.transform.scale(image, (32, 32)) 
            
            self.idle_list.append(image)
        
        for i in range(4):
            directory = './pics/'+str(self.Type)+'/Gunner_Hurt_'+str(i+1)+'.png'
            image = pygame.image.load(directory)
            image.fill((255, 0, 0), special_flags=pygame.BLEND_ADD)
            image = pygame.transform.scale(image, ((int)(image.get_width()*scale), (int)(image.get_height()*scale))) 
            
            self.hurt_list.append(image)
        
        self.animation_list.append(self.idle_list)
        self.animation_list.append(self.hurt_list)
        #self.animation_list.append(self.jump_list)
            
        self.image = self.animation_list[self.behavior][self.index]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0];
        self.rect.y = pos[1]
        
        self.flip = False
        self.lastTime = pygame.time.get_ticks()     
        self.time_since_key_press = 0
        self.ammo = 30
        self.readyToShoot = True
        self.reactionTime = rand.randrange(4)
        
    def update(self, dt, player):
        self.col_points = [(self.rect.centerx + self.rect.w / 2, self.rect.centery), (self.rect.centerx - self.rect.w / 2, self.rect.centery), (self.rect.centerx, self.rect.y + self.rect.h + 4), (self.rect.centerx, self.rect.y)]
        #print(self.col_points)
        
        Animation_timer = 50
        currentTime = pygame.time.get_ticks()
                
        
        if currentTime-self.lastTime >=Animation_timer:
            self.index+=1
            self.lastTime = currentTime
        
        if self.index>= len(self.animation_list[self.behavior]):
            self.index = 0
            if (not self.alive):
                self.is_done = True
        
        #print(self.index)
        
        #if self.is_grounded == True:
            #self.image = self.animation_list[self.behavior][self.index]
        #else:
            #self.image = self.animation_list[self.behavior][0]

        self.image = self.animation_list[self.behavior][self.index]
        self.image2 = pygame.transform.flip(self.image, True, False) 
        
        #self.checkCollisions()
        self.show()
        #self.checkKeyInput(dt)
        #self.move(dt)    
        if (self.alive):
            self.act(player, dt)
        else:
            self.behaviour = 1;
        
    def act(self, player, dt):
        self.time_since_key_press += dt
        
        if (player.rect.x < self.rect.x):
            self.flip = True
        else:
            self.flip = False
            
        if (self.ammo <= 0):
            self.readyToShoot = False
        else:
            self.readyToShoot = True
            
        if (self.readyToShoot):
            if (abs(player.rect.centery - self.rect.centery) < 32) and abs(player.rect.centerx - player.rect.centerx) < 32 * 4 and self.time_since_key_press > 0.5 + self.reactionTime:
                if self.flip:
                    bullets.append(Bullet((self.rect.centerx - self.rect.w/2, self.rect.centery - self.rect.h / 8), (-15, 0), "Gunner"))
                else:
                    bullets.append(Bullet((self.rect.centerx + self.rect.w/2, self.rect.centery - self.rect.h / 8), (15, 0), "Gunner"))
                
                self.ammo-=1
                self.time_since_key_press = 0      
        elif  (self.time_since_key_press > 3):
            self.ammo = 30
            
            
        
    def show(self):
        
        if self.flip ==False:
            image = self.image
        else:
            image = self.image2
        
        
        #pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(image, self.rect)    
        
player = Player(2, 200,200,3,"Gunner")
enemies = []

generateMap()

while play:
    for event in pygame.event.get(): 
        if event.type== pygame.QUIT:
            sys.exit("Goodbye")
            
    if (player.health) <= 0:
        sys.exit("Gameover")
    clock.tick(60)
    dt = clock.get_time() / 1000;
    
    screen.fill((100, 50, 255))
    
    #player.update(dt)

    for bullet in reversed(bullets):
        bullet.update(dt)
        if (bullet.is_done):
            bullets.remove(bullet)
        
    for tile in mapTiles:
        tile.update()
        
    for enemy in reversed(enemies):
        enemy.update(dt, player)
        if (enemy.is_done):
            enemies.remove(enemy)
        
    player.update(dt)
            
    if player.rect.x + player.rect.w >= Screen_Width and offsetX == section * Screen_Width:
        section+=1
    elif player.rect.x < 0 and offsetX != 0 and offsetX == section * Screen_Width:
        section -= 0;
    
    if section * Screen_Width != offsetX:
        if (offsetX < Screen_Width * section):
            offsetX += 16
            player.rect.x -= 16
            for enemy in enemies:
                enemy.rect.x -= 16
        elif (offsetX > Screen_Width * offsetX):
            offsetX -= 16
            player.rect.x += 16
            for enemy in enemies:
                enemy.rect.x += 16   
                
    player.UI()
    pygame.display.flip()
    

        
        
            
    