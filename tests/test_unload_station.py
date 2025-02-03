import pytest
from src.models.station import UnloadStation

@pytest.fixture
def station():
    return UnloadStation(id=1)

def test_station_initial_state(station):
    assert station.id == 1
    assert station.available_time == 0
    assert len(station.queue) == 0

def test_station_queue(station):
    station.add_to_queue(1)
    station.add_to_queue(2)

    assert len(station.queue) == 2
    assert station.stats["max_queue_length"] == 2
