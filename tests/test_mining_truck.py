import pytest
from src.models.truck import TruckState, MiningTruck
from src.models.station import UnloadStation

@pytest.fixture
def truck():
    return MiningTruck(id=1)

def test_truck_initial_state(truck):
    assert truck.id == 1
    assert truck.current_state == TruckState.MINING
    assert truck.stats["total_mining_time"] == 0
    assert truck.stats["unloads_completed"] == 0

def test_mining_progress(truck):
    truck.mine()
    assert truck.current_state in [TruckState.MINING, TruckState.TRAVELING_TO_STATION]

def test_truck_unloading():
    truck = MiningTruck(id=2)
    station = UnloadStation(id=1)
    truck.station = station

    truck.current_state = TruckState.UNLOADING
    for _ in range(5):  # Simulate unloading time
        truck.unload()

    assert truck.current_state == TruckState.TRAVELING_TO_SITE
    assert truck.stats["total_unload_time"] == 5
    assert truck.stats["unloads_completed"] == 1

def test_truck_waiting(truck):
    truck.current_state = TruckState.WAITING
    for _ in range(10):
        truck.wait()

    assert truck.stats["total_wait_time"] == 10