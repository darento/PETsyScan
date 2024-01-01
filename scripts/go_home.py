#!/usr/bin/env python3

"""Move the motor to the home position. Reverse the direction of the motor if it is not moving in the right direction. 
Usage: find_home.py YAMLCONF

Arguments:
    YAMLCONF  File with all parameters to take into account in the scan.

Options:
    -h --help     Show this screen.
"""

from docopt import docopt
import yaml
import sys
from src.config import validate_yaml_dict

from src.motor_control import MotorControl
from src.motor_control import serial_ports

if __name__ == "__main__":
    args = docopt(__doc__)
    yaml_conf = args["YAMLCONF"]

    with open(yaml_conf) as yaml_reader:
        yaml_dict = yaml.safe_load(yaml_reader)

    validate_yaml_dict(yaml_dict)

    # Find the motor port
    motor_port = serial_ports()

    if motor_port is None:
        print("No motor port found")
        sys.exit(1)

    # Create a MotorControl instance for each motor
    motors = []
    for i in range(yaml_dict["num_motors"]):
        motor_name = f"motor{chr(88 + i)}"  # 88 is ASCII for 'X'
        motor_config = yaml_dict[motor_name]
        motor = MotorControl(
            motor_port,
            motor_config["relation"],
            motor_config["microstep"],
            motor_config["start"],
            motor_config["end"],
            motor_config["step_size"],
            motor_name,
            i + 1,
            motor_config["speed"],
            motor_config["max_speed"],
            motor_config["acceleration"],
        )
        motors.append(motor)
    for motor in motors:
        motor.find_home()