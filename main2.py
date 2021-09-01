import pygame
import sys
import os
import time
import neat
import math
import pickle
import multiprocessing
'''
Variables
'''
e = False
worldx = 960
worldy = 720
fps = 40
ani = 3
world = pygame.display.set_mode([worldx, worldy])
BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (34, 177, 76)
steps = 10
pygame.display.set_caption("game AI")
'''
Objects
'''


class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []
        img = pygame.image.load(os.path.join('images', 'hero.png'))
        # img.convert_alpha()  # optimise alpha
        # img.set_colorkey(ALPHA)  # set alpha
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.a = True

    def die(self):
        self.a = False
        self.rect.y = 1500

    def live(self):
        return self.a

    def control(self, x, y):
        """
        control player movement
        """
        self.movex += x
        self.movey += y

    def update(self, stepx, stepy):
        """
        Update sprite position
        """
        # self.rect.x = self.rect.x + self.movex
        # self.rect.y = self.rect.y + self.movey

        self.rect.x = self.rect.x + stepx
        self.rect.y = self.rect.y + stepy

        # moving left


class boundry1(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = pygame.image.load(os.path.join('images', 'boundry.png'))
        # img.convert_alpha()  # optimise alpha
        # img.set_colorkey(ALPHA)  # set alpha
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x  # go to x
        self.rect.y = y


class enemy(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self, world, y):
        pygame.sprite.Sprite.__init__(self)
        # print ("created a new sprite:", id(self))
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []
        img = pygame.image.load(os.path.join('images', 'enemy.png'))
        # img.convert_alpha()  # optimise alpha
        # img.set_colorkey(ALPHA)  # set alpha
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 50  # go to x
        self.rect.y = y
        self.a = 0
        # self.rect.y = 100 * enemycount  # go to y

    def die(self):
        self.a = 0
        self.rect.y = -500

    def spawn(self, y):
        self.a = 1
        self.rect.y = y

    def live(self):
        return self.a


class bullet(pygame.sprite.Sprite):
    def __init__(self, enemycount):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []
        img = pygame.image.load(os.path.join('images', 'bullet.png')).convert()
        img.convert_alpha()  # optimise alpha
        img.set_colorkey(ALPHA)  # set alpha
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 10000  # go to x
        self.rect.y = 10  # go to y

    def control(self, x, y):
        self.rect.x = x
        self.rect.y = y + 15
        self.movex = -5

    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey


class enemybullet(pygame.sprite.Sprite):
    def __init__(self, enemycount):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []
        img = pygame.image.load(os.path.join('images', 'bullet.png')).convert()
        img.convert_alpha()  # optimise alpha
        img.set_colorkey(ALPHA)  # set alpha
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = -10000  # go to x
        self.rect.y = 10  # go to y

    def control(self, x, y):
        self.rect.x = x + 53
        self.rect.y = y + 17
        self.movex = 5

    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey


'''
Setup
'''

backdrop = pygame.image.load(os.path.join('images', 'stage.png'))
circle = pygame.image.load(os.path.join('images', 'hero1.png'))
over = pygame.image.load(os.path.join('images', 'over.png'))
blk = pygame.image.load(os.path.join('images', 'black.png'))
level1 = pygame.image.load(os.path.join('images', 'level1.png'))
level1s = pygame.image.load(os.path.join('images', 'level1small.png'))
level2 = pygame.image.load(os.path.join('images', 'level2.png'))
level2s = pygame.image.load(os.path.join('images', 'level2small.png'))
end = pygame.image.load(os.path.join('images', 'end.png'))
over.convert_alpha()
over.set_colorkey(ALPHA)
clock = pygame.time.Clock()
pygame.init()
backdropbox = world.get_rect()

main = True

'player = Player()  # spawn playere'
'player.rect.x = 850  # go to x'
'player.rect.y = 250  # go to y'
player_list = pygame.sprite.Group()
'player_list.add(player)'
boundry = boundry1(50, 0)
topb = boundry1(500, -780)
bottomb = boundry1(500, 780)
behindb = boundry1(1000, 0)
b_list = pygame.sprite.Group()
b_list.add(boundry)
b_list.add(topb)
b_list.add(bottomb)
b_list.add(behindb)
# player2 = Player()  # spawn player
# print(player_list.sprites())
'''
enemies = pygame.sprite.Group()
enemiesbullets = pygame.sprite.Group()
'''
'bullet = bullet()'
# bullet.rect.x=1000
bullet_list = pygame.sprite.Group()
'bullet_list.add(bullet)'

'''
Main Loop
'''
gen = 0
enemies1 = pygame.sprite.Group()
enemies2 = pygame.sprite.Group()
enemies3 = pygame.sprite.Group()
enemiesbullets1 = pygame.sprite.Group()
enemiesbullets2 = pygame.sprite.Group()
enemiesbullets3 = pygame.sprite.Group()


def playerkill(id, ge, nets, player, level, enemycount, edead):
    global player_list, main, k, colid, e, ed, adead, playerdead, p1shot, start, eshot
    global bullet_list, enemies1, enemies2, enemies3, enemiesbullets1, enemiesbullets2, enemiesbullets3
    ge[id].fitness -= 1
    nets.pop(id)
    ge.pop(id)
    player.kill()

    enemycount.pop(id)
    edead.pop(id)
    enemies1.sprites()[id].kill()
    enemies2.sprites()[id].kill()

    if level[id] == 2:
        enemiesbullets3.sprites()[id].kill()
        enemies3.sprites()[id].kill()
    level.pop(id)
    enemiesbullets1.sprites()[id].kill()
    enemiesbullets2.sprites()[id].kill()
    # playerdead = True
    bullet_list.sprites()[id].kill()


def eval_genomes(genomes, config):
    global player_list, main, k, colid, e, ed, edead, level, adead, playerdead, p1shot, enemycount, start, eshot
    global bullet_list, enemies1, enemies2, enemies3, enemiesbullets1, enemiesbullets2, enemiesbullets3, gen,p
    population = 20
    e = False
    gen += 1
    enemycount = []
    edead = []
    playerdead = False
    colid = False
    wcolid = False
    b = False
    k = ''
    w = ''
    eshot = time.time() - 5
    level = []
    playeralive = []
    adead = time.time()
    start = time.time()
    ed = False
    nets = []
    ge = []
    en1 = []
    en2 = []
    en3 = []
    tempx = []
    tempy = []
    player_list.empty()
    bullet_list.empty()
    enemies1.empty()
    enemies2.empty()
    enemies3.empty()
    enemiesbullets1.empty()
    enemiesbullets2.empty()
    enemiesbullets3.empty()
    p1shot = []
    mtime = []
    movex = []
    movey = []
    did = []
    didtime = []
    fpstime = time.time()
    fps = 0

    for genome_id, genome in genomes:
        # print(genome_id)

        genome.fitness = 50  # start with fitness level of 50
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        player_list.add(Player(850, 345))
        bullet_list.add(bullet(world))
        enemies1.add(enemy(world, -500))
        enemies2.add(enemy(world, -500))
        enemies3.add(enemy(world, -500))
        enemiesbullets1.add(enemybullet(enemycount))
        enemiesbullets2.add(enemybullet(enemycount))
        enemiesbullets3.add(enemybullet(enemycount))
        ge.append(genome)
        l = int(1)
        level.append(l)
        a = int(0)
        enemycount.append(a)
        edead.append(a)
        p = int(1)
        playeralive.append(p)
        en1.append(a)
        en2.append(a)
        en3.append(a)
        tempx.append(850)
        tempy.append(250)
        p1shot.append(time.time() - 4.5)
        mtime.append(time.time())
        movex.append(0)
        movey.append(0)
        did.append(False)
        didtime.append(time.time())

        # e = pygame.sprite.Group()
        # enemies.append(e)
        # enemiesbullets.append(e)

    alive = 5
    while alive > 0:
        d = False

        if e == True:
            for id, player in enumerate(player_list.sprites()):
                # for x in enemiesbullets[id].sprites():

                if playeralive[id] == 1:
                    if enemiesbullets1.sprites()[id].rect.colliderect(player.rect) and en1[id] == 1:
                        ge[id].fitness -= 2000
                        player.die()
                        print("en1 bullet", id, "gen", gen,"level",level[id])
                        playeralive[id] = 0
                        # playerkill(id, ge, nets, player, level, enemycount, edead, en1, en2, en3)  # killing player function
                        '''
                        ge[id].fitness -= 1
                        nets.pop(id)
                        ge.pop(id)
                        player.kill()
                        playerdead = True

                        '''

                    if enemiesbullets2.sprites()[id].rect.colliderect(player.rect) and en2[id] == 1:
                        player.die()
                        print("en2 bullet", id, "gen", gen,"level",level[id])
                        playeralive[id] = 0
                        ge[id].fitness -= 2000

                        # playerkill(id, ge, nets, player, level, enemycount, edead, en1, en2, en3)  # killing player function

                    if level == 2:
                        if enemiesbullets3.sprites()[id].rect.colliderect(player.rect) and en3[id] == 1:
                            player.die()
                            print("en3 bullet", id, "gen", gen,"level",level[id])
                            playeralive[id] = 0
                            ge[id].fitness -= 2000
                    if bullet_list.sprites()[id].rect.colliderect(enemies1.sprites()[id].rect) and en1[id] == 1:
                        # print(id)

                        # x.control(-10000, 0)
                        enemies1.sprites()[id].die()
                        en1[id] = 0
                        didtime[id] = time.time()

                        '''
                        enemies1.sprites()[id].kill()
                        enemiesbullets1.sprites()[id].kill()
                        '''
                        ge[id].fitness += 50000
                        edead[id] += 1

                        print("en1 dead", id, edead[id], "gen", gen,"level",level[id])

                    if bullet_list.sprites()[id].rect.colliderect(enemies2.sprites()[id].rect) and en2[id] == 1:
                        enemies2.sprites()[id].die()
                        en2[id] = 0
                        ge[id].fitness += 50000
                        edead[id] += 1
                        didtime[id] = time.time()

                        print("en2 dead", id, edead[id], "gen", gen,"level",level[id])
                    if level[id] == 2:

                        if bullet_list.sprites()[id].rect.colliderect(enemies3.sprites()[id].rect) and en3[id] == 1:
                            enemies3.sprites()[id].die()
                            en3[id] = 0
                            ge[id].fitness += 100000
                            edead[id] += 1
                            didtime[id] = time.time()
                            print("en3 dead", id, edead[id], "gen", gen,"level",level[id])

                    if player.rect.colliderect(boundry.rect) or player.rect.colliderect(
                            topb.rect) or player.rect.colliderect(bottomb.rect) or player.rect.colliderect(
                        behindb.rect):
                        player.die()
                        print("boundry id", id,"edead", edead[id], "gen", gen,"level",level[id])
                        playeralive[id] = 0
                        ge[id].fitness -= 20000
                        if level[id] == 2:
                            ge[id].fitness -= 200000

                        # playerkill(id, ge, nets, player, level, enemycount, edead, en1, en2, en3)
        if main:
            for id, player in enumerate(player_list.sprites()):

                e = True
                '''
                player.rect.x = 850  # go to x
                player.rect.y = 250  # go to y
                '''
                if edead[id] == 3:
                    player.die()
                    playeralive[id] = 0
                    ge[id].fitness += 5000000
                elif edead[id] == 2 and level[id] == 1:
                    ge[id].fitness += 200000

                if edead[id] == 2 and enemycount[id] != 3:
                    level[id] = int(2)
                    enemycount[id] = int(0)
                # print(level)
                if level[id] == 1 and enemycount[id] != 2:
                    # y = 100 + 400*enemycount
                    enemycount[id] = 2
                    enemies1.sprites()[id].spawn(100)
                    enemies2.sprites()[id].spawn(500)
                    en1[id] = 1
                    en2[id] = 1
                if level[id] == 2 and enemycount[id] != 3:
                    edead[id] = 0
                    e = True
                    player.rect.x = 850  # go to x
                    player.rect.y = 250  # go to y
                    bullet_list.sprites()[id].rect.x = 10000
                    bullet_list.sprites()[id].rect.y = 10
                    # y = 100 + 200 * enemycount
                    enemycount[id] = int(3)
                    enemies1.sprites()[id].spawn(100)
                    enemies3.sprites()[id].spawn(300)
                    enemies2.sprites()[id].spawn(500)
                    en1[id] = 1
                    en2[id] = 1
                    en3[id] = 1
        if e == True and time.time() - eshot >= 4:
            for id, player in enumerate(player_list.sprites()):
                # print(time.time()-eshot)
                if playeralive[id] == 1:
                    if en1[id] == 1:
                        enemiesbullets1.sprites()[id].control(enemies1.sprites()[id].rect.x,
                                                              enemies1.sprites()[id].rect.y)
                        # print("b1", enemies1.sprites()[id].rect.x, enemies1.sprites()[id].rect.y)
                    if en2[id] == 1:
                        enemiesbullets2.sprites()[id].control(enemies2.sprites()[id].rect.x,
                                                              enemies2.sprites()[id].rect.y)
                    if level[id] == 2:
                        if en3[id] == 1:
                            enemiesbullets3.sprites()[id].control(enemies3.sprites()[id].rect.x,
                                                                  enemies3.sprites()[id].rect.y)
                    eshot = time.time()
        for event in pygame.event.get():
            player = player_list.sprites()[1]
            if event.type == pygame.QUIT:
                pygame.quit()

                #neat.Checkpointer.save_checkpoint
                try:
                    sys.exit()
                finally:
                    main = False


            '''
            if event.type == pygame.KEYDOWN:

                if event.key == ord('q'):
                    pygame.quit()
                    try:
                        sys.exit()
                    finally:
                        main = False
                if main:

                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        k = event.key
                        player.control(-steps, 0)
                        colid = False

                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        k = event.key
                        colid = False
                        player.control(steps, 0)

                    if event.key == pygame.K_UP or event.key == ord('w'):
                        w = event.key
                        player.control(0,-steps)

                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        w = event.key
                        player.control(0, steps)

                    if event.key == ord("b") and (time.time()-p1shot[1])>=5:
                        b = True
                        bullet_list.sprites()[1].control(player.rect.x, player.rect.y)
                        p1shot[1] =time.time()


            if event.type == pygame.KEYUP :
                if (event.key == pygame.K_LEFT or event.key == ord('a')):
                        #print("colid")
                        player.control(steps, 0)
                if (event.key == pygame.K_RIGHT or event.key == ord('d')):
                        player.control(-steps, 0)
                if event.key == pygame.K_UP or event.key == ord('w')  :
                        player.control(0, steps)
                if event.key == pygame.K_DOWN or event.key == ord('s') :
                        player.control(0, -steps)
            '''

        for id, player in enumerate(player_list.sprites()):
            strafea = 2
            strafeb = 5
            bullf = 2

            if playeralive[id] == 1:
                # print("alive")
                output = nets[id].activate((player.rect.x, player.rect.y, enemies1.sprites()[id].rect.x,
                                            enemies1.sprites()[id].rect.y, enemies2.sprites()[id].rect.x,
                                            enemies2.sprites()[id].rect.y, enemies3.sprites()[id].rect.x,
                                            enemies3.sprites()[id].rect.y, bullet_list.sprites()[id].rect.x,
                                            bullet_list.sprites()[id].rect.y, en1[id], en2[id], en3[id],
                                            enemiesbullets1.sprites()[id].rect.x, enemiesbullets1.sprites()[id].rect.y,
                                            enemiesbullets2.sprites()[id].rect.x, enemiesbullets2.sprites()[id].rect.y,
                                            enemiesbullets3.sprites()[id].rect.x, enemiesbullets3.sprites()[id].rect.y,
                                            level[id], (time.time() - p1shot[id])))
                ge[id].fitness += 0.5
                if (time.time() - didtime[id]) > 30:
                    player.die()
                    playeralive[id] = 0
                    ge[id].fitness -= 50000
                if output[0] < 0.5 and output[1] < 0.5 and output[2] < 0.5 and output[3] < 0.5:
                    ge[id].fitness += 0.5

                if output[0] >= 0.5:
                    # moving up
                    player.update(0, steps)
                    ge[id].fitness += strafea
                    if movey[id] == 2:
                        ge[id].fitness += strafeb
                    movey[id] = 1
                elif output[1] >= 0.5:
                    # moving down

                    ge[id].fitness += strafea
                    player.update(0, -steps)
                    if movey[id] == 1:
                        ge[id].fitness += strafeb
                    movey[id] = 1
                if output[2] >= 0.5:
                    # moving right
                    ge[id].fitness += strafea
                    player.update(steps, 0)
                    if movex[id] == 2:
                        ge[id].fitness += strafeb
                    movex[id] = 1
                elif output[3] >= 0.5:
                    # moving left
                    ge[id].fitness += strafea
                    player.update(-steps, 0)
                    if movex[id] == 1:
                        ge[id].fitness += strafeb
                    movex[id] = 2
                if output[4] >= 0.75:
                    if level[id] == 1:
                        a = 200
                        b = 0
                        if (time.time() - p1shot[id]) >= 5:
                            a = 20000
                            b = 200
                        if (player.rect.y) > 100 and (player.rect.y + 15) < 220 and en1[id] == 1:
                            ge[id].fitness += a
                        elif (player.rect.y) > 500 and (player.rect.y + 15) < 620 and en2[id] == 1:
                            ge[id].fitness += a + b
                    elif level[id] == 2:
                        if (player.rect.y) > 100 and (player.rect.y + 15) < 220 and en1[id] == 1:
                            ge[id].fitness += a
                        elif (player.rect.y) > 500 and (player.rect.y + 15) < 620 and en2[id] == 1:
                            ge[id].fitness += a
                        elif (player.rect.y) > 300 and (player.rect.y + 15) < 420 and en3[id] == 1:
                            ge[id].fitness += a

                    if (time.time() - p1shot[id]) >= 5:
                        bullet_list.sprites()[id].control(player.rect.x, player.rect.y)
                        ge[id].fitness += -10
                        p1shot[id] = time.time()
                    else:
                        ge[id].fitness += -20
                tx = tempx[id] - player.rect.x
                ty = tempy[id] - player.rect.y
                displacement = math.sqrt((tx ** 2) + (ty ** 2))
                # print(displacement)
                if displacement <= 100 and (time.time() - mtime[id]) >= 15:
                    print("stationary death", id)
                    player.die()
                    playeralive[id] = 0
                    ge[id].fitness -= 50000
                elif displacement >= 20:
                    mtime[id] = time.time()
                    tempx[id] = player.rect.x
                    tempy[id] = player.rect.y

        world.blit(backdrop, backdropbox)
        if time.time() - start < 1.5 and level == 1:
            world.blit(level1, (385, 200))
        elif time.time() - start < 1.5 and level == 2:
            world.blit(level2, (400, 200))
        if level == 1:
            world.blit(level1s, (470, 0))
        elif level == 2:
            world.blit(level2s, (470, 0))

        # world.blit(circle , (50,50))
        # player_list.update(0,0)
        # player2.update()
        player_list.draw(world)
        enemies1.draw(world)
        enemies2.draw(world)
        enemies3.draw(world)
        # print(player_list)
        '''
        if playerdead == True:
            world.blit(blk,(0,0))
            world.blit(over,(300,250))
        if ed == True:
            world.blit(blk, (0, 0))
            world.blit(end, (250, 150))
            playerdead = True
        '''

        enemiesbullets1.update()
        enemiesbullets1.draw(world)
        enemiesbullets2.update()
        enemiesbullets2.draw(world)
        enemiesbullets3.update()
        enemiesbullets3.draw(world)

        bullet_list.update()
        bullet_list.draw(world)
        # b_list.draw(world)

        pygame.display.flip()
        clock.tick(60)
        # print(alive)
        alive = 0
        for id, player in enumerate(player_list.sprites()):
            # alive = 0
            if playeralive[id] == 1:
                alive += 1
                # ge[id].fitness += 0.2


def run(config_file):
    global gen
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(200, 1000))
    # Run for up to 50 generations.

    winner = p.run(eval_genomes, 5000000)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))
    stats.save()

def resume(config_path):
    global gen
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-1785')
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(200, 1000))
    gen = p.generation

    # Run for up to 50 generations.

    winner = p.run(eval_genomes, 5000000)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))
    stats.save()

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    resume(config_path)
    #run(config_path)
