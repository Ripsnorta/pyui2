


import sys, time, pygame

pygame.init()

black = 0, 0, 0

screen = pygame.display.set_mode((800, 600))
frameCounter = 0
lastTime = 0


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    frameCounter = frameCounter + 1

    now = time.time()

    if now - lastTime >= 1:
        lastTime = now
        print "FPS: %d" % frameCounter
        frameCounter = 0

    screen.fill(black)
    pygame.display.flip()