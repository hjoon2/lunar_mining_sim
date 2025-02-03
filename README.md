# Lunar Mining Simulation

A Python simulation of lunar mining operations, modeling the interaction between mining trucks and unloading stations.

## Features

- Simulates multiple mining trucks operating simultaneously
- Models unloading station queues and processing
- Tracks detailed statistics for both trucks and stations
- Configurable via YAML and command-line arguments
- Comprehensive logging system
- Generates simulation reports both in a human-readable format printed to the terminal and saved as JSON files for further analysis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lunar-mining-sim.git
cd lunar-mining-sim
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

## Configuration

The simulation can be configured through:
1. `config.yaml` file
2. Command-line arguments

Example `config.yaml`:
```yaml
simulation:
  trucks: 5
  stations: 2
  logging:
    level: INFO
```

Command-line options:
- `--trucks`: Number of mining trucks
- `--stations`: Number of unloading stations
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Usage

Run the simulation:
```bash
python -m src.main
```

With command-line options:
```bash
python -m src.main --trucks 8 --stations 3 --log-level DEBUG
```

Running with `--log-level DEBUG` will print ALL activities happening every minute in the simulation.

## Simulation Report
The simulation generates two types of reports:
1. JSON report saved to the `reports/` directory with a timestamped filename, such as `report_2025-02-02_14-30-45.json`, containing all the detailed statistics in machine-readable format for further analysis.
2. Human-readable report printed to stdout, showing detailed statistics of the simulation including:
   - Simulation Duration
   - Truck Statistics: including mining time, travel time, unload time, and more
   - Station Statistics: including the total number of trucks processed and maximum queue length
    ```
   INFO - Starting simulation for 72.0 hours with 5 trucks and 1 station
    ==================================================
    LUNAR HELIUM-3 MINING SIMULATION REPORT
    ==================================================
    
    Total Simulation Duration: 72h 00m
    
    --------------------------------------------------
    MINING TRUCK STATISTICS
    --------------------------------------------------
    
    Fleet Overview (Average per truck):
    • Total Trucks : 5
    • Completed Cycles: 16.6
    • Mining Time: 52h 29m
    • Travel Time: 16h 42m
    • Unload Time: 01h 23m
    
    Individual Truck Performance:
    
    Truck #0:
      • Completed Cycles: 16
      • Mining Time: 53h 02m
      • Travel Time: 16h 00m
      • Unload Time: 01h 20m
      • Wait Time: 00h 00m
    
    Truck #1:
      • Completed Cycles: 16
      • Mining Time: 54h 21m
      • Travel Time: 16h 00m
      • Unload Time: 01h 20m
      • Wait Time: 00h 00m
    
    Truck #2:
      • Completed Cycles: 17
      • Mining Time: 53h 20m
      • Travel Time: 17h 00m
      • Unload Time: 01h 25m
      • Wait Time: 00h 00m
    
    Truck #3:
      • Completed Cycles: 17
      • Mining Time: 48h 38m
      • Travel Time: 17h 00m
      • Unload Time: 01h 25m
      • Wait Time: 00h 00m
    
    Truck #4:
      • Completed Cycles: 17
      • Mining Time: 53h 05m
      • Travel Time: 17h 30m
      • Unload Time: 01h 25m
      • Wait Time: 00h 00m
    
    --------------------------------------------------
    UNLOAD STATION STATISTICS
    --------------------------------------------------
    
    Overall Statistics:
    • Total Trucks Processed: 83
    • Maximum Queue Length: 0
    
    Individual Station Performance:
    
    Station #0:
      • Trucks Processed: 83
      • Maximum Queue Length: 0
    
    --------------------------------------------------
    EFFICIENCY METRICS
    --------------------------------------------------
    
    • Average Processing Rate: 1.2 trucks/hour
    INFO - 72.0 hour Simulation executed in 0.008 seconds.
    INFO - Simulation results saved to: src\reports\20250202_170725_sim_report_.json

   ```
## Running Unit Tests
This project uses `pytest` for unit testing and are located in `tests` directory. Follow these steps to run the tests:
1. Run all Tests with `pytest -v`:
```commandline
# Navigate to tests directory from project root and run test
cd tests
pytest -v

=============================================================================================================================================== test session starts ===============================================================================================================================================
cachedir: .pytest_cache
collected 8 items                                                                                                                                                                                                                                                                                                   

tests/test_mining_truck.py::test_truck_initial_state PASSED                                                                                                                                                                                                                                                  [ 12%] 
tests/test_mining_truck.py::test_mining_progress PASSED                                                                                                                                                                                                                                                      [ 25%] 
tests/test_mining_truck.py::test_truck_unloading PASSED                                                                                                                                                                                                                                                      [ 37%] 
tests/test_mining_truck.py::test_truck_waiting PASSED                                                                                                                                                                                                                                                        [ 50%] 
tests/test_sim.py::test_simulation_setup PASSED                                                                                                                                                                                                                                                              [ 62%] 
tests/test_sim.py::test_simulation_run PASSED                                                                                                                                                                                                                                                                [ 75%] 
tests/test_unload_station.py::test_station_initial_state PASSED                                                                                                                                                                                                                                              [ 87%] 
tests/test_unload_station.py::test_station_queue PASSED                                                                                                                                                                                                                                                      [100%] 

================================================================================================================================================ 8 passed in 0.04s ================================================================================================================================================ 
```
2. Run Specific Tests with `pytest -v path/to/test_file.py`:
```commandline
pytest -v .\test_mining_truck.py

=============================================================================================================================================== test session starts ===============================================================================================================================================
cachedir: .pytest_cache
collected 4 items

test_mining_truck.py::test_truck_initial_state PASSED                                                                                                                                                                                                                                                        [ 25%] 
test_mining_truck.py::test_mining_progress PASSED                                                                                                                                                                                                                                                            [ 50%] 
test_mining_truck.py::test_truck_unloading PASSED                                                                                                                                                                                                                                                            [ 75%] 
test_mining_truck.py::test_truck_waiting PASSED                                                                                                                                                                                                                                                              [100%] 

================================================================================================================================================ 4 passed in 0.02s ================================================================================================================================================ 

```

## Project Structure

```
lunar_mining_sim/
├── README.md
├── requirements.txt
├── config.yaml
├── src/
│   ├── main.py                 # Entry point
│   ├── simulation.py           # Core simulation logic
│   ├── models/                 # Data models
│   ├── utils/                  # Utilities
│   └── reports/               # JSON Reports
└── tests/                     # Unit Test files
```