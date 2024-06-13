import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Particle:
    def __init__(self, x, y, vx, vy, mass=1.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass


def initialize_particles(num_particles, temperature):
    particles = []
    for _ in range(num_particles):
        x = np.random.uniform(0, 800)
        y = np.random.uniform(0, 600)
        vx = np.random.normal(0, np.sqrt(temperature ))
        vy = np.random.normal(0, np.sqrt(temperature ))
        # we wzorze przyjęte jest, ze masa jest stała Boltzmanna jest w przybliżeniu równa 1, a masa jest identyczna
        particles.append(Particle(x, y, vx, vy))
    return particles


def update_simulation(frame, particles, dt, container_width, container_height):
    for particle in particles:
        # Aktualizacja pozycji cząsteczki
        particle.x += particle.vx * dt
        particle.y += particle.vy * dt

        # Obsługa zderzeń z ściankami pojemnika
        if particle.x < 0 or particle.x > container_width:
            particle.vx *= -1  # Odbicie od poziomej ściany
        if particle.y < 0 or particle.y > container_height:
            particle.vy *= -1  # Odbicie od pionowej ściany

    # Obsługa zderzeń między cząsteczkami
    for i, particle in enumerate(particles):
        for j in range(i + 1, len(particles)):
            other_particle = particles[j]
            dx = other_particle.x - particle.x
            dy = other_particle.y - particle.y
            distance = np.sqrt(dx ** 2 + dy ** 2)
            if distance < 10:  # Odległość, przy której następuje zderzenie
                # Obliczanie normalnej i stycznej
                normal_x = dx / distance
                normal_y = dy / distance
                tangent_x = -normal_y
                tangent_y = normal_x

                # Składowe prędkości wzdłuż normalnej
                v1n = particle.vx * normal_x + particle.vy * normal_y
                v2n = other_particle.vx * normal_x + other_particle.vy * normal_y

                # Składowe prędkości wzdłuż stycznej
                v1t = particle.vx * tangent_x + particle.vy * tangent_y
                v2t = other_particle.vx * tangent_x + other_particle.vy * tangent_y

                # Aktualizacja składowych prędkości wzdłuż normalnej
                particle.vx = v2n * normal_x + v1t * tangent_x
                particle.vy = v2n * normal_y + v1t * tangent_y
                other_particle.vx = v1n * normal_x + v2t * tangent_x
                other_particle.vy = v1n * normal_y + v2t * tangent_y

    # Aktualizacja wykresu
    scatter.set_offsets([(particle.x, particle.y) for particle in particles])
    scatter.set_sizes([particle.mass * 20 for particle in particles])
    return scatter,


# Główne parametry symulacji
num_particles = 100
initial_temperature = 1000
simulation_time = 100
dt = 0.1

# Inicjalizacja
particles = initialize_particles(num_particles, initial_temperature)

# Tworzenie wykresu
fig, ax = plt.subplots()
ax.set_xlim(0, 800)
ax.set_ylim(0, 600)
ax.set_xlabel('Pozycja X')
ax.set_ylabel('Pozycja Y')
ax.set_title('Symulacja cząsteczek')
ax.grid(True)

# Aktualizacja scatter plot z kolorami i rozmiarami
scatter = ax.scatter([], [], c='red', s=20, edgecolors='black')

# Animacja
animation = FuncAnimation(fig, update_simulation, frames=simulation_time,
                          fargs=(particles, dt, 800, 600), interval=50)

plt.show()

# Obliczanie energii kinetycznych
kinetic_energies = [0.5 *  particle.mass * (particle.vx * 2 + particle.vy * 2) for particle in particles]

# Wykres histogramu
plt.figure(figsize=(10, 6))
plt.hist(kinetic_energies, bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Energia kinetyczna')
plt.ylabel('Częstotliwość')
plt.title('Histogram energii kinetycznej')
plt.grid(True, linestyle='--', linewidth=0.5)
plt.show()