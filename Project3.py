import math
import matplotlib.pyplot as plt
import dynamics


class Project3(dynamics.Dynamics):
    def __init__(self, grassBirth, grassDeath, insectBirth, insectDeath, pesticideDecay, grassPesticideRate, insectPesticideRate, time_step):
        numEquations = 3                            # set the number of state equations

        # set constants
        self.grassInc = grassBirth
        self.grassDec = grassDeath
        self.insectInc = insectBirth
        self.insectDec = insectDeath
        self.pesticideRate = pesticideDecay
        self.grassRate = grassPesticideRate
        self.insectRate = insectPesticideRate

        super().__init__(numEquations, time_step)   # initialize super class dynamics (Euler Method)

        # create variables to hold the state history for plotting
        self.Q = [[] for i in range(numEquations)]
        self.T = []

    def initialize(self, grassWeight, insectWeight, pesticideWeight):
        # set state variable initial values
        self.q[0] = grassWeight
        self.q[1] = insectWeight
        self.q[2] = pesticideWeight
        # initialize state history used for plotting
        self.Q = [[self.q[i]] for i in range(len(self.q))]
        self.T = [0.0]

    def advance(self, count):
        # compute "count" updates of the state equations
        for i in range(count):
            # self.dq[0] = (self.grassInc * self.q[0]) - (self.grassDec * self.q[0] * self.q[1])
            # self.dq[1] = (self.insectInc * self.q[0] * self.q[1]) - (self.insectDec * self.q[1])
            self.dq[0] = (self.grassInc * self.q[0]) - (self.grassDec * self.q[0] * self.q[1]) - (self.grassRate * self.q[0] * self.q[2])
            self.dq[1] = (self.insectInc * self.q[0] * self.q[1]) - (self.insectDec * self.q[1]) - (self.insectRate * self.grassRate * self.q[1] * self.q[2])
            self.dq[2] = -self.pesticideRate
            if (self.q[2] < 0):
                self.q[2] = 0
            self.step()
        # save the updated state variables after the "count" updates for plotting
        [self.Q[i].append(self.q[i]) for i in range(len(self.q))]
        self.T.append(self.now())

    def print(self):
        # custom print for current simulation
        print('time={0:10f} grass={1:10f} insect={2:10f}'.format(self.time, self.q[0], self.q[1]))

    def plot(self):
        # custom plot for current simulation
        plt.figure()
        plt.subplot(411)
        plt.plot(self.T, self.Q[0], 'g')
        plt.ylabel('grass')

        plt.subplot(412)
        plt.plot(self.T, self.Q[1], 'r--')
        plt.ylabel('insect')

        plt.subplot(413)
        plt.plot(self.T, self.Q[2], 'k')
        plt.ylabel('pesticide')

        plt.subplot(414)
        plt.plot(self.T, self.Q[0], 'g', self.T, self.Q[1], 'r--')
        plt.ylabel('grass - insect')
        plt.xlabel('time')

        plt.figure()
        plt.plot(self.Q[0], self.Q[1], 'b')
        plt.ylabel('grass')
        plt.xlabel('insect')

        plt.show()


# set parameters for Predator-Pray simulation

# parameters describing the simulation time
endTime = 1000.0       # length of simulation (i.e. end time)
dt = 0.01             # time step size used to update state equations

# parameters describing the real system
grassBirth = 0.05
grassDeath = 0.001
insectBirth = 0.0005
insectDeath = 0.01
pesticideDecay = 0.01
grassPesticideRate = 0.001
insectPesticideRate = 0.9
initialGrass = 150.0
initialInsect = 50.0
initialPesticide = 25.0

# create the simulation and initialize state variables
P = Project3(grassBirth, grassDeath, insectBirth, insectDeath, pesticideDecay, grassPesticideRate, insectPesticideRate, dt)
P.initialize(initialGrass, initialInsect, initialPesticide)

# run the simulation
displayInterval = 1         # number of state updates before saving state
while P.now() < endTime:
    P.advance(displayInterval)
    P.print()               # call print to see numeric values of state per display interval

P.plot()                    # call custom plot
