# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 17:12:16 2023

@author: bruno
"""
import globalPARAMETERS_GANDIGLIO as glo
import pyomo.environ as pyomo
import matplotlib.pyplot as plt

m = pyomo.ConcreteModel()

m.t = pyomo.Set(initialize=range(0, glo.time_end))
m.dt = pyomo.Set(initialize=range(0, glo.time_end+1))

m.list_load_furnace = pyomo.Param(m.t, initialize=glo.PL)

m.power_EG_buy = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)
m.power_EL_in = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)
m.power_CP_in = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)

m.power_EL_out = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)
m.power_EL_out_GB = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)
m.power_EL_out_CP = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)

m.power_GB_in = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)
m.power_GB_out = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)
m.power_GG_buy = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)
m.power_HT_in = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)
m.power_HT_out = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)

m.power_EL_rated_aux = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)
m.power_EL_rated = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)
m.optDELTA_ele = pyomo.Var(m.t, domain=pyomo.Reals, initialize=0)

m.capacity_HT = pyomo.Var(m.dt, domain=pyomo.Reals, initialize=0)



m.constraints = pyomo.ConstraintList()

for k in list(range(0, glo.time_end)):
        
    # =========================================================================
    ## eq1: POWER BALANCE NODE 1
    # ==========================================================================
    m.constraints.add(m.power_EG_buy[k] == m.power_EL_in[k] + m.power_CP_in[k])
    # =========================================================================
    ## eq2: POWER BALANCE NODE 2
    # ==========================================================================
    m.constraints.add(m.power_EL_out[k] == m.power_EL_out_GB[k] + m.power_EL_out_CP[k])
    # =========================================================================
    ## eq3: POWER BALANCE NODE 3
    # ==========================================================================
    m.constraints.add(m.power_GB_in[k] == m.power_GG_buy[k] + m.power_EL_out_GB[k] + m.power_HT_out[k])
    # =========================================================================
    ## eq6: POWER LIMIT at ELECTROLYSER
    # ==========================================================================
    #m.constraints.add(pyomo.inequality(0.10*m.power_EL_rated_aux[k], m.power_EL_in[k],1*m.power_EL_rated_aux[k]))
    # =========================================================================
    ## eq7: EFFICIENCY at ELECTROLYSER
    # ==========================================================================
    m.constraints.add(m.power_EL_out[k] == glo.efficiency_ele*m.power_EL_in[k])
    # =========================================================================
    ## eq8: DELTA LINEARIZATION at ELECTROLYSER
    # ==========================================================================
    m.constraints.add(m.power_EL_rated_aux[k] == m.power_EL_rated[k]*m.optDELTA_ele[k])
    # =========================================================================
    ## eq9: LINEARIZATION condition
    # ==========================================================================
    m.constraints.add(m.power_EL_rated_aux[k] <= m.power_EL_rated[k]* - (1 - m.optDELTA_ele[k])*glo.power_EL_rated_min)
    # =========================================================================
    ## eq10: LINEARIZATION condition
    # ==========================================================================
    m.constraints.add(m.power_EL_rated_aux[k] >= m.power_EL_rated[k]* - (1 - m.optDELTA_ele[k])*glo.power_EL_rated_max)
    # =========================================================================
    ## eq11: LINEARIZATION condition
    # ==========================================================================
    m.constraints.add(m.power_EL_rated_aux[k] <= glo.power_EL_rated_max*m.optDELTA_ele[k])
    # =========================================================================
    ## eq12: LINEARIZATION condition
    # ==========================================================================
    m.constraints.add(m.power_EL_rated_aux[k] >= glo.power_EL_rated_min*m.optDELTA_ele[k])
    # =========================================================================
    ## eq13: POWER required by the COMPRESSOR
    # ==========================================================================
    m.constraints.add(m.power_CP_in[k] == m.power_EL_out_CP[k]*glo.compression_work / glo.LHV_h2)                  
    # =========================================================================
    ## eq14: POWER BALANCE pot of the electrolyser
    # ==========================================================================
    m.constraints.add(m.power_EL_out_CP[k] == m.power_HT_in[k])
    # =========================================================================
    ## eq15: HYDROGEN TANK ENERGY BALANCE
    # ==========================================================================
    m.constraints.add(m.capacity_HT[k+1] == m.capacity_HT[k] + m.power_HT_in[k] - m.power_HT_out[k])
    # =========================================================================
    ## eq16: HYDROGEN TANK Initial condition
    # ==========================================================================
    m.constraints.add(m.capacity_HT[0] == glo.capacity_HT_rated * 0.90)
    # =========================================================================
    ## eq18: ENERGY BALANCE in the STORAGE TANK : CAPACITY CONSTRAINT
    # ==========================================================================
    m.constraints.add(glo.perc_min_ht * glo.capacity_HT_rated <= m.capacity_HT[k])          # we have to consider the E[k+1] or E[k]?
    m.constraints.add(m.capacity_HT[k] <= glo.perc_max_ht * glo.capacity_HT_rated)       
    # =========================================================================
    ## eq19: BURNER EFFICIENCY
    # ==========================================================================
    m.constraints.add(m.power_GB_out[k] == glo.efficiency_bur*m.power_GB_in[k])
    # =========================================================================
    ## eq20: BURNER BALANCE: constraint on POWER AT INLET
    # ==========================================================================
    m.constraints.add(glo.perc_min_bur*glo.power_bur_rated <= m.power_GB_in[k])
    m.constraints.add(m.power_GB_in[k] <= glo.perc_max_bur*glo.power_bur_rated)
    # =========================================================================
    ## eq21: POWER BALANCE: LOAD CONSTRAINT
    # ==========================================================================
    m.constraints.add(m.power_GB_out[k] == m.list_load_furnace[k])
    
def obj_func(m):
    CAPEX_EL_tot = sum(m.power_EL_out[kk]*glo.CAPEX_ele for kk in m.t)
    OPEX_EL_tot = sum(m.power_EL_out[kk]*glo.CAPEX_ele for kk in m.t)
    
    return 
    
m.obj = pyomo.Objective(rule=obj_func, sense=pyomo.minimize)
instance = m.create_instance()
opt = pyomo.SolverFactory('gurobi')
result = opt.solve(instance)
result.write()



# ===============================================================================================================================================
## # STORE the values model.optimization
# ===============================================================================================================================================
pow_ele = []
for ii in m.t:
    pow_ele.append(pyomo.value(m.power_EL_out[ii]))
        
plt.plot(m.t, pow_ele)
print('Result from OPTIMIZATION FUNCTION = ', m.obj())   

    
    
              
    
    
    