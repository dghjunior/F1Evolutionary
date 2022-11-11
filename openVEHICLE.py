from scipy.io import savemat

## Initialize vectors of data
info = ['Formula 1', 'Open Wheel', 650, 45, 3000, 10, -4.8, -1.2, 1, 1, 50, 1, 1.225, 
    250, 40, 0.45, 6, 40, 25, 4, 1, 330, -0.001, 2, 250, 0.0001, 2, 250, 0.0001, 800, 
    1000, 1, 0.35, 4.72E+07, 'RWD', 0.01, 1, 0.92, 0.98, 1, 7, 2.57, 2.11, 1.75, 1.46, 
    1.29, 1.13, 1, 0, 0, 0]
torque_curve = [125, 125, 125, 125, 125, 125, 150, 200, 240, 270, 300, 340, 350, 340,
    330, 325, 312, 296.75]
i = 0;
f1dict = {}

# info about car
f1dict["name"] = info[i]; i = i + 1
f1dict["car_type"] = info[i]; i = i + 1
f1dict["M"] = info[i]; i = i + 1 #[kg]
f1dict["df"] = info[i]; i = i + 1 #[-]
f1dict["L"] = info[i]; i = i + 1
f1dict["rack"] = info[i]; i = i + 1 #[-]
f1dict["Cl"] = info[i]; i = i + 1 #[-]
f1dict["Cd"] = info[i]; i = i + 1 #[-]
f1dict["factor_C1"] = info[i]; i = i + 1  #[-]
f1dict["factor_Cd"] = info[i]; i = i + 1  #[-]
f1dict["da"] = info[i]; i = i + 1  #[-]
f1dict["A"] = info[i]; i = i + 1  #[m2]
f1dict["rho"] = info[i]; i = i + 1  #[kg/m3]
f1dict["br_disc_d"] = info[i]; i = i + 1  #[m]
f1dict["br_pad_h"] = info[i]; i = i + 1  #[m]
f1dict["br_pad_mu"] = info[i]; i = i + 1  #[m]
f1dict["br_nop"] = info[i]; i = i + 1  #[m]
f1dict["br_pist_d"] = info[i]; i = i + 1  #[m]
f1dict["br_mast_d"] = info[i]; i = i + 1  #[m]
f1dict["br_ped_r"] = info[i]; i = i + 1  #[m]
f1dict["factor_grip"] = info[i]; i = i + 1  #[-]
f1dict["tyre_radius"] = info[i]; i = i + 1  #[m]
f1dict["Cr"] = info[i]; i = i + 1  #[-]
f1dict["mu_x"] = info[i]; i = i + 1  #[-]
f1dict["mu_x_M"] = info[i]; i = i + 1  #[1/kg]
f1dict["sens_x"] = info[i]; i = i + 1  #[-]
f1dict["mu_y"] = info[i]; i = i + 1  #[-]
f1dict["mu_y_M"] = info[i]; i = i + 1  #[]1/kg
f1dict["sens_y"] = info[i]; i = i + 1  #[]-
f1dict["CF"] = info[i]; i = i + 1  #[N/deg]
f1dict["CR"] = info[i]; i = i + 1  #[N/deg]
f1dict["factor_power"] = info[i]; i = i + 1 
f1dict["n_thermal"] = info[i]; i = i + 1 
f1dict["fuel_LHV"] = info[i]; i = i + 1  #[J/kg]
f1dict["drive"] = info[i]; i = i + 1 
f1dict["shift_time"] = info[i]; i = i + 1  #[]
f1dict["n_primary"] = info[i]; i = i + 1 
f1dict["n_final"] = info[i]; i = i + 1 
f1dict["n_gearbox"] = info[i]; i = i + 1 
f1dict["ratio_primary"] = info[i]; i = i + 1 
f1dict["ratio_final"] = info[i]; i = i + 1 
f1dict["fation_gearbox"] = info[i]; i = i + 1 

print(f1dict)
savemat("f1_py_test.mat", f1dict)