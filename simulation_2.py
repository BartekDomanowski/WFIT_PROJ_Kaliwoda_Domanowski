import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Particle:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

def initialize_particles(num_particles, temperature):
    particles = []
    for _ in range(num_particles):
        x = np.random.uniform(0, 800)
        y = np.random.uniform(0, 600)
        vx = np.random.normal(0, np.sqrt(temperature))
        vy = np.random.normal(0, np.sqrt(temperature))
        particles.append(Particle(x, y, vx, vy))
    return particles

def update_simulation(frame, particles, dt, container_width, container_height):
    for particle in particles:
        # Update particle position
        particle.x += particle.vx * dt
        particle.y += particle.vy * dt

        # Handle collisions with container walls
        if particle.x < 0 or particle.x > container_width:
            particle.vx *= -1  # Horizontal wall bounce
        if particle.y < 0 or particle.y > container_height:
            particle.vy *= -1  # Vertical wall bounce

        # Handle collisions between particles
        for other_particle in particles:
            if other_particle != particle:
                distance = np.sqrt((particle.x - other_particle.x)**2 + (particle.y - other_particle.y)**2)
                if distance < 10:  # Distance at which collision occurs
                    # Calculate reflection vector
                    dx = other_particle.x - particle.x
                    dy = other_particle.y - particle.y
                    distance = np.sqrt(dx**2 + dy**2)
                    normal_x = dx / distance
                    normal_y = dy / distance
                    # Calculate new velocities after collision
                    dot_product = (particle.vx * normal_x + particle.vy * normal_y) * 2
                    particle.vx -= dot_product * normal_x
                    particle.vy -= dot_product * normal_y

    # Update plot
    scatter.set_offsets([(particle.x, particle.y) for particle in particles])
    return scatter,

# Main simulation parameters
num_particles = 100
initial_temperature = 1000
simulation_time = 100
dt = 0.1

# Initialization
particles = initialize_particles(num_particles, initial_temperature)
energies = []

# Create plot
fig, ax = plt.subplots()
ax.set_xlim(0, 800)
ax.set_ylim(0, 600)
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_title('Particle Simulation')
ax.grid(True)

# Update scatter plot with color and size
scatter = ax.scatter([], [], c='red', s=20, edgecolors='black')

# Animation
animation = FuncAnimation(fig, update_simulation, frames=simulation_time,
                          fargs=(particles, dt, 800, 600), interval=50)

plt.show()

# Calculate kinetic energies
kinetic_energies = [0.5 * (particle.vx**2 + particle.vy**2) for particle in particles]

# Plot histogram
plt.figure(figsize=(10, 6))
plt.hist(kinetic_energies, bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Kinetic Energy')
plt.ylabel('Frequency')
plt.title('Histogram of Kinetic Energy')
plt.grid(True, linestyle='--', linewidth=0.5)
plt.show()