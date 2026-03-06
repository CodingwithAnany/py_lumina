from pylumina import Simulation, render
from pylumina.physics import Gravity

def main():
    sim = Simulation()
    sim.add_force(Gravity())
    
    p = sim.add_particle("Ball", (0, 10, 0), 1.0)
    
    print("Starting Particle Demo...")
    for _ in range(10):
        sim.step(0.1)
        render(sim)

if __name__ == "__main__":
    main()
