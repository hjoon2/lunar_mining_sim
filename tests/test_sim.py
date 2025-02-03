import pytest
from src.simulation import MiningSimulation

@pytest.fixture
def simulation():
    return MiningSimulation(num_trucks=5, num_stations=2)

def test_simulation_setup(simulation):
    assert len(simulation.trucks) == 5
    assert len(simulation.stations) == 2

def test_simulation_run(simulation):
    simulation.run_simulation()
    assert all(truck.stats["unloads_completed"] > 0 for truck in simulation.trucks)
