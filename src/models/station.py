from collections import deque
import logging
from src.utils.constants import UNLOAD_TIME

logger = logging.getLogger(__name__)

class UnloadStation:
    """
    Represents unload station in the lunar mining simulation.

    Attributes:
        id (int): Unique identifier for the station.
        available_time (int): Timestamp indicating when the station will be next available for unloading.
        queue (deque): A queue (using deque) to track trucks waiting to unload.
        stats (dict): Aggregated statistics of the truck's activities.
    """
    def __init__(self, id):
        self.id = id
        self.available_time = 0  # Time when the station will be available
        self.queue = deque()  # Use deque for tracking truck wait list

        self.stats = {
            'total_trucks_processed': 0,
            'max_queue_length': 0
        }

    def is_available(self, current_time):
        """Check if the station is available at the given time."""
        return self.available_time <= current_time

    def add_to_queue(self, truck_id):
        """Add a truck to the station's queue."""
        self.queue.append(truck_id)
        self.stats['max_queue_length'] = max(self.stats['max_queue_length'], len(self.queue))

        logger.debug(f"Truck {truck_id} added to <Station {self.id}> queue. Queue length: {len(self.queue)}. Trucks in Queue: {self.queue}")
        logger.debug(f"<Station {self.id}> stats: {self.stats}")

    def process_truck(self, current_time):
        """Process the next truck in the queue."""
        if self.is_available(current_time) and self.queue:
            truck_id = self.queue.popleft()
            self.available_time = current_time + UNLOAD_TIME  # Set the time when the station will be available again
            #self.stats['total_trucks_processed'] += 1

            logger.debug(f"<Station {self.id}> processed truck {truck_id} from queue.")

            return truck_id
        return None