import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

import time

def cmt():
    return round(time.time() * 1000)





class config:
	#BASIC SETTINGS
	fullscreen = True
	reso_x = 1280
	reso_y = 720
	ps = 3	          #player speed
	sens = .5          #sensitivity of turning when using arrows
	d_sens = sens - sens *2
	
	#OPTIMIZATION SETTINGS
	rd = 64	          #roundness of the shperes, applied to both latitude and longitude
	tl = 1	          #time lock, miliseconds
	opt_dist = 50     #if the star is this far a away, the quality will be devided by opt_mult
	opt_mult = 4      #if the star is opt_dist far away, the quality will be devided by this
	
	#STAR SETTINGS
	sd = 500   #sphere max distance
	sm = -500  #sphere min distance
	sc = 250   #sphere count
	mm = .05   #maximal movement
	lm = -.05  #minimal movement
	bs = 8	   #highest sphere size
	ss = .5	   #lowest sphere size

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


pos_x = 0
pos_y = 0
pos_z = 0
rot_x = 0
rot_y = 0
rot_z = 0


for i in range(config.sc):
	#random.seed(cmt())
	lsx.append(random.randint(config.sm, config.sd))
	lsy.append(random.randint(config.sm, config.sd))
	lsz.append(random.randint(config.sm, config.sd))
	lsr.append(random.uniform(config.bs, config.ss))
	los.append(gluNewQuadric())
	stx.append(random.uniform(config.lm, config.mm))
	sty.append(random.uniform(config.lm, config.mm))
	stz.append(random.uniform(config.lm, config.mm))

pygame.init()
display = (config.reso_x, config.reso_y)
scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.toggle_fullscreen()


glEnable(GL_DEPTH_TEST)

sphere = gluNewQuadric() #Create new sphere

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 5000) #THE LAST ARGUMENT HERE IS THE DRAWING DISTANCE

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
		pos_z+=config.ps
		glTranslatef(0,0,config.ps)
	if keypress[pygame.K_s]:
		pos_z+=config.ps - config.ps * 2
		glTranslatef(0,0,config.ps - config.ps * 2)
	if keypress[pygame.K_d]:
		pos_x+=config.ps - config.ps * 2
		glTranslatef(config.ps - config.ps * 2,0,0)
	if keypress[pygame.K_a]:
		pos_x+=config.ps
		glTranslatef(config.ps,0,0)
	if keypress[pygame.K_UP]:
		glRotatef(config.d_sens, config.sens, 0, 0)
	if keypress[pygame.K_DOWN]:
		glRotatef(config.sens, config.sens, 0, 0)
	if keypress[pygame.K_LEFT]:
		glRotatef(config.d_sens, 0, config.sens, 0)
	if keypress[pygame.K_RIGHT]:
		glRotatef(config.sens, 0, config.sens, 0)
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
		polc = config.rd
		
		#OPTIMIZATION BY DISTANCE
		#if the sphere is more than 50 away, the program will reduce its render quality by 4
		#simple yet it made it like 5 times faster
		if config.opt_dist < abs(pos_x-lsx[n]) or config.opt_dist < abs(pos_z-lsz[n]):
			polc = int(polc/config.opt_mult)
		glColor4f(1, 1, 1, 1) 
		gluSphere(los[i], lsr[i], polc, polc)
		glPopMatrix()


	pygame.display.flip() #Update the screen
	pygame.time.wait(config.tl)  #Wait, propably useless

pygame.quit()
