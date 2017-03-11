# File to do stat runs

import matplotlib.pyplot as plt

from simulator import simulator
from coordinator import coordinator
from planner import planner
import time
import numpy as np

def statrunsNumSteps():

    num_runs = 100

    output_file = "../results/tLimited_auction.txt"

    file = open(output_file,'w')

    num_rows = 20
    row_len = 8
    num_bins = 100
    num_workers = 15
    num_bots = 8

    # 0 = greedy, 1 = auction based, 2= replanning
    coord_method = 2

    num_timestep = 300

    writeHeader(file, num_rows, row_len, num_bins, num_workers, num_bots, coord_method, num_timestep)

    file.write("percentage picked, ")
    file.write("time wasted\n")

    percent_picked = []

    for i in range(num_runs):

        sim = simulator(num_rows, row_len, num_bots, num_bins, num_workers)
        coord = coordinator(coord_method)
        plnr = planner(sim)

        for timestep in range(num_timestep):
            plan = coord.cordStep(sim)

            plan = plnr.getPlan(plan, sim)
    
            sim.step()

        percent_picked.append(sim.apples_picked / sim.total_apples * 100)
        file.write(str(sim.apples_picked / sim.total_apples * 100))
        file.write(", ")
        file.write(str(sim.wasted_time))
        file.write("\n")
        print "done running iteration: ", i
    print "mean percent picked: ", np.mean(percent_picked)
    print "std percent picked: ", np.std(percent_picked)

def statrunsTimeDone():

    num_runs = 10

    output_file = "../results/tLimited_auction.txt"

    file = open(output_file,'w')

    num_rows = 1
    row_len = 5
    num_bins = 100
    num_workers = 1
    num_bots = 2

    # 0 = greedy, 1 = auction based, 2= replanning
    coord_method = 1

    writeHeader(file, num_rows, row_len, num_bins, num_workers, num_bots, coord_method, '0')

    file.write("percentage picked, ")
    file.write("time wasted\n")

    time_done = []

    for i in range(num_runs):

        sim = simulator(num_rows, row_len, num_bots, num_bins, num_workers)
        coord = coordinator(coord_method)
        plnr = planner(sim)
        time_taken = 0

        while sim.applesLeft() != 0:
            plan = coord.cordStep(sim)

            plan = plnr.getPlan(plan, sim)
    
            sim.step()

            sim.drawSimulator()

            time_taken += 1

        time_done.append(time_taken)

        print "done running iteration: ", i
    print "mean percent picked: ", np.mean(time_done)
    print "std percent picked: ", np.std(time_done)

def writeHeader(file, num_rows, row_len, num_bins, num_workers, num_bots, coord_method, num_timestep):
    file.write("parameters\n")
    
    file.write("------------------------------------------------------------------\n")

    file.write("num_rows: ")
    file.write(str(num_rows))
    file.write("\n")

    file.write("row_len: ")
    file.write(str(row_len))
    file.write("\n")

    file.write("num_bins: ")
    file.write(str(num_bins))
    file.write("\n")

    file.write("num_workers: ")
    file.write(str(num_workers))
    file.write("\n")

    file.write("num_bots: ")
    file.write(str(num_bots))
    file.write("\n")

    file.write("coord method: ")
    file.write(str(coord_method))
    file.write("\n")

    file.write("num_timestep: ")
    file.write(str(num_timestep))
    file.write("\n")

    file.write("------------------------------------------------------------------\n")

if __name__ == '__main__':
    #statrunsNumSteps()
    statrunsTimeDone()

