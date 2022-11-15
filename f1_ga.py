import array
import logging
import random
import numpy
from deap import algorithms
from deap import base
from deap import benchmarks
from deap import creator
from deap import tools
import xlsxwriter
import matlab.engine

eng = matlab.engine.start_matlab()
eng.cd(r'OpenLAP', nargout=0)

workbook = xlsxwriter.Workbook('F1Car.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Category')
worksheet.write('B1', 'Description')
worksheet.write('C1', 'Value')
worksheet.write('D1', 'Unit')
worksheet.write('E1', 'Comment')

row = 2
col = 3

info = (
    ['Name', 'Formula 1'],
    ['Type', 'Open Wheel'],
    ['Total Mass', 798],
    ['Front Mass Distribution', 0],
    ['Wheelbase', 0],
    ['Steering Rack Ratio', 10],
    ['Lift Coefficient CL',  0],
    ['Drag Coefficient CD', 0],
    ['CL Scale Multiplier', 1],
    ['CD Scale Multiplier', 1],
    ['Front Aero Distribution', 0],
    ['Frontal Area', 0],
    ['Air Density', 1.225],
    ['Disc Outer Diameter', 0],
    ['Pad Height', 0],
    ['Pad Friction Coefficient', 0.45],
    ['Caliper Number of Pistons', 0],
    ['Caliper Piston Diameter', 52],
    ['Master Cylinder Piston Diameter', 32.5],
    ['Pedal Ratio', 4],
    ['Grip Factor Multiplier', 1],
    ['Tyre Radius', 457],
    ['Rolling Resistance', -0.001],
    ['Longitudinal Friction Coefficient', 2],
    ['Longitudinal Friction Load Rating', 300],
    ['Longitudinal Friction Sensitivity', 0.0001],
    ['Lateral Friction Coefficient', 2],
    ['Lateral Friction Load Rating', 300],
    ['Lateral Friction Sensitivity', 0.0001],
    ['Front Cornering Stiffness', 0],
    ['Rear Cornering Stiffness', 0],
    ['Power Factor Multiplier', 1], 
    ['Thermal Efficiency', 0.35],
    ['Fuel Lower Heating Value', 47200000],
    ['Drive Type', 'RWD'],
    ['Gear Shift Time', 0.01],
    ['Primary Gear Efficiency', 1],
    ['Final Gear Efficiency', 0.92],
    ['Gearbox Efficiency', 0.98],
    ['Primary Gear Reduction', 1],
    ['Final Gear Reduction', 7],
    ['1st Gear Ratio', 0],
    ['2nd Gear Ratio', 0],
    ['3rd Gear Ratio', 0],
    ['4th Gear Ratio', 0],
    ['5th Gear Ratio', 0],
    ['6th Gear Ratio', 0],
    ['7th Gear Ratio', 0],
    ['8th Gear Ratio', 0],
    ['9th Gear Ratio', 0],
    ['10th Gear Ratio', 0],
)

evolving = (
    ['Front Mass Distribution', 0],          #frontal_mass = [0.445, 0.540]
    ['Wheelbase', 0],                       #wheelbase = [3460mm, 3600mm]
    ['Lift Coefficient CL', 0],             #lift_coef = [-4.4, -2.8]
    ['Drag Coefficient CD', 0],             #drag_coef = [-1.1, --0.7]
    ['Front Aero Distribution', 0],         #aero_dist = [0.5, 0.7]
    ['Frontal Area', 0],                    #frontal_area = [0.9m2, 1.4m2]
    ['Disc Outer Diameter', 0],             #disc_diameter = [325mm, 330mm]
    ['Pad Height', 0],                      #pad_height = [52mm, 52.8mm]
    ['Caliper Number of Pistons', 0],       #caliper_num_pistons = [1, 6]
    ['Front Cornering Stiffness', 0],       #front_stiffness = [800, 1200]
    ['Rear Cornering Stiffness', 0],        #rear_stiffness = [800, 1200]
    ['1st Gear Ratio', 0],                  #first_ratio = [2, 3]
    ['2nd Gear Ratio', 0],                  #second_ratio = [Prev*0.7, Prev*0.9]
    ['3rd Gear Ratio', 0],                  #third_ratio = [Prev*0.7, Prev*0.9]
    ['4th Gear Ratio', 0],                  #fourth_ratio = [Prev*0.7, Prev*0.9]
    ['5th Gear Ratio', 0],                  #fifth_fatio = [Prev*0.7, Prev*0.9]
    ['6th Gear Ratio', 0],                  #sixth_ratio = [Prev*0.7, Prev*0.9]
    ['7th Gear Ratio', 0],                  #seventh_ratio = [Prev*0.7, Prev*0.9]
    ['8th Gear Ratio', 0],                  #eighth_ratio = [Prev*0.7, Prev*0.9]                   
)

Prev = 2

bounds = (
    [0.445,  0.540],
    [3460, 3600],
    [-4.4, -2.8],
    [-1.1, -0.7],
    [0.5, 0.7],
    [0.9, 1.4],
    [325, 330],
    [52, 52.8],
    [1, 6],
    [800,1200],
    [800,1200],
    [2,3],
    [Prev*0.7, Prev*0.9],
    [Prev*0.7, Prev*0.9],
    [Prev*0.7, Prev*0.9],
    [Prev*0.7, Prev*0.9],
    [Prev*0.7, Prev*0.9],
    [Prev*0.7, Prev*0.9],
    [Prev*0.7, Prev*0.9],
)

workbook.close()

#TODO-DANIEL
def evalLapTime(filename):
    eng.OpenVEHICLEnew(nargout=0)
    laptime = eng.OpenLAP(nargout=1)
    print(laptime)

#TODO-ANDY
def cxIntermediate(ratio):
    return 0.0

#TODO-DANIEL add loop for individual genes and bounds
def mutationAdaptFeasible():
    lb = 5
    ub = 100
    gene = 60
    r = random.uniform(0, 1)
    s = random.uniform(0,1)**0.35
    t = (gene-lb)/(ub-lb)
    if t < r:
        gene = gene - s*(gene-lb)
    else:
        gene = gene + s*(ub-gene)        


#TODO-DANIEL
# Write island model stuff


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

#TODO fix gene representation
toolbox.register("attr_float", random.uniform, -5, 5)

#TODO add new genes for individual representation
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 51)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evalLapTime)
toolbox.register("mate", cxIntermediate, ratio = 0.8)
toolbox.register("mutate", mutationAdaptFeasible)
toolbox.register("select", tools.selTournament, tournsize=2)

def main():
    random.seed()
    mutationAdaptFeasible()

    pop = toolbox.population(n=30)
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", numpy.mean)
    stats.register("Std", numpy.std)
    stats.register("Min", numpy.min)
    stats.register("Max", numpy.max)

    #TODO-DANIEL check mutation probability
    algorithms.eaSimple(pop, toolbox, cxpb=1, mutpb=0.5, ngen=500, stats=stats, halloffame=hof, verbose=True)

    return pop, stats, hof


if __name__ == "__main__":
    main()