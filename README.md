# paradigm-shift-py
# Programming Paradigms

Electric Vehicles have BMS - Battery Management Systems

[Here is an article that helps to understand the need for BMS](https://circuitdigest.com/article/battery-management-system-bms-for-electric-vehicles)

[Wikipedia gives an idea of the types and topologies](https://en.wikipedia.org/wiki/Battery_management_system)

[This site gives the optimum Charging-temperature limits](https://batteryuniversity.com/learn/article/charging_at_high_and_low_temperatures)

[This abstract suggests a range for the optimum State of Charge](https://www.sciencedirect.com/science/article/pii/S2352484719310911)

[Here is a reference for the maximum charge rate](https://www.electronics-notes.com/articles/electronic_components/battery-technology/li-ion-lithium-ion-charging.php#:~:text=Constant%20current%20charge:%20In%20the%20first%20stage%20of,rate%20of%20a%20maximum%20of%200.8C%20is%20recommended.)

## Possible purpose

- Protect batteries while charging:
at home, in public place, within vehicle / regenerative braking
- Estimate life, inventory and supply chains

## The Starting Point

We will explore the charging phase of Li-ion batteries to start with.

## Issues

- The code here has high complexity in a single function.
- The tests are not complete - they do not cover all the needs of a consumer

## Tasks

1. Reduce the cyclomatic complexity.
1. Avoid duplication - functions that do nearly the same thing
1. Complete the tests - cover all conditions.
1. To treat, we need to know the abnormal vital and the breach -
whether high or low. Add this capability.
1. Add the ability to plug-in different reporters to this code.

## The Exploration

How well does our code hold-out in the rapidly evolving EV space?
Can we add new functionality without disturbing the old?

## The Landscape

- Limits may change based on new research
- Technology changes due to obsolescence
- Sensors may be from different vendors with different accuracy
- Predicting the future requires Astrology!

## Keep it Simple

Shorten the Semantic distance

- Procedural to express sequence
- Functional to express relation between input and output
- Object oriented to encapsulate state with actions
- Apect oriented to capture repeating aspects



# Battery Monitor

A simple Python class to monitor battery parameters such as temperature, state of charge (SoC), and charge rate. The class provides methods to check if these parameters are within safe limits and report any issues.

## Features

- **Temperature Monitoring**: Ensures the battery temperature is within the safe range of 0°C to 45°C.
- **State of Charge (SoC) Monitoring**: Ensures the battery's state of charge is within the safe range of 20% to 80%.
- **Charge Rate Monitoring**: Ensures the battery's charge rate does not exceed 0.8C.
- **Early Warnings**: Provides warnings when parameters are approaching their limits with a 5% tolerance.

## Usage

To use the `BatteryMonitor` class, you need to provide a reporter function that handles the messages. Two example reporters are provided: `console_reporter` (prints messages to the console) and `file_reporter` (writes messages to a file).

### Example

```python
from battery_monitor import BatteryMonitor, console_reporter

# Create a BatteryMonitor instance with the console reporter
monitor = BatteryMonitor(console_reporter)

# Check battery parameters
monitor.battery_is_ok(25, 70, 0.7)
monitor.battery_is_ok(50, 70, 0.7)
monitor.battery_is_ok(25, 85, 0.7)
monitor.battery_is_ok(25, 70, 0.9)
monitor.battery_is_ok(-5, 15, 0.9)

# Test warnings
monitor.battery_is_ok(2, 22, 0.75)
