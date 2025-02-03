import time
import logging
import os
import json
from datetime import datetime
from src.utils.config import setup_configuration
from src.utils.constants import SIMULATION_DURATION
from src.simulation import MiningSimulation

logger = logging.getLogger(__name__)

def main():
    try:
        # Get the directory containing your project
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        yaml_file = os.path.join(project_root, "config.yaml")

        config = setup_configuration(yaml_file)

        # Initialize and run simulation
        simulation = MiningSimulation(
            num_trucks=config['simulation']['trucks'],
            num_stations=config['simulation']['stations']
        )

        start_time = time.time()
        simulation.run_simulation()
        end_time = time.time()

        # Generate statistics
        report = simulation.generate_report()
        formatted_report = simulation.format_simulation_report(report)
        print(formatted_report)

        # Create a unique json filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_output_path = os.path.join(project_root, "src", "reports", f"{timestamp}_sim_report_.json")

        # Save the report to a JSON file
        with open(json_output_path, "w") as json_file:
            json.dump(report, json_file, indent=4)

        logger.info(f"{SIMULATION_DURATION/60:.1f} hour Simulation executed in {end_time - start_time:.3f} seconds.")
        logger.info(f"Simulation results saved to: {json_output_path}")
    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    main()