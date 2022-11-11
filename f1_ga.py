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
#frontal_mass
#wheelbase
steering_ratio = 10
#lift_coef
#drag_coef
cl_mult = 1
cd_mult = 1
#aero_dist
#frontal_area
air_density = 1.225 #kg/m3
#disc_diameter
#pad_height
pad_friction = 0.45
#caliper_num_pistons
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
#front_stiffness
#rear_stiffness
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
#first_ratio
#second_ratio
#third_ratio
#fourth_ratio
#fifth_fatio
#sixth_ratio
#seventh_ratio
#eighth_ratio

#empty
#ninth_ratio
#tenth_ratio


creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("attr_float", random.uniform, -5, 5)

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 3)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def checkBounds(min, max):
    def decorator(func):
        def wrappper(*args, **kargs):
            offspring = func(*args, **kargs)
            for child in offspring:
                for i in range(len(child)):
                    if child[i] > max:
                        child[i] = max
                    elif child[i] < min:
                        child[i] = min
            return offspring
        return wrappper
    return decorator

toolbox.register("evaluate", benchmarks.kursawe)
toolbox.register("mate", tools.cxBlend, alpha=1.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=3, indpb=0.3)
toolbox.register("select", tools.selNSGA2)

toolbox.decorate("mate", checkBounds(-5, 5))
toolbox.decorate("mutate", checkBounds(-5, 5))

def main():
    random.seed(64)

    MU, LAMBDA = 50, 100
    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    algorithms.eaMuPlusLambda(pop, toolbox, mu=MU, lambda_=LAMBDA, 
                              cxpb=0.5, mutpb=0.2, ngen=150, 
                              stats=stats, halloffame=hof)

    return pop, stats, hof