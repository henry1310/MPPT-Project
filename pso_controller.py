# pso_controller.py
import random

class Particle:
    def __init__(self, min_volt, max_volt):
        self.voltage = random.uniform(min_volt, max_volt)
        self.velocity = 0.0
        self.best_voltage = self.voltage
        self.best_power = 0.0

    def update_velocity(self, global_best_voltage):
        # Constants for how much the particle relies on itself vs the swarm
        inertia = 0.5
        cognitive = 1.5 # Pull toward personal best
        social = 1.5    # Pull toward global best
        
        r1, r2 = random.random(), random.random()
        
        cognitive_pull = cognitive * r1 * (self.best_voltage - self.voltage)
        social_pull = social * r2 * (global_best_voltage - self.voltage)
        
        self.velocity = (inertia * self.velocity) + cognitive_pull + social_pull

    def update_position(self, min_volt, max_volt):
        self.voltage += self.velocity
        # Keep the particle within safe voltage limits
        self.voltage = max(min_volt, min(self.voltage, max_volt))

class PSO_Controller:
    def __init__(self, num_particles, min_volt, max_volt):
        self.swarm = [Particle(min_volt, max_volt) for _ in range(num_particles)]
        self.global_best_voltage = 0.0
        self.global_best_power = 0.0
        self.min_volt = min_volt
        self.max_volt = max_volt

    def evaluate_and_move(self, virtual_panel):
        # 1. Evaluate current positions
        for particle in self.swarm:
            power = virtual_panel.get_power(particle.voltage)
            
            # Update personal best
            if power > particle.best_power:
                particle.best_power = power
                particle.best_voltage = particle.voltage
                
            # Update global best
            if power > self.global_best_power:
                self.global_best_power = power
                self.global_best_voltage = particle.voltage

        # 2. Move swarm for the next iteration
        for particle in self.swarm:
            particle.update_velocity(self.global_best_voltage)
            particle.update_position(self.min_volt, self.max_volt)