from enum import Enum
import random
import logging
from src.utils.constants import MINING_TIME_RANGE, TRAVEL_TIME, UNLOAD_TIME

logger = logging.getLogger(__name__)

class TruckState(Enum):
    """
    Class representing the possible states of a mining truck in the simulation.
    """
    MINING = "mining" # Default state
    TRAVELING_TO_STATION = "traveling_to_station"
    TRAVELING_TO_SITE = "traveling_to_site"
    UNLOADING = "unloading"
    WAITING = "waiting"


class MiningTruck:
    """
    Represents a mining truck in the lunar mining simulation.

    Attributes:
        id (int): Unique identifier for the truck.
        mining_time (int): tracks timestamp for the truck to mine resources.
        travel_time (int): tracks timestamp for travel between sites and stations.
        unload_time (int): tracks timestamp to unload resources at a station.
        time_in_state (int): Tracks duration spent in the current state.
        current_state (TruckState): Current state of the truck.
        station : Assigned unload station.
        stats (dict): Aggregated statistics of the truck's activities.
    """
    def __init__(self, id):
        self.id = id
        self.mining_time = 0
        self.travel_time = 0
        self.unload_time = 0
        self.time_in_state = 0  # Time spent in the current state
        self.current_state = TruckState.MINING
        self.station = None  # track assigned station

        self.stats = {
            'total_mining_time': 0,
            'total_travel_time': 0,
            'total_unload_time': 0,
            'total_wait_time': 0,
            'unloads_completed': 0
        }

    def get_assigned_station(self):
        """Return the station that the truck is assigned to."""
        return self.station

    def mine(self):
        """Simulate mining operation."""
        if self.current_state is TruckState.MINING:
            if self.time_in_state == 0:
                self.mining_time = random.randint(*MINING_TIME_RANGE) # Unpack tuple
                logger.debug(f"<Truck {self.id}> started mining for {self.mining_time} minutes.")
            self.time_in_state += 1
            if self.time_in_state >= self.mining_time:
                self.stats['total_mining_time'] += self.mining_time
                self.current_state = TruckState.TRAVELING_TO_STATION
                self.time_in_state = 0
                logger.debug(f"<Truck {self.id}> finished mining. Total mining time: {self.stats['total_mining_time']} minutes. Transitioning to traveling_to_station.")

    def travel(self):
        """Simulate travel to unload station and back to mining site."""
        if self.current_state is TruckState.TRAVELING_TO_STATION:
            if self.time_in_state == 0:
                self.travel_time = TRAVEL_TIME
                logger.debug(f"<Truck {self.id}> started traveling to station. Travel time: {self.travel_time} minutes.")
            self.time_in_state += 1
            if self.time_in_state >= self.travel_time:
                self.stats['total_travel_time'] += self.travel_time
                self.current_state = TruckState.UNLOADING
                self.time_in_state = 0
                logger.debug(f"<Truck {self.id}> arrived at station. Total travel time: {self.stats['total_travel_time']} minutes. Transitioning to unloading.")

        elif self.current_state is TruckState.TRAVELING_TO_SITE:
            if self.time_in_state == 0:
                self.travel_time = TRAVEL_TIME
                logger.debug(f"<Truck {self.id}> started traveling to mining site. Travel time: {self.travel_time} minutes.")
            self.time_in_state += 1
            if self.time_in_state >= self.travel_time:
                self.stats['total_travel_time'] += self.travel_time
                self.current_state = TruckState.MINING
                self.time_in_state = 0
                logger.debug(f"<Truck {self.id}> arrived at mining site. Total travel time: {self.stats['total_travel_time']} minutes. Transitioning to mining.")

    def unload(self):
        """Simulate unloading operation."""
        if self.current_state is TruckState.UNLOADING:
            if self.time_in_state == 0:
                self.unload_time = UNLOAD_TIME
                logger.debug(f"<Truck {self.id}> started unloading. Unload time: {self.unload_time} minutes.")
            self.time_in_state += 1
            if self.time_in_state >= self.unload_time:
                self.stats['total_unload_time'] += self.unload_time
                self.stats['unloads_completed'] += 1
                self.current_state = TruckState.TRAVELING_TO_SITE
                self.time_in_state = 0

                station = self.get_assigned_station()  # Get the assigned station
                if station:
                    # Increment total trucks processed after unloading is completed
                    station.stats['total_trucks_processed'] += 1
                    logger.debug(f"<Truck {self.id}> finished unloading. <Station {station.id}> total trucks processed: {station.stats['total_trucks_processed']}. Transitioning to {self.current_state}.")

    def wait(self):
        """Simulate waiting time."""
        if self.current_state is TruckState.WAITING:
            self.stats['total_wait_time'] += 1
            logger.debug(f"<Truck {self.id}> is waiting. Total wait time: {self.stats['total_wait_time']} minutes.")