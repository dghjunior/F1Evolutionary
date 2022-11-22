# F1Evolutionary
This is a project written by Daniel Harper and Andy Weaver for CSCI 4560 (Evolutionary Computation) taught by Dr. Khaled Rasheed. The majority of files in this repository are taken from the OpenLap Lap Time Simulator by Michael Chalkiopoulos. This repository can be found here: [OpenLap GitHub](https://github.com/mc12027/OpenLAP-Lap-Time-Simulator).

## General Information
This is a genetic algorithm (details of algorithm below) using the OpenLap Lap Time Simulator as a fitness function. The goal is to perform optimization over a lap time for a Formula 1 car (representation details below)

## Genetic Algorithm Details
- Population:
    - Size 30
    - Initial Range: [5-100, 1-10]
- Representation:
    - List of doubles
- Selection:
    - Type: Tournament Selection
    - Tournament Size: 2
- Crossover:
    - Crossover Fraction: 0.8
    - Crossover Function: Intermediate
- Mutation:
    - Mutation Function: Constraint Dependent

## Technologies
random - 
numpy - 
deap - 
xlsxwriter - 
matlab.engine - 

## Representation of Vehicle
Vehicle representation is stored in an Excel spreadsheet file type '.xlsx'. We used the xlsxwriter library in Python to take an array of integer, double, and string values to store in a spreadsheet. Below is a list of all 51 values needed for the OpenVEHICLE file to represent a vehicle for use with the lap time simulator

### Fixed Values
---
Name - 'Formula 1'  
Type - 'Open Wheel'  
Air Density - 1.225  
Total Mass - 798   
Steering Rack Ratio - 10    
Pedal Ratio - 4  
Grip Factor Multiplier - 1  
Tire Radius - 457  
Rolling Resistance - -0.001   
Longitudinal Friction Coefficient - 2  
Longitudinal Friction Load Rating - 300  
Longitudinal Friction Sensitivity - 0.0001  
Lateral Friction Coefficient - 2  
Lateral Friction Load Rating - 300  
Lateral Friction Sensitivity - 0.0001  
Power Factor Multiplier - 1  
Thermal Efficiency - 0.35  
Fuel Lower Heating Value - 47200000  
Drive Type - 'RWD'  
Gear Shift Time - 0.01
Primary Gear Efficiency - 1  
Final Gear Efficiency - 0.92  
Gearbox Efficiency - 0.98  
CL Scale Multiplier - 1  
CD Scale Multiplier - 1  
9th gear ratio - ''  
10th gear ratio - ''  
Primary Gear Reduction - 1    
Final Gear Reduction - 8  
Pad Friction Coefficient - 0.45  
Caliper Piston Diameter - 52   
Master Cylinder Piston Diameter - 32.5  

### Evolving Values
---
Front Mass Distribution - [44.5, 54]  
Wheelbase - [3460, 3600]  
Lift Coefficient CL - [-4.4, -2.8]  
Drag Coefficient CD - [-1.1, -0.7]  
Front Aero Distribution - [50, 70]  
Frontal Area - [0.9, 1.4]  
Disc Outer Diameter - [325, 330]   
Pad Height - [52, 52.8]  
Caliper Number of Pistons - [1, 6]    
Front Cornering Stiffness - [800, 1200]  
Rear Cornering Stiffness - [800, 1200]  
1st gear ratio - [2, 3]  
2nd gear ratio - [1.75, 2.2]    
3rd gear ratio - [1.5, 1.9]  
4th gear ratio - [1.2, 1.6]  
5th gear ratio - [1.15, 1.4]  
6th gear ratio - [1.05, 1.25]  
7th gear ratio - [0.9, 1.15]  
8th gear ratio - [0.75, 1]  