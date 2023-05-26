## OpenLAP Laptime Simulation Project
#
# OpenVEHICLE
#
# Racing vehicle model file creation for use in OpenLAP and OpenDRAG
#
# This file is based on the OpenVEHICLE.m script in Micahel Halkiopoulos OpenLAP repository
# TODO insert repo link here

import pandas as pd
import numpy as np

# Moving helper functions from the bottom (standard for MATLAB) to the top (necessary for Python)

def read_torque_curve(workbookFile, sheetName=1, startRow=2, endRow=10000):

    torque_curve = pd.read_excel(workbookFile)

    return torque_curve

def read_info(workbookFile, sheetName=1, startRow=2, endRow=10000):

    info_arr = pd.read_excel(workbookFile)

    return info_arr

# Vehicle file selection

filename = 'C:\Users\dghju\Documents\GitHub\F1Evolutionary\Individuals\individual_0.xlsx'

# Reading vehicle file

info = read_info(filename, 'Info')
data = read_torque_curve(filename, 'Torque Curve')

# Getting Variables

# info
name, veh_type, M, df, L, rack, Cl, Cd, factor_Cl, factor_Cd, da, A, rho, br_disc_d, br_pad_h, br_pad_mu, br_nop, br_pist_d, br_mast_d, br_ped_r, factor_grip, tyre_radius, Cr, mu_x, mu_x_M, sens_x, mu_y, mu_y_M, sens_y, CF, CR, factor_power, n_thermal, fuel_LHV, drive, shift_time, n_primary, n_final, n_gearbox, ratio_primary, ratio_final, ratio_gearbox = read_info(filename, 'Info')
nog = 8

# HUD

[folder_status, folder_msg] = mkdir('OpenVEHICLE Vehicles')
vehname = 'OpenVEHICLE Vehicles/OpenVEHICLE_'+name+'_'+veh_type
delete(vehname+'.log')
diary(vehname+'.log')
print('OpenVEHICLE Script')
print('=====================================')
print(filename)
print('File read successfully')
print('=====================================')
print('Name: '+name)
print('Type: '+veh_type)
print('Date: '+datestr(now, 'dd/mm/yyyy'))
print('Time: '+datestr(now, 'HH:MM:SS'))
print('=====================================')
print('Vehicle generation started.')

# Brake Model

br_pist_a = br_nop*pi*(br_pist_d/1000)^2/4
br_mast_a = pi*(br_mast_d/1000)^2/4
beta = tyre_radius/(br_disc_d/2-br_pad_h/2)/br_pist_a/br_pad_mu/4
phi = br_mast_a/br_ped_r*2
print('Braking model generated successfully.')

# Steering Model

a = (1-df)*L
b = -df*L
C = 2*[CF, CF+CR;CF*a, CF*a+CR*b]
print('Steering model generated successfully.')

# Driveline Model
# TODO fix this!!
en_speed_curve = '??'
en_torque_curve = '??'
en_power_curve = en_torque_curve.*en_speed_curve*2*pi/60

wheel_speed_gear = zeros(len(en_speed_curve), nog)
vehicle_speed_gear = zeros(len(en_speed_curve), nog)
wheel_torque_gear = zeros(len(en_torque_curve), nog)

for i in range(1, nog):
    wheel_speed_gear