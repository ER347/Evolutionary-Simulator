import agentpy as ap
import numpy as np
from simfuncs import *
rng = np.random.default_rng(12345)
class Organism(ap.Agent):
    def agent_setup(self,consts):
        genes_rand = 2*rng.random((consts["num_out"],consts["num_in"]))-1
        self.genes = genes_rand/magnitude(genes_rand)
        self.bloodline = self.id
        self.dead = False
        self.energy = consts["start_energy"]
        self.age = 0
        self.age_mult = 1

    def agent_step(self,consts):    
        self.pos = self.model.plane.positions[self]
        self.energy += self.model.plane.growth[self.pos[0],self.pos[1]]-consts["energy_idle"]
        self.model.plane.growth[self.pos[0],self.pos[1]] = 0
        in_growth = []
        for y in range(self.pos[0]-consts["vrange"],consts["vrange"]+1+self.pos[0]):
            for x in range(self.pos[1]-consts["vrange"],self.pos[1]+consts["vrange"]+1):
                in_growth.append(self.model.plane.growth[y%consts["sizey"],x%consts["sizex"]])
        self.inp = np.concatenate((in_growth,self.energy/10,1),axis=None)
        self.inp = np.reshape(self.inp,(len(self.inp),1))
        self.res = np.matmul(self.genes,self.inp)

        mpx = out_norm(self.res[0,0])
        mnx = out_norm(self.res[1,0])
        mpy = out_norm(self.res[2,0])
        mny = out_norm(self.res[3,0])
        repr_weight = out_norm(self.res[4,0])
        sleep = out_norm(self.res[5,0])

        if self.energy < consts["repr_enmin"]:
            repr_weight = 0

        sumout = mpx+mnx+mpy+mny+repr_weight+sleep
        self.vel = (0,0)
        reproduce = False
        if sumout != 0:
            probabilities = np.array([mpx,mnx,mpy,mny,repr_weight,sleep])/sumout
            rand = rng.choice([0,1,2,3,4,5], p = probabilities)
        
            if rand == 0:
                self.vel = (0,1)
            elif rand == 1:
                self.vel = (0,-1)
            elif rand == 2:
                self.vel = (1,0)
            elif rand == 3:
                self.vel = (-1,0)
            elif rand == 4:
                reproduce = True

        if self.vel != (0,0):
            self.energy -= consts["energy_move"]*self.age_mult
            self.age_mult *= consts["age_effect"]
            self.model.plane.move_by(self,self.vel)

        if reproduce:
            self.model.repr_args["num"] += 1
            self.model.repr_args["pos"].append(self.pos)
            self.model.repr_args["genes"].append(self.genes)
            self.model.repr_args["energy"].append((self.energy-consts["repr_base_cost"])*consts["repr_enperc"])
            self.model.repr_args["bloodline"].append(self.bloodline)
            self.energy = (self.energy-consts["repr_base_cost"])*(1-consts["repr_enperc"])
            
        if self.energy <= 0:
            self.dead = True
            
        self.age += 1

    def mutate(self,consts):
        mutations = (rng.random((consts["num_out"],consts["num_in"]))-0.5)* consts["mut_rate"]
        self.genes = self.genes+mutations*np.abs(mutations)
        self.genes /= magnitude(self.genes)