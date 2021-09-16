import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random

import math

class config:
	rd = 64    #roundness of the shperes, applied to both latitude and longitude
	tl = 1     #time lock, miliseconds
	sd = 200   #sphere max distance
	sm = -200  #sphere min distance
	sc = 200   #sphere count
	mm = .05   #maximal movement
	lm = -.05  #minimal movement
	bs = 4     #highest sphere size
	ss = .5    #lowest sphere size
	ps = 3     #player speed

sx = 0
sy = 0
sz = 0

los = []#List of spheres
lsx = []#Sphere X
lsy = []#Sphere Y
lsz = []#Sphere Z
lsr = []#Sphere Size
stx = []#Sphere X Position change per tick
sty = []#Sphere Y Position change per tick
stz = []#Sphere Z Position change per tick

for i in range(config.sc):
	lsx.append(random.randint(config.sm, config.sd))
	lsy.append(random.randint(config.sm, config.sd))
	lsz.append(random.randint(config.sm, config.sd))
	lsr.append(random.uniform(config.bs, config.ss))
	los.append(gluNewQuadric())
	stx.append(random.uniform(config.lm, config.mm))
	sty.append(random.uniform(config.lm, config.mm))
	stz.append(random.uniform(config.lm, config.mm))

pygame.init()
display = (1200, 900)
scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glEnable(GL_DEPTH_TEST)

sphere = gluNewQuadric() #Create new sphere

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 500)

glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False  

    keypress = pygame.key.get_pressed()

    # init model view matrix
    glLoadIdentity()

    # init the view matrix
    glPushMatrix()
    glLoadIdentity()

    # apply the movement 
    if keypress[pygame.K_w]:
        glTranslatef(0,0,config.ps)
    if keypress[pygame.K_s]:
        glTranslatef(0,0,config.ps - config.ps * 2)
    if keypress[pygame.K_d]:
        glTranslatef(config.ps - config.ps * 2,0,0)
    if keypress[pygame.K_a]:
        glTranslatef(config.ps,0,0)
    if keypress[pygame.K_UP]:
	    glRotatef(-1, 1, 0, 0)
    if keypress[pygame.K_DOWN]:
	    glRotatef(1, 1, 0, 0)
    if keypress[pygame.K_LEFT]:
	    glRotatef(-1, 0, 1, 0)
    if keypress[pygame.K_RIGHT]:
	    glRotatef(1, 0, 1, 0)
    # multiply the current matrix by the get the new view matrix and store the final via matrix 
    glMultMatrixf(viewMatrix)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    # apply view matrix
    glPopMatrix()
    glMultMatrixf(viewMatrix)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #Clear the screen

    glPushMatrix()

    sx = sx + .01
    glTranslatef(sx, sy, sz) #Move to the place
    glColor4f(1, 1, 1, 1) #Put color
    gluSphere(sphere, 1.0, config.rd, config.rd) #Draw sphere
    glPopMatrix()
    
    for n, sp in enumerate(los):
        glPushMatrix()
        lsx[n] = lsx[n] + stx[n]
        lsy[n] = lsy[n] + sty[n]
        lsz[n] = lsz[n] + stz[n]
        glTranslatef(lsx[n], lsy[n], lsz[n])
        glColor4f(1, 1, 1, 1) 
        gluSphere(los[i], lsr[i], config.rd, config.rd)
        glPopMatrix()


    pygame.display.flip() #Update the screen
    pygame.time.wait(config.tl)  #Wait, propably useless

pygame.quit()
