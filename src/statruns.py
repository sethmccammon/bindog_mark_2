# File to do stat runs

import matplotlib.pyplot as plt

from simulator import simulator
from coordinator import coordinator
from planner import planner
import time

def statruns():

    num_runs = 100

    output_file = "../results/tLimited_auction.txt"

    file = open(output_file,'w')

    num_rows = 5
    row_len = 5
    num_bins = 30
    num_workers = 4
    num_bots = 2

    # 0 = greedy, 1 = auction based
    coord_method = 1

    num_timestep = 200

    writeHeader(file, num_rows, row_len, num_bins, num_workers, num_bots, coord_method, num_timestep)

    file.write("percentage picked, ")
    file.write("time wasted\n")

    for i in range(num_runs):

        sim = simulator(num_rows, row_len, num_bots, num_bins, num_workers)
        coord = coordinator(coord_method)
        plnr = planner(sim)

        for timestep in range(num_timestep):
            plan = coord.cordStep(sim)

            plan = plnr.getPlan(plan, sim)
    
            sim.step()

        file.write(str(sim.apples_picked / sim.total_apples * 100))
        file.write(", ")
        file.write(str(sim.wasted_time))
        file.write("\n")
        print "done running iteration: ", i

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
    statruns()

