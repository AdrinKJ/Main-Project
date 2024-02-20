import math
import sys
import pygame
import neat

#Set the size of the screen
width = 1500
height = 800

generation = 0

class autonomouscar:
    def __init__(self):
        self.initialize()
        
    def initialize(self):
        self.surface = pygame.transform.scale(pygame.image.load("redCar.png"), (95,50)) #95,50 is the pixels
        self.rotate_surface = self.surface
        self.pos = [100, 600] #initializing the position of the car
        self.distance = 0
        self.speed = 0
        self.angle = 0
        self.center = [self.pos[0] + 50, self.pos[1]+50]
        self.radars = []
        self.is_alive = True
        self.time_spent = 0

    def position(self, display):
        display.blit(self.rotate_surface, self.pos) #renders the car in the screen

    def avoid_collision(self, track):
        self.is_alive = True
        for i in self.box_corner:
            if track.get_at((int(i[0]), int(i[1]))) == (255, 255, 255, 255):
                self.is_alive = False #If the car hits the white pixel(255 is white) then the car is dead
                break
    
    def radardetections(self, degree, track):
        length = 0 #is the inital distance from the car to the obstacle(white pixels in our case)
        x = int(self.center[0] + math.cos(math.radians(360-(self.angle+degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360-(self.angle+degree))) * length)

        while not track.get_at((x, y)) == (255, 255, 255, 255) and length < 300: #it needs to satisfy 2 criteria: (1) as long as the car is on the white area (2) the distance length should be less than 300
            length += 1
            x = int(self.center[0] + math.cos(math.radians(360-(self.angle+degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360-(self.angle+degree))) * length)
        distance = int(math.sqrt(math.pow(x - self.center[0],2) + math.pow(y - self.center[1],2))) #To calculate the euclidean distance between the final x,y point and tha center postions(d = √( (x2-x1)² + (y2-y1)²) )
        self.radars.append([(x,y), distance])

    def positionupdate(self,track):
        self.speed = 15
        
        self.rotate_surface = pygame.transform.rotate(self.surface, self.angle)
        self.pos[0] += math.cos(math.radians(360-self.angle)) * self.speed #self.pos[0] always represents x axis
        self.pos[0] = max(20, min(self.pos[0], width -120))

        self.distance += self.speed
        self.time_spent += 1
        self.pos[1] += math.sin(math.radians(360-self.angle)) * self.speed 
        self.pos[1] = max(20, min(self.pos[1], height -120))

        self.center = [int(self.pos[0]) + 50, int(self.pos[1]) +50] #self.pos[1] always represents y axis
        length = 38
        self.box_corner = [
            [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.cos(math.radians(360 - (self.angle + 30))) * length], #is to update the positions of the car
            [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.cos(math.radians(360 - (self.angle + 150))) * length], #x axis deals with cos and y axis deals with sin
            [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.cos(math.radians(360 - (self.angle + 210))) * length],
            [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.cos(math.radians(360 - (self.angle + 330))) * length]
        ]

        self.avoid_collision(track)
        self.radars.clear()
        for j in range(-90, 120, 45):
            self.radardetections(j, track)
    
    def radars_data(self): #retrives data from the car
        radars = self.radars
        radarlist = list()
        radarlist = [0,0,0,0,0]#represents the 5 different sensors
        for a,b in enumerate(radars): #here a is used as the index variable and b to store each string from the list
            radarlist[a] = int(b[1]/35)#35 given here is just a random number
        return radarlist

    def add_reward(self): #used to reward the car if it stays on the track
        return self.distance/50
    
    def check_alive(self):
        return self.is_alive


def run_autonomouscar(genomes, configuration):
    pygame.init()
    display = pygame.display.set_mode((width, height))
    cartrack = pygame.image.load("carTrack.png")
    neuralnetworks = list()
    cars = list()
    for i, j in genomes:
        neuralnetwork = neat.nn.FeedForwardNetwork.create(j, configuration)
        neuralnetworks.append(neuralnetwork)
        j.fitness = 0
        cars.append(autonomouscar())
    
    while True:
        for x in pygame.event.get():
            if x.type == pygame.QUIT:#used to exit the program
                pygame.quit()
                sys.exit(0)

        for k, car in enumerate(cars):
            result = neuralnetworks[k].activate(car.radars_data())
            a = result.index(max(result))
            if a == 0:
                car.angle = car.angle + 10
            else:
                car.angle = car.angle - 10

        remaining = 0
        for m, car in enumerate(cars):
            if car.check_alive():
                remaining = remaining + 1
                car.positionupdate(cartrack)
                genomes[m][1].fitness += car.add_reward()
        if remaining == 0:
            break
        display.blit(cartrack, (0,0))
        for y in cars:
            if y.check_alive():
                y.position(display)

        pygame.display.flip() #is used to display the updated frame

def simulation():
    configurationfile = "neat_config.txt"
    configuration = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configurationfile)
    sample_population = neat.Population(configuration)
    sample_population.add_reporter(neat.StdOutReporter(True))
    statcisticaldata = neat.StatisticsReporter()
    sample_population.add_reporter(statcisticaldata)
    idealcar = sample_population.run(run_autonomouscar, 15)#8 represents the number of iterations the simulations should run
    return idealcar

if __name__ == "__main__":
    simulation()