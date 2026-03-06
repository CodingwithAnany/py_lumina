def render(sim=None):
    if sim is None:
        from .environment import env
        sim = env.sim
    
    print(f"\n--- Simulation State (Time: {sim.time:.2f}s) ---")
    for e in sim.entities:
        print(f"Entity: {e.name} | Pos: ({e.position.x:.2f}, {e.position.y:.2f}, {e.position.z:.2f}) | Vel: ({e.velocity.x:.2f}, {e.velocity.y:.2f}, {e.velocity.z:.2f})")
    print("-------------------------------------------\n")
