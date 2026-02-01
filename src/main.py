from simulation import Simulation

if __name__ == "__main__":
    try:
        sim = Simulation()
        sim.run()
    except KeyboardInterrupt as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")