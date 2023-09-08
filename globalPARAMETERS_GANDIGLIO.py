# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 17:17:23 2023

@author: bruno
"""

import pandas
from scipy.io import loadmat

#====================================================================
## TIME DATA for the code
#====================================================================
time_end = 8760                                                                      # [h]
time_vec = list(range(0, time_end))
life = 20

mat= loadmat('thermalload_momo_new.mat')
mat= loadmat('PL.mat')
PL = mat['PL']
PL = PL.reshape((-1))
PL = PL[0:time_end]

efficiency_ele = 0.65  
power_EL_rated_min = 0
power_EL_rated_max = 1e6 

specific_work_cp = 4                                                                    # [MJ/kgH2]
compression_work = specific_work_cp * 1000 / 3600                                       # [kWh/kgH2] = [MJ/kgH2] * [kWh/MJ] 
LHV_h2 = 33.33                                                                             # [kWh/kg]

capacity_HT_rated = 1000            #[kWh]
perc_min_ht = 10            #assumed
perc_max_ht = 90            #assumed

efficiency_bur = 98
perc_min_bur = 0
perc_max_bur = 1
power_bur_rated = 1e6       #assumed

LHV_h2 = 33.33                                                                             # [kWh/kg]
density_h2 = 0.0899                                                                     # [kg/m3]
density_h2o = 1000                                                                    # [kg/m3]
ECI = 166         
discount_rate = 0.04
#====================================================================
cost_energy_grid = 0.2966                                                               # [€/kWh] https://electricityinspain.com/electricity-prices-in-spain/
#====================================================================
## ELECTROLYSER
#====================================================================
CAPEX_ele = 1188                                                                        # [€/kWe]  https://www.iea.org/reports/electrolysers + Marocco Gandiglio
OPEX_ele = 15.84                                                                        # [€/kWe/year]  Marocco Gandiglio
INSTALL_ele = CAPEX_ele*0.1                                                             # [€/kWe/year]  Marocco Gandiglio
REPLACE_ele = CAPEX_ele*0.35                                                            # [€/kWe/year]  Marocco Gandiglio
power_EL_rated = 1000                                                                   # [€/kW]
flow_rate_rated_ELE = power_EL_rated*1000/LHV_h2/3600                                  # [kg/s] = [MW] / [kWh/kg]
#====================================================================
## HYDROGEN COMPRESSOR
#====================================================================
specific_work_cp = 4                                                                    # [MJ/kgH2]
compression_work = specific_work_cp * 1000 / 3600                                       # [kWh/kgH2] = [MJ/kgH2] * [kWh/MJ] 
CAPEX_cp = 1600                                                                         # [€/kWe/year]  Marocco Gandiglio
OPEX_cp_USD = 19                                                                        # [USD/kW] https://emp.lbl.gov/publications/benchmarking-utility-scale-pv
OPEX_cp = OPEX_cp_USD / 0.92                                                            # [€/kWe]
power_rated_CP = compression_work*1000/1                                                # [kW] = [kWh]/[h]
#====================================================================
## HYDROGEN STORAGE TANK
#====================================================================
loh_ht = 0.75
perc_max_ht = 0.9                                                                       # [-] [MOMO]
perc_min_ht = 0.1                                                                       # [-] [MOMO]
capacity_ht_rated = 11.2e3                                                              # [kWh]             A CASOO     https://core.ac.uk/download/pdf/11653831.pdf
CAPEX_ht = 470                                                                          # [€/kgH2/year]  Marocco Gandiglio
OPEX_ht = OPEX_ele*0.02                                                                 # [€/kgH2/year]  Marocco Gandiglio
#====================================================================
## HYDROGEN BOTTLE TANK
#====================================================================
capacity_volume_bo = 850                                                                # [liters] https://www.mahytec.com/wp-content/uploads/2021/03/CL-DS10-Data-sheet-60bar-850L-EN.pdf
capacity_bo_rated = capacity_volume_bo / 1000 * density_h2 * LHV_h2                        # [kWh] = [litri] * [m3/l] * [kg/m3] * [kWh/kg]
CAPEX_bo = 470/2                                                                        # [€/kgH2/year] like the storage: MOMO said to reduce it so it is dividd by two
OPEX_bo = OPEX_ele*0.02                                                                 # [€/kgH2/year] like the storage:
#====================================================================
## BURNER
#====================================================================
efficiency_bur = 0.98                                                                   # [-] Marocco Gandiglio
perc_max_bur = 1                                                                        # [-] Marocco Gandiglio
perc_min_bur = 0                                                                        # [-] Marocco Gandiglio
power_bur_rated = 7500                                                                  # [kW] a caso (?)
CAPEX_bur = 63.32                                                                       # [€/kWth/year]  Marocco Gandiglio
OPEX_bur = CAPEX_bur*0.05      