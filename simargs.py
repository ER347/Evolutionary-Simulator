import numpy as np
vis = False
steps = 10000

vrange = 1
consts = {
    "repr_base_cost" : 5,
    "repr_enperc" : 0.5,
    "repr_enmin" : 0,
    "energy_idle" : 0.1,
    "energy_move" : 0.4,
    "mut_rate" : 0.2,
    "age_effect" : 1.005,
    "vrange" : vrange,
    "num_out" : 6,
    "num_in" : 1*((2*vrange+ 1)**2)+2,
    "sizex" : 100,
    "sizey" : 100,
    "recording_interval" : 10,
    "start_pop_size" : 30,
    "start_energy" : 30
}
repr_args = {
    "num" : 0,
    "pos" : [],
    "genes" : [],
    "energy" : [],
    "bloodline" : []
}
env_args = [0.7,0.07,1]
growth = np.full((consts["sizey"],consts["sizex"]),env_args[0])
growth_rate = np.full((consts["sizey"],consts["sizex"]),env_args[1])
max_growth = np.full((consts["sizey"],consts["sizex"]),env_args[2])