import random
import logging
from src.models.truck import MiningTruck, TruckState
from src.models.station import UnloadStation
from src.utils.constants import SIMULATION_DURATION, UNLOAD_TIME

logger = logging.getLogger(__name__)

class MiningSimulation:
    def __init__(self, num_trucks: int, num_stations: int):
        """
        Initialize the simulation with the given number of trucks and stations.

        Args:
            num_trucks (int): Number of trucks.
            num_stations (int): Number of unloading stations.
        """
        if num_trucks <= 0 or num_stations <= 0:
            raise ValueError("Number of trucks and stations must be at least 1.")

        self.num_trucks = num_trucks
        self.num_stations = num_stations

        # Create a list of MiningTruck objects based on number of trucks
        self.trucks = [MiningTruck(id=i) for i in range(num_trucks)]

        # Create a list of UnloadStation objects based on the number of stations
        self.stations = [UnloadStation(id=i) for i in range(num_stations)]

        # Initialize the current simulation time to 0
        self.current_time = 0

    def run_simulation(self, duration=SIMULATION_DURATION):
        """
       Run the simulation for the specified duration (default SIMULATION_DURATION 72 hours).

       This method simulates the mining process, truck movements, unloading, and station assignments
       for each 1 minute time tick.
       """

        logger.info(f"Starting simulation for {SIMULATION_DURATION/60:.1f} hours with {len(self.trucks)} trucks and {len(self.stations)} stations")
        while self.current_time < duration:
            logger.debug(f"*********Current Simulation Time {self.current_time} minutes")

            # Update all trucks states
            for truck in self.trucks:
                if truck.current_state == TruckState.MINING:
                    truck.mine()
                elif truck.current_state == TruckState.TRAVELING_TO_STATION:
                    truck.travel()
                elif truck.current_state == TruckState.TRAVELING_TO_SITE:
                    truck.travel()
                elif truck.current_state == TruckState.UNLOADING:
                    truck.unload()
                elif truck.current_state == TruckState.WAITING:
                    truck.wait()

            # Assign trucks to stations when they arrive at the station
            for truck in self.trucks:
                if truck.current_state == TruckState.TRAVELING_TO_STATION and truck.time_in_state >= truck.travel_time:
                    self.assign_to_station(truck)

            # Process queues at all stations
            for station in self.stations:
                truck_id = station.process_truck(self.current_time)
                if truck_id:
                    self.trucks[truck_id].current_state = TruckState.UNLOADING
                    logger.debug(f"<Truck {truck_id}> started unloading at station {station.id}.")

            # Increment simulation time
            self.current_time += 1

    def assign_to_station(self, truck):
        """Assign a truck to the first available unload station or the one with the shortest queue."""
        available_stations = [station for station in self.stations if station.is_available(self.current_time)]

        if available_stations:
            # If stations are available, randomly assign truck to available station.
            station = random.choice(available_stations)
            station.available_time = self.current_time + UNLOAD_TIME  # Update station's next available time
            truck.station = station  # Set the assigned station to the truck

            logger.debug(f"<Truck {truck.id}> assigned to <station {station.id}>. Current state: {truck.current_state}")

        else:
            # If no stations are available, place the truck in the station with the shortest queue
            station = min(self.stations, key=lambda s: len(s.queue))
            station.add_to_queue(truck.id)
            truck.current_state = TruckState.WAITING  # Ensure the truck is in the waiting state when assigned to a busy station
            truck.stats['total_wait_time'] += 1  # Increment wait time for each tick of the simulation
            logger.debug(f"<Truck {truck.id}> current state: {truck.current_state}.")
            #logger.debug(f'<Station {station.id}> Trucks in queue: {station.queue}: length {len(station.queue)}. Max Queue Length: {station.stats['max_queue_length']}')

    def format_simulation_report(self, report):
        """
        Format the simulation report into a readable string with proper formatting and sections.

        Args:
            report (dict): The simulation report dictionary

        Returns:
            str: Formatted report string
        """

        def format_time(minutes: int):
            """Convert minutes to hours and minutes format"""
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours:02d}h {mins:02d}m"

        # Initialize the formatted report
        lines = []

        # Simulation Overview
        lines.append("=" * 50)
        lines.append("LUNAR HELIUM-3 MINING SIMULATION REPORT")
        lines.append("=" * 50)
        lines.append(f"\nTotal Simulation Duration: {format_time(report['simulation_duration'])}")

        # Truck Statistics
        lines.append("\n" + "-" * 50)
        lines.append("MINING TRUCK STATISTICS")
        lines.append("-" * 50)

        # Calculate averages for overall statistics
        total_trucks = len(report['trucks'])
        avg_cycles = sum(i['number_of_unloads'] for i in report['trucks']) / total_trucks
        avg_mining = sum(i['mining_time'] for i in report['trucks']) / total_trucks
        avg_travel = sum(i['travel_time'] for i in report['trucks']) / total_trucks
        avg_unload = sum(i['unload_time'] for i in report['trucks']) / total_trucks

        lines.append(f"\nFleet Overview (Average per truck):")
        lines.append(f"• Total Trucks : {total_trucks}")
        lines.append(f"• Completed Cycles: {avg_cycles:.1f}")
        lines.append(f"• Mining Time: {format_time(int(avg_mining))}")
        lines.append(f"• Travel Time: {format_time(int(avg_travel))}")
        lines.append(f"• Unload Time: {format_time(int(avg_unload))}")

        lines.append("\nIndividual Truck Performance:")
        for truck in report['trucks']:
            lines.append(f"\nTruck #{truck['id']}:")
            lines.append(f"  • Completed Cycles: {truck['number_of_unloads']}")
            lines.append(f"  • Mining Time: {format_time(truck['mining_time'])}")
            lines.append(f"  • Travel Time: {format_time(truck['travel_time'])}")
            lines.append(f"  • Unload Time: {format_time(truck['unload_time'])}")
            lines.append(f"  • Wait Time: {format_time(truck['wait_time'])}")

        # Station Statistics
        lines.append("\n" + "-" * 50)
        lines.append("UNLOAD STATION STATISTICS")
        lines.append("-" * 50)

        total_processed = sum(i['trucks_processed'] for i in report['stations'])
        max_queue = max(i['max_queue'] for i in report['stations'])

        lines.append(f"\nOverall Statistics:")
        lines.append(f"• Total Trucks Processed: {total_processed}")
        lines.append(f"• Maximum Queue Length: {max_queue}")

        lines.append("\nIndividual Station Performance:")
        for station in report['stations']:
            lines.append(f"\nStation #{station['id']}:")
            lines.append(f"  • Trucks Processed: {station['trucks_processed']}")
            lines.append(f"  • Maximum Queue Length: {station['max_queue']}")

        # Efficiency Metrics
        lines.append("\n" + "-" * 50)
        lines.append("EFFICIENCY METRICS")
        lines.append("-" * 50)

        avg_trucks_per_hour = total_processed / (report['simulation_duration'] / 60)
        lines.append(f"\n• Average Processing Rate: {avg_trucks_per_hour:.1f} trucks/hour")

        return "\n".join(lines)


    def generate_report(self):
        """Generate simulation report"""
        return {
            'simulation_duration': SIMULATION_DURATION,
            'trucks': [{
                'id': truck.id,
                'number_of_unloads': truck.stats['unloads_completed'],
                'mining_time': truck.stats['total_mining_time'],
                'travel_time': truck.stats['total_travel_time'],
                'unload_time': truck.stats['total_unload_time'],
                'wait_time': truck.stats['total_wait_time']
            } for truck in self.trucks],
            'stations': [{
                'id': station.id,
                'trucks_processed': station.stats['total_trucks_processed'],
                'max_queue': station.stats['max_queue_length']
            } for station in self.stations]
        }