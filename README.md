# PRA_instance_generator

## Overview
This project includes a instance generator that was developed to generate instances of patient-to-room and nurse-to-patient assignment described in our [preprint](https://arxiv.org/abs/2309.10739). It creates JSON files containing information about nurses, patients, rooms, and shifts based on input parameters. The generated instances can be used for scheduling and optimization purposes.

## Prerequisites

Before using this script, make sure you have the following installed:
- Python 3.x
- Required Python libraries (NumPy)

## Input Parameters

You can customize the instance generation by modifying the input parameters in the script. Here's a brief explanation of some key parameters:

- `n_eq_instances`: Number of equal instances to generate.
- `plan_weeks`: Number of weeks to plan for.
- `room_sizes`: List of room capacities.
- `room_balances`: List of room balancing percentages.
- `equipments`: Equipment available in rooms.
- `nurse_skills`: Number of nurse skill levels.
- `nurse_max_load`: Maximum workload for nurses.
- `rest_rooms`: Number of rest rooms.
- `occupancy_rates`: Occupancy rate for patient rooms.
- `fix_nurses`: Number of fixed nurses.
- `mode`: Generation mode (auto or manual).

## Output

The script generates a JSON file in the current directory. This file represents a nurse scheduling instance based on the input parameters.
Filename `random_instance_<n_week>_<room_config>_<room_balancing>_<fix_nurses>_<nurse_skill_level>_<equipment>_<id>.json`

## License

This code is provided under the [MIT License](LICENSE).

For questions about the Generator, please contact Tom Lorenz Klein (tom.klein[@]tum.de)