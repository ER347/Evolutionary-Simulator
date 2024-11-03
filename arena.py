import agentpy as ap
import numpy as np
import random
from agent import *
from simfuncs import *
class Arena(ap.Model):
    def setup(self,consts,repr_args,growth,growth_rate,max_growth):
        self.random = random.Random(12345)
        self.nprandom = np.random.default_rng(98765)
        pop_start = ap.AgentList(self,consts["start_pop_size"],Organism)
        self.plane = ap.Grid(self,(consts["sizey"],consts["sizex"]),torus=True)
        self.plane.add_agents(pop_start,random=True)
        self.plane.add_field('growth',growth)
        self.plane.add_field('growth_rate',growth_rate)
        self.plane.add_field('max_growth',max_growth)
        self.repr_args = repr_args
        self.t = 0
        self.agents = self.plane.agents.to_list()
        self.agents.agent_setup(consts)
        self.save_data()
            
    def step(self,consts):
        self.agents = self.plane.agents.to_list()

        self.plane.growth += self.plane.growth_rate
        self.plane.growth = np.clip(self.plane.growth,a_min=None,a_max=self.plane.max_growth)

        self.agents.agent_step(consts)
        
        if self.repr_args["num"] != 0:
            new_agents = ap.AgentList(self, self.repr_args["num"],Organism)
            new_agents.pos = ap.AttrIter(self.repr_args["pos"])
            new_agents.genes = ap.AttrIter(self.repr_args["genes"])
            new_agents.energy = ap.AttrIter(self.repr_args["energy"])
            new_agents.bloodline = ap.AttrIter(self.repr_args["bloodline"])
            new_agents.dead = False 
            new_agents.age = 0
            new_agents.age_mult = 1
            new_agents.mutate(consts)
            self.plane.add_agents(new_agents,new_agents.pos)
            self.repr_args["num"] = 0
            self.repr_args["pos"].clear()
            self.repr_args["genes"].clear()
            self.repr_args["energy"].clear()
            self.repr_args["bloodline"].clear()
        dead_agents = self.agents.select(self.agents.dead)
        if len(dead_agents) != 0:
            self.plane.remove_agents(dead_agents)
        self.t +=1
        self.save_data()
        
    def save_data(self):
        self.agents = self.plane.agents.to_list()
        if self.t%consts["recording_interval"] == 0:
            self.population = len(self.agents)
            self.record('population',self.population)
            if self.population > 0:
                avg_age_mult = 0
                for x in range(len(self.agents)):
                    avg_age_mult += self.agents[x].age_mult
                avg_age_mult /= len(self.agents)
                self.record('avg_age_mult',avg_age_mult)
                avg_gene = np.copy(self.agents[0].genes)
                for x in range(1,len(self.agents)):
                    avg_gene += self.agents[x].genes
                avg_gene /= len(self.agents)
                avg_gene = avg_gene/magnitude(avg_gene)
                gen_var = 0
                for x in range(len(self.agents)):
                    gen_var += angle(self.agents[x].genes,avg_gene)
                gen_var /= len(self.agents)
                self.record('gen_var',gen_var)
                self.record('max_energy',max(self.agents.energy))

            self.record('num_bloodlines',len(np.unique(self.agents.bloodline)))