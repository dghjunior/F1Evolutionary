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
#eng.cd(r'OpenLAP', nargout=0)

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
        [1000, 125],
        [2000, 125],
        [3000, 125],
        [4000, 125],
        [5000, 125],
        [6000, 125],
        [7000, 150],
        [8000, 200],
        [9000, 240],
        [10000, 270],
        [11000, 300],
        [12000, 340],
        [13000, 350],
        [14000, 340],
        [15000, 330],
        [16000, 325],
        [17000, 312],
        [18000, 296.75],
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
    [1.75, 2.2],
    [1.5, 1.9],
    [1.2, 1.6],
    [1.15, 1.4],
    [1.05, 1.25],
    [0.9, 1.15],
    [0.75, 1],
)

#TODO-DANIEL
def evalLapTime(ind):
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
        ['9th Gear Ratio', ''],
        ['10th Gear Ratio', ''],
    )
    info[3][1] = ind[0]
    info[4][1] = ind[1]
    info[6][1] = ind[2]
    info[7][1] = ind[3]
    info[10][1] = ind[4]
    info[11][1] = ind[5]
    info[13][1] = ind[6]
    info[14][1] = ind[7]
    info[16][1] = ind[8]
    info[29][1] = ind[9]
    info[30][1] = ind[10]
    info[41][1] = ind[11]
    info[42][1] = ind[12]
    info[43][1] = ind[13]
    info[44][1] = ind[14]
    info[45][1] = ind[15]
    info[46][1] = ind[16]
    info[47][1] = ind[17]
    info[48][1] = ind[18]
    filename = xlsxsetup(info)
    eng.OpenVEHICLEnew(filename, nargout=0)
    return float(eng.OpenLAP(nargout=1)),

#TODO-ANDY
def cxIntermediate(ratio):
    return 0.0

#TODO-DANIEL add loop for individual genes and bounds
def mutationpower(individual):
    for i in range(0,19):
        lb = bounds[i][0]
        ub = bounds[i][1]
        gene = individual[i]
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
toolbox.register('frontal_mass', random.uniform, 0.445, 0.540)
toolbox.register('wheelbase', random.randint, 3460, 3600)
toolbox.register('lift_coef', random.uniform, -4.4, -2.8)
toolbox.register('drag_coef', random.uniform, -1.1, -0.7)
toolbox.register('aero_dist', random.uniform, 0.5, 0.7)
toolbox.register('frontal_area', random.uniform, 0.9, 1.4)
toolbox.register('disc_diameter', random.randint, 325, 330)
toolbox.register('pad_height', random.uniform, 52, 52.8)
toolbox.register('caliper_num_pistons', random.randint, 1, 6)
toolbox.register('front_stiffness', random.randint, 800, 1200)
toolbox.register('rear_stiffness', random.randint, 800, 1200)
toolbox.register('first_ratio', random.uniform, 2, 3)
toolbox.register('second_ratio', random.uniform, 1.75, 2.2)
toolbox.register('third_ratio', random.uniform, 1.5, 1.9)
toolbox.register('fourth_ratio', random.uniform, 1.2, 1.6)
toolbox.register('fifth_ratio', random.uniform, 1.15, 1.4)
toolbox.register('sixth_ratio', random.uniform, 1.05, 1.25)
toolbox.register('seventh_ratio', random.uniform, 0.9, 1.15)
toolbox.register('eight_ratio', random.uniform, 0.75, 1)

#TODO add new genes for individual representation
toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.frontal_mass,
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
toolbox.register("mate", tools.cxUniform, indpb=0.8)
toolbox.register("mutate", mutationpower)
toolbox.register("select", tools.selTournament, tournsize=2)

def main():
    random.seed()

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