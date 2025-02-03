import yaml
import argparse
import logging
from .logger import setup_logging

def setup_configuration(input_file):
    """
    Sets up simulation configuration using a hybrid approach:
    - Loads base configuration from YAML file (num of trucks and stations, logging level)
    - Allows command-line overrides for commonly changed parameters
    - Returns a complete configuration object
    """
    # First, load the base configuration from config.yaml file
    try:
        with open(input_file, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file {input_file} not found!")

    # Parse command line arguments that can override YAML settings
    parser = argparse.ArgumentParser(description='Lunar Mining Simulation')
    parser.add_argument('--trucks', type=int,
                        default=config['simulation']['trucks'],
                        help='Number of mining trucks')
    parser.add_argument('--stations', type=int,
                        default=config['simulation']['stations'],
                        help='Number of unloading stations')
    parser.add_argument('--log-level',
                        default=config['simulation']['logging']['level'],
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='Set the logging level')

    args = parser.parse_args()

    # Override config file values with command line arguments
    config['simulation']['trucks'] = args.trucks
    config['simulation']['stations'] = args.stations
    config['simulation']['logging']['level'] = args.log_level

    # set log level
    setup_logging(config['simulation']['logging']['level'])

    return config