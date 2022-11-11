import array
import logging
import random
import numpy
from deap import algorithms
from deap import base
from deap import benchmarks
from deap import creator
from deap import tools

name = 'Formula 1 2022'
type = 'Open Wheel'
mass = 798 #kg
#frontal_mass = [0.445, 0.540]
#wheelbase = [3460mm, 3600mm]
steering_ratio = 10
#lift_coef = [-4.4, -2.8]
#drag_coef = [-1.1, --0.7]
cl_mult = 1
cd_mult = 1
#aero_dist = [0.5, 0.7]
#frontal_area = [0.9m2, 1.4m2]
air_density = 1.225 #kg/m3
#disc_diameter = [325mm, 330mm]
#pad_height = [52mm, 52.8mm]
pad_friction = 0.45
#caliper_num_pistons = [1, 6]
caliper_piston_d = 52 #mm
master_cyl_d = 32.5 #mm
pedal_ratio = 4
grip_factor = 1
tire_radius = 457 #mm
rolling_resistance = -0.001
long_fric_coef = 2
long_load_rating = 300 #kg
long_fric_sens = 0.0001
lat_fric_coef = 2
lat_load_rating = 300 #kg
lat_fric_sens = 0.0001
#front_stiffness = [800, 1200]
#rear_stiffness = [800, 1200]
power_mult = 1
thermal_eff = 0.35
fuel_heating_value = 47200000 #J/kg
drive_type = 'RWD'
shift_time = 0.01 #sec
primary_gear_eff = 1
final_gear_eff = 0.92
gearbox_eff = 0.98
primary_gear_red = 1
final_gear_red = 7
#first_ratio = [2, 3]
#second_ratio = [Prev*0.7, Prev*0.9]
#third_ratio = [Prev*0.7, Prev*0.9]
#fourth_ratio = [Prev*0.7, Prev*0.9]
#fifth_fatio = [Prev*0.7, Prev*0.9]
#sixth_ratio = [Prev*0.7, Prev*0.9]
#seventh_ratio = [Prev*0.7, Prev*0.9]
#eighth_ratio = [Prev*0.7, Prev*0.9]

#empty
#ninth_ratio
#tenth_ratio

#TODO-DANIEL
def evalLapTime():
    return 0.0

#TODO-ANDY
def cxIntermediate(ratio):
    return 0.0

#TODO-DANIEL
def mutationAdaptFeasible():
    return 0.0

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

    pop = toolbox.population(n=50)
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