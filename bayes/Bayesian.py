

class Bayesian:
    def __init__(self, prob_grid):
        self.prob_grid = prob_grid
        self.maximum_range = 30
        self.beta = 0.5 #Half lobe angle
        self.accuracy = 0.01

    def bayes_handler(self, bresenham_lines):

        for i in range(0, len(bresenham_lines)):
            #print(bresenham_lines[i][0], ',' , end = '')
            #print(bresenham_lines[i][1])
            #self.bayes_rule(bresenham_lines[i][0], bresenham_lines[i][1])

            s = bresenham_lines[len(bresenham_lines)-1]
            self.bayes_rule(s, bresenham_lines[i])

    def bayes_rule(self, sensor_cell, cell):
        # P(Occupied | s) = P(s|Occupied)*P(Occupied)/(P(s|Occupied)*P(Occupied) + P(s|!Occupied)*P(!Occupied))
        # P(Occupied, s) = P(s,Occupied)*P(Occupied)/(P(s,Occupied)*P(Occupied) + P(s,!Occupied)*P(!Occupied))
        r = sensor_cell

        print(self.probability(cell))
        print("regionII_empty along y, x constant", self.regionII_empty(cell[1], 0))
        print("regionI_occupied along y, x constant", self.regionI_occupied(cell[1], 0))
        #print(self.empty(cell[0], 0))
        #PsH = self.occupied(s, cell) * self.probability(cell)
        #PH =  self.probability(cell)
        #return PsH*PH/(PsH*PH + (1-PsH)*(1-PH))

    # P(s|Empty)
    def regionII_empty(self, r, alpha):
        a = (self.maximum_range - r)/self.maximum_range
        b = (self.beta - abs(alpha))/self.beta
        return (a + b)/2

    def regionI_occupied(self, r, alpha):
        a = (self.maximum_range - r)/self.maximum_range
        b = (self.beta - abs(alpha))/self.beta
        return ((a + b)/2)*0.98

    #P(s|Occupied)
    def occupied(self, r, alpha):
        return 1 - self.empty(alpha, r)

    def probability(self, cell):
        return self.prob_grid[cell[0]][cell[1]]

###########################
    def regions(self, r, alpha):

        if r < (self.R - self.accuracy):
            self.region = 2