import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
import math


"""What do we have:
    We take our prior states, use the laser readings and calculate the new ones
    p is determined by the distance of the laser reading 
    Each point have a probability"""
data_coin_flips = np.random.randint(2, size=1000)

params = np.linspace(0, 1, 100)
p_x = [np.product(st.bernoulli.pmf(data_coin_flips, p)) for p in params]
plt.scatter(params, p_x)
print(p_x)
print(params)
#plt.axis([-min(params), min(params), -min(p_x), max(p_x)])
#plt.show()

grid_size = 10
grid = np.array([[0.5 for col in range(grid_size)] for row in range(grid_size)])
print(grid)


class Bayesian():

    #Region
    def __init__(self, grid):
        self.R = 30
        self.grid = 0
        self.beta = 0.5
        self.accuracy = 0.01
        """
        self.R = 10 #Typ 30
        self.grid = 0
        self.beta = 15#math.radians(0.5)
        self.accuracy = 0.01
        """

    def regions(self, alpha, r):

        if r < (self.R - self.accuracy):
            self.region = 2

    # P(s|Empty)
    def empty(self, r, alpha):
        a = (self.R - r)/self.R
        b = (self.beta - abs(alpha))/self.beta
        return (a + b)/2

    #P(s|Occupied)
    def occupied(self, alpha, r):
        return 1 - self.empty(alpha, r)

    def bayes_rule(self, s, H):
        # P(Occupied | s) = P(s|Occupied)*P(Occupied)/(P(s|Occupied)*P(Occupied) + P(s|!Occupied)*P(!Occupied))
        # P(Occupied, s) = P(s,Occupied)*P(Occupied)/(P(s,Occupied)*P(Occupied) + P(s,!Occupied)*P(!Occupied))
        PsH = P.conditioned(s, H) * P.probability(H)
        PH =  P.probability(H)

        return PsH*PH/(PsH*PH + (1-PsH)*(1-PH) )

    def probability(self):
        pass

    def conditioned(self):
        pass

    def region_divider(self,cells):
        region = None

        if d_cell > d_laser:
            return None

        if d_laser > d_cell:
            region = 1

        """
        P = Bayesian(grid)

        P.conditioned(laser_reading, occupied)
        P.conditioned(laser_reading, empty)
        P.probability(occupied)
        P.probability(empty)

        # P(s|H)P(H)
        # P(H|s):
        P.bayes_rule()

        print("bayesian", P.empty(3.5, math.radians(0)))
        print("bayesian", P.occupied(3.5, math.radians(0)))
        print("Total prob", P.empty(3.5, math.radians(0)) + P.occupied(3.5, math.radians(0)))
        """