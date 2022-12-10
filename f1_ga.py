import random
import numpy
from deap import algorithms
from deap import base
from deap import benchmarks
from deap import creator
from deap import tools
import xlsxwriter
import matlab.engine
import shutil
import os
try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequence

from itertools import repeat

eng = matlab.engine.start_matlab()

car_num = 0

def xlsxsetup(arr):
    global car_num
    filename = 'Individuals\individual_' + str(car_num) + '.xlsx'
    car_num += 1
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('Info')
    worksheet.write('A1', 'Category')
    worksheet.write('B1', 'Description')
    worksheet.write('C1', 'Value')
    worksheet.write('D1', 'Unit')
    worksheet.write('E1', 'Comment')

    row = 1
    col = 1

    info = arr

    for Description, Value in (info):
        worksheet.write(row, col, Description)
        worksheet.write(row, col + 1, Value)
        row += 1

    worksheet2 = workbook.add_worksheet('Torque Curve')
    worksheet2.write('A1', 'Engine Speed [rpm]')
    worksheet2.write('B1', 'Torque [Nm]')

    torque_curve = (
        [1000, 529],
        [2000, 540],
        [3000, 564],
        [4000, 598],
        [5000, 690],
        [6000, 702],
        [7000, 782],
        [8000, 817],
        [9000, 776],
        [10000, 776],
        [11000, 750],
        [12000, 736],
        [13000, 684],
        [14000, 529],
        [15000, 460],
    )

    row = 1
    col = 0

    for rpm, Nm in (torque_curve):
        worksheet2.write(row, col, rpm)
        worksheet2.write(row, col + 1, Nm)
        row += 1

    workbook.close()

    return filename

evolving = (
    ['Mass', 0],                             #mass = [825, 905]
    ['Front Mass Distribution', 0],         #frontal_mass = [0.445, 0.540]
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

bounds = (
    [825, 905],
    [44.5,  54.0],
    [3460, 3600],
    [-4.4, -2.8],
    [-1.1, -0.7],
    [50, 70],
    [0.9, 1.4],
    [325, 330],
    [52, 52.8],
    [1, 6],
    [800,1200],
    [800,1200],
    [2.21,3],
    [1.79, 2.2],
    [1.51, 1.78],
    [1.31, 1.5],
    [1.15, 1.3],
    [1.05, 1.14],
    [0.9, 1.04],
    [0.7, 0.89],
)

def evalLapTime(ind):
    info = (
        ['Name', 'Formula 1'],
        ['Type', 'Open Wheel'],
        ['Total Mass', 850],
        ['Front Mass Distribution', 45],
        ['Wheelbase', 3500],
        ['Steering Rack Ratio', 10],
        ['Lift Coefficient CL',  -4.8],
        ['Drag Coefficient CD', -1.2],
        ['CL Scale Multiplier', 1],
        ['CD Scale Multiplier', 1],
        ['Front Aero Distribution', 50],
        ['Frontal Area', 1],
        ['Air Density', 1.225],
        ['Disc Outer Diameter', 325],
        ['Pad Height', 52],
        ['Pad Friction Coefficient', 0.45],
        ['Caliper Number of Pistons', 6],
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
        ['Front Cornering Stiffness', 900],
        ['Rear Cornering Stiffness', 1100],
        ['Power Factor Multiplier', 1], 
        ['Thermal Efficiency', 0.35],
        ['Fuel Lower Heating Value', 47200000],
        ['Drive Type', 'RWD'],
        ['Gear Shift Time', 0.01],
        ['Primary Gear Efficiency', 1],
        ['Final Gear Efficiency', 0.92],
        ['Gearbox Efficiency', 0.98],
        ['Primary Gear Reduction', 1],
        ['Final Gear Reduction', 8],
        ['1st Gear Ratio', 2.57],
        ['2nd Gear Ratio', 2.11],
        ['3rd Gear Ratio', 1.75],
        ['4th Gear Ratio', 1.46],
        ['5th Gear Ratio', 1.29],
        ['6th Gear Ratio', 1.13],
        ['7th Gear Ratio', 1],
        ['8th Gear Ratio', 0.8],
        ['9th Gear Ratio', ''],
        ['10th Gear Ratio', ''],
    )
    info[2][1] = ind[0]
    info[3][1] = ind[1]
    info[4][1] = ind[2]
    info[6][1] = ind[3]
    info[7][1] = ind[4]
    info[10][1] = ind[5]
    info[11][1] = ind[6]
    info[13][1] = ind[7]
    info[14][1] = ind[8]
    info[16][1] = ind[9]
    info[29][1] = ind[10]
    info[30][1] = ind[11]
    info[41][1] = ind[12]
    info[42][1] = ind[13]
    info[43][1] = ind[14]
    info[44][1] = ind[15]
    info[45][1] = ind[16]
    info[46][1] = ind[17]
    info[47][1] = ind[18]
    info[48][1] = ind[19]
    filename = xlsxsetup(info)
    eng.OpenVEHICLEnew(filename, nargout=0)
    return float(eng.OpenLAP(filename, nargout=1)),

#TODO-ANDY
def cxIntermediate(ind1, ind2, ratio):
    size = len(ind1)
    for i in range(size):
        if ind1[i] < ind2[i]:
            ind1[i] = ind1[i] + ratio * (ind2[i] - ind1[i])
        else:
            ind1[i] = ind2[i] + ratio * (ind1[i] - ind2[i])
        
    return ind1, ind2

def cxSimulatedBinaryBounded(ind1, ind2, eta, low, up):
    size = min(len(ind1), len(ind2))
    if not isinstance(low, Sequence):
        low = repeat(low, size)
    elif len(low) < size:
        raise IndexError("low must be at least the size of the shorter individual: %d < %d" % (len(low), size))
    if not isinstance(up, Sequence):
        up = repeat(up, size)
    elif len(up) < size:
        raise IndexError("up must be at least the size of the shorter individual: %d < %d" % (len(up), size))

    for i, xl, xu in zip(range(size), low, up):
        if random.random() <= 0.5:
            # This epsilon should probably be changed for 0 since
            # floating point arithmetic in Python is safer
            if abs(ind1[i] - ind2[i]) > 1e-14:
                x1 = min(ind1[i], ind2[i])
                x2 = max(ind1[i], ind2[i])
                rand = random.random()

                beta = 1.0 + (2.0 * (x1 - xl) / (x2 - x1))
                alpha = 2.0 - beta ** -(eta + 1)
                if rand <= 1.0 / alpha:
                    beta_q = (rand * alpha) ** (1.0 / (eta + 1))
                else:
                    beta_q = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (eta + 1))

                c1 = 0.5 * (x1 + x2 - beta_q * (x2 - x1))

                beta = 1.0 + (2.0 * (xu - x2) / (x2 - x1))
                alpha = 2.0 - beta ** -(eta + 1)
                if rand <= 1.0 / alpha:
                    beta_q = (rand * alpha) ** (1.0 / (eta + 1))
                else:
                    beta_q = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (eta + 1))
                c2 = 0.5 * (x1 + x2 + beta_q * (x2 - x1))

                c1 = min(max(c1, xl), xu)
                c2 = min(max(c2, xl), xu)

                if random.random() <= 0.5:
                    ind1[i] = c2
                    ind2[i] = c1
                else:
                    ind1[i] = c1
                    ind2[i] = c2

    return ind1, ind2

def mutationpower(individual, indpb):
    size = len(individual)
    for i in range(size):
        if random.random() < indpb:
            lb = bounds[i][0]
            ub = bounds[i][1]
            gene = individual[i]
            r = random.uniform(0, 1)
            s = random.uniform(0,1)**0.35
            t = (gene-lb)/(ub-lb)
            if t < r:
                individual[i] = gene - s*(gene-lb)
            else:
                individual[i] = gene + s*(ub-gene)
    return individual,

nonUniformProb = [.15, .15, .075, .15, .15, .15, .15, .05, .05, .05, .075, .075, .15, .15, .15, .15, .15, .15, .15, .15]

def nonUniformMutation(individual, indpb):
    size = len(individual)
    for i in range(size):
        if random.random() < indpb:
            if random.random() < nonUniformProb[i]:
                lb = bounds[i][0]
                ub = bounds[i][1]  
                if random.random() >= .5:
                    individual[i] = individual[i] * (1 + nonUniformProb[i])
                    if individual[i] > ub:
                        individual[i] = ub
                else:
                    individual[i] = individual[i] * (1 - nonUniformProb[i])
                    if individual[i] < lb:
                        individual[i] = lb
    return individual,

#TODO-DANIEL
# Write island model stuff


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register('vehicle_mass', random.uniform, 825, 905)
toolbox.register('frontal_mass', random.uniform, 44.5, 54.0)
toolbox.register('wheelbase', random.randint, 3460, 3600)
toolbox.register('lift_coef', random.uniform, -4.4, -2.8)
toolbox.register('drag_coef', random.uniform, -1.1, -0.7)
toolbox.register('aero_dist', random.uniform, 50, 70)
toolbox.register('frontal_area', random.uniform, 0.9, 1.4)
toolbox.register('disc_diameter', random.randint, 325, 330)
toolbox.register('pad_height', random.uniform, 52, 52.8)
toolbox.register('caliper_num_pistons', random.randint, 1, 6)
toolbox.register('front_stiffness', random.randint, 800, 1200)
toolbox.register('rear_stiffness', random.randint, 800, 1200)
toolbox.register('first_ratio', random.uniform, 2.21, 3)
toolbox.register('second_ratio', random.uniform, 1.79, 2.2)
toolbox.register('third_ratio', random.uniform, 1.51, 1.78)
toolbox.register('fourth_ratio', random.uniform, 1.31, 1.5)
toolbox.register('fifth_ratio', random.uniform, 1.15, 1.3)
toolbox.register('sixth_ratio', random.uniform, 1.05, 1.14)
toolbox.register('seventh_ratio', random.uniform, 0.9, 1.04)
toolbox.register('eight_ratio', random.uniform, 0.7, 0.89)
toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.vehicle_mass,
    toolbox.frontal_mass,
    toolbox.wheelbase,
    toolbox.lift_coef,
    toolbox.drag_coef,
    toolbox.aero_dist,
    toolbox.frontal_area,
    toolbox.disc_diameter,
    toolbox.pad_height,
    toolbox.caliper_num_pistons,
    toolbox.front_stiffness,
    toolbox.rear_stiffness,
    toolbox.first_ratio,
    toolbox.second_ratio,
    toolbox.third_ratio,
    toolbox.fourth_ratio,
    toolbox.fifth_ratio,
    toolbox.sixth_ratio,
    toolbox.seventh_ratio,
    toolbox.eight_ratio),
    n=1
)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evalLapTime)
#toolbox.register("mate", cxIntermediate, ratio=0.8)
toolbox.register("mate", tools.cxUniform, indpb=0.8)
#toolbox.register("mate", cxSimulatedBinaryBounded, eta=0.5, low=list(map(lambda x: x[0], bounds)), up=list(map(lambda x: x[1], bounds)))
#toolbox.register("mutate", mutationpower, indpb=0.3)
toolbox.register("mutate", nonUniformMutation, indpb=0.3)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    shutil.rmtree('Individuals')
    shutil.rmtree('OpenVEHICLE Vehicles')
    os.makedirs('Individuals')
    random.seed()

    pop = toolbox.population(n=30)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", numpy.mean)
    stats.register("Std", numpy.std)
    stats.register("Min", numpy.min)
    stats.register("Max", numpy.max)

    algorithms.eaSimple(pop, toolbox, cxpb=0.9, mutpb=0.4, ngen=100, stats=stats, halloffame=hof, verbose=True)

    print(hof[0])

    return pop, stats, hof


if __name__ == "__main__":
    main()