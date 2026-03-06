from pylumina import Simulation, render
from pylumina.physics import Wind, Drag

def main():
    sim = Simulation()
    # Strong headwind
    sim.add_force(Wind(direction=(-1, 0, 0), strength=10.0))
    sim.add_force(Drag(cd=0.5, area=0.1))
    
    p = sim.add_particle("Glider", (0, 0, 0), 0.5)
    p.velocity.x = 20.0 # Launch forward
    
    print("Starting Wind Simulation...")
    for _ in range(15):
        sim.step(0.1)
        render(sim)

if __name__ == "__main__":
    main()
