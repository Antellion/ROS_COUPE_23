# ROS_COUPE_23
src code of "let him cook" robot of RIR Robotech, Robotic's French Cup 2023

## Getting Started

Coupe is the main pkg you will find all node and launch file

other are tests packages works individualy.
INTERFACES IS REQUIRED EACH TIME

### Main launch

ROS2 IS Required 
In order to launch master pkg

```
. install/setup.bach
ros2 launch coupe coupe_launch.py
```

### Running others

Other pkg running
in order to launch multiple node open different shell

```
. install/setup.bash
ros2 run <package_name> <node name>
```

## Authors

* **Leo Mourgues** - *Initial work* - [Antellion](https://github.com/Antellion)* 
