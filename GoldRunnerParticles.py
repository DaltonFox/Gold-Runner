import pygame, pygame.gfxdraw, math, random, time  # imports the stuff we need to run this program


class GenericParticle(object):
    """
    ~ Parent Class
    This is our Generic Particle class which handles the basics of what a particle does and how it appears depending on its parameters.
    Our particle object is used to make many copies of the 'same' particle to be created by our particle system object.
    """
    def __init__(self, init_x, init_y, init_direction, init_speed, init_lifespan, init_size, init_color, init_alpha=255, init_type=0):
        # this is our constructor, it requires the following input to handle a particle successfully
        self.x = init_x
        self.y = init_y
        self.direction = init_direction
        self.speed = init_speed
        self.lifespan = init_lifespan
        self.size = init_size
        self.color = init_color
        self.alpha = init_alpha  # optional parameter
        self.type = init_type  # optional parameter

        self.birthdate = time.time()  # get the time the particle was created
        self.life_percentage = 0
        self.opacity = self.alpha

    def update(self):  # this updates the location and handles the 'movement' of the particle
        dx = self.speed*math.cos(math.radians(self.direction))
        dy = -1*self.speed*math.sin(math.radians(self.direction))
        self.x += dx
        self.y += dy * 0.05

        self.life_percentage = abs(time.time() - self.birthdate) / self.lifespan  # get the percentage of life left in a particle

    def update_effects(self):  # this updates other things a particle might want to do, for instance alpha (opacity)
        pass

    def render(self):  # this draws our particle according to its parameters
        pass


class Particle(GenericParticle):
    """
    ~ Child Class
    The Particle is a particle that chooses between two types and moves in a direction, eventually fading out and coming to a stop.
    """
    def update_effects(self):
        if self.life_percentage < 1 and self.life_percentage >= 0.60:  # as long as we haven't reached 100% lifespan start to fade at 65%
            self.opacity = 255 - abs(255 * self.life_percentage)
        if self.life_percentage < 1 and self.life_percentage >= 0.05:
            if self.speed > 0:
                    self.speed -= 0.5
            if self.speed <= 0:
                    self.speed = 0

    def render(self, surface):  # depending on the type chosen we create a particle based on it
        if self.type == 1:
            pygame.gfxdraw.circle(surface, int(self.x), int(self.y), int(self.size), (self.color + (self.opacity, )))
        if self.type == 2:
            pygame.gfxdraw.filled_circle(surface, int(self.x), int(self.y), int(self.size), (self.color + (self.opacity, )))


class GenericParticleSystem(object):
    """
    ~ Parent Class
    This is our Generic Particle System class which handles the creation of multiple particles.
    """
    def __init__(self):  # particle system constructor initializes the list we will store particles in
        self.particle_list = []

    def emit_particle(self, x, y, part_direction, part_speed, part_lifespan, part_size, part_color):
        # when we ask our particle system to emit a particle (add it to the list) we request its type(class) and info(parameters)
        self.particle_list.append(GenericParticle(x, y, part_direction, part_speed, part_lifespan, part_size, part_color))

    def update_particles(self):  # update all of the particles in our list
        for particle in self.particle_list:
            particle.update()
            particle.update_effects()
            if time.time() > particle.birthdate + particle.lifespan:
                self.particle_list.remove(particle)  # remove expired particles

    def render_particles(self, surface):  # draw all the particles in our list
        for particle in self.particle_list:
            particle.render(surface)  # draws particles on the specified surface


class ParticleSystem(GenericParticleSystem):
    """
    ~ Child Class
    The Particles System creates Particles
    """
    def emit_particle(self, x, y, part_direction, part_speed, part_lifespan, part_size, part_color, part_alpha, part_type):
        self.particle_list.append(Particle(x, y, part_direction, part_speed, part_lifespan, part_size, part_color, part_alpha, part_type))
