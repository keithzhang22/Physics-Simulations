import pygame
import random
import math
import os

background_colour = (255,255,255)
(width, height) = (600, 400)
mass_of_air = 0
elasticity = 1
gravity = (math.pi, 0.002)

def addVectors(vector1, vector2):
    x  = math.sin(vector1[0]) * vector1[1] + math.sin(vector2[0]) * vector2[1]
    y  = math.cos(vector1[0]) * vector1[1] + math.cos(vector2[0]) * vector2[1]

    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size: #if distance apart less than combined radius
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = addVectors((p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass), (angle, 2*p2.speed*p2.mass/total_mass))
        (p2.angle, p2.speed) = addVectors((p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass), (angle+math.pi, 2*p1.speed*p1.mass/total_mass))

        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap


class Particle():
    def __init__(self, position, size, mass=1):
        self.x = position[0]
        self.y = position[1]
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = (self.mass/(self.mass + mass_of_air)) ** self.size

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        if self.angle <= math.pi/2:
            self.x += math.sin(self.angle) * self.speed
            self.y -= math.cos(self.angle) * self.speed
        elif self.angle > math.pi/2 and self.angle <= math.pi:
            basic = math.pi - self.angle
            self.x += math.sin(basic) * self.speed
            self.y += math.cos(basic) * self.speed
        elif self.angle > math.pi and self.angle <= math.pi*1.5:
            basic = self.angle - math.pi
            self.x -= math.sin(basic) * self.speed
            self.y += math.cos(basic) * self.speed
        elif self.angle > math.pi*1.5 and self.angle < 2*math.pi:
            basic = self.angle - 1.5 * math.pi
            self.x -= math.cos(basic) * self.speed
            self.y -= math.sin(basic) * self.speed
        elif self.angle == 0 or self.angle == 2*math.pi:
            self.y += self.speed
            
        self.speed *= self.drag

    def bounce(self, up, down, left, right):
        if self.x > right - self.size:
            self.x = 2*(right - self.size) - self.x
            self.angle = - self.angle
            #self.speed *= elasticity

        elif self.x < left-self.size:
            self.x = 2*(left-self.size) - self.x
            self.angle = - self.angle
            #self.speed *= elasticity

        if self.y + self.size > down:
            d = self.y + self.size - down
            self.y = self.y - d
            self.angle = math.pi - self.angle
            #self.speed *= elasticity

        elif self.y + self.size < up:
            d = up - (self.y + self.size)
            self.y = self.y + d
            self.angle = math.pi - self.angle
            #self.speed *= elasticity

    def reset(self):
        self.speed = originalspeed

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Conduction for Non-metals')
clock = pygame.time.Clock()

my_particles = [] #all


#molecules
my_molecules = []
size = 20
density = 20
rows = 3
columns = 7
originalspeed = 0.02

boxwidth = columns*45
boxheight = 45*rows
originalposition=[]
listofangle = []

x1=200
angle1 = random.uniform(0,math.pi*2)
for column in range(columns):
    y1=180
    for row in range(rows):
        particle = Particle((x1, y1), size, density*size**2)
        particle.colour = (200-density*10, 200-density*10, 255)
        particle.speed = originalspeed
        angle1+=math.pi/2
        particle.angle = angle1
        my_particles.append(particle)
        originalposition.append((x1,y1))
        listofangle.append(particle.angle)
        #print(particle.angle)
        y1+=45
    x1+=45

button = 0
heatImg = pygame.image.load('Heat.png')
heatImg = pygame.transform.scale(heatImg, (80, boxheight+10))

xpos_heat = 50
ypos_heat = 130

selected_particle = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                button = 0
                for particle in my_particles:
                    particle.reset()
            if event.key == pygame.K_g:
                button += 1


    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(background_colour)

    for i, particle in enumerate(my_particles):
        particle.move() 
        particle.bounce(originalposition[i][1]-7, originalposition[i][1]+7, originalposition[i][0]-7, originalposition[i][0]+7)
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
        particle.display()

    if button == 2:
        for row in range(rows):
            my_particles[row].speed += 0.1
            if my_particles[row].speed > 1:
                my_particles[row].speed = 1
    if button == 3:
        for row in range(rows):
            my_particles[row].speed = 1
        for row in range(rows, 2*rows):
            my_particles[row].speed += 0.1
            if my_particles[row].speed > 1:
                my_particles[row].speed = 1
    if button == 4: 
        for row in range(2*rows):
            my_particles[row].speed = 1
        for row in range(2*rows, 3*rows):
            my_particles[row].speed += 0.1
            if my_particles[row].speed > 1:
                my_particles[row].speed = 1
    if button == 5: #column 4
        for row in range(3*rows):
            my_particles[row].speed = 1
        for row in range(3*rows, 4*rows):
            my_particles[row].speed += 0.1
            if my_particles[row].speed > 1:
                my_particles[row].speed = 1
    if button == 6:
        for row in range(4*rows):
            my_particles[row].speed = 1
        for row in range(4*rows, 5*rows):
            my_particles[row].speed += 0.1
            if my_particles[row].speed > 1:
                my_particles[row].speed = 1
    if button == 7:
        for row in range(5*rows):
            my_particles[row].speed = 1
        for row in range(5*rows, 6*rows):
            my_particles[row].speed += 0.1
            if my_particles[row].speed > 1:
                my_particles[row].speed = 1
    if button > 7:
        for row in range(6*rows):
            my_particles[row].speed = 1
        for row in range(6*rows, 7*rows):
            my_particles[row].speed += 0.1
            if my_particles[row].speed > 1:
                my_particles[row].speed = 1

    if button > 0:
        screen.blit(heatImg, (xpos_heat, ypos_heat))
        
    pygame.draw.rect(screen, (0, 100, 255), (150, 130, boxwidth+20, boxheight+20), 3)  # width = 3
    pygame.display.flip()
    clock.tick(100)

