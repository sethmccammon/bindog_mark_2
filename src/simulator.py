
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import random


class simulator(object):
  """docstring for simulator"""
  def __init__(self, num_rows, row_size, num_bots, num_bins, num_workers):
    #random init

    self.num_rows = num_rows
    self.row_size = row_size


    self.workers = []
    self.bots = {}
    self.bins = {}

    for ii in range(num_workers):
      worker_loc = [random.randint(0, num_rows-1), random.randint(0*row_size)]
      self.workers.append(workerGroup(worker_loc))

    for ii in range(num_bots):
      #where should the robots start?
      bot_loc = [1, 0]
      self.bots[ii] = bindog(bot_loc)

    for ii in range(num_bins):
      bin_loc = [0, 0]
      self.bins[ii] = orchardBin(bin_loc)


  def drawSimulator(self):
    scale = 10
    img_size = [(num_rows*2+1)*scale, row_size+2*scale]
    fig1 = plt.figure()
    ax1 = plt.gca()
    # axes.se

    plt.xlim((-.5, (num_rows*2+.5)))
    plt.ylim((-.5, row_size+1.5))
    #ax1 = fig1.add_subplot(111, aspect='equal')

    for row in range(0, num_rows*2+1, 2):
      for col in range(1, row_size+1):
        ax1.add_patch(patches.Rectangle((row-.5, col-.5), 1., 1., facecolor="#228b22"))
        plt.plot(row, col, 'go')

    for bot in self.bots:
      loc = self.bots[bot].loc
      ax1.add_patch(patches.Rectangle((loc[0]-.25, loc[1]-.25), .5, .5, facecolor="#7b9095"))

    plt.show()





  def step():
    for worker in self.workers:
      local_bin = bins[worker.loc]
      worker.pickFruit()
      #bot takes an action
      self.moveBot



class bindog(object):
  """docstring for bindog"""
  def __init__(self, loc):
    self.loc = loc
    self.status = "idle" #robot starts idle
    self.bin = None #Robot Starts with No Bin

  def takeAction(self, action):
    if action == "GOTO":
      return 0
    elif action == "PICK_UP":
      return 0
    elif action == "PUT_DOWN":
      return 0
    else:
      return 0

  def getBin(self, loc, orchardBin):
    if self.loc == orchardBin.loc and self.bin is None:
      self.bin = orchardBin

  def dropBin(self):
    if self.bin is not None:
      self.bin = None

  def moveBot(self, new_loc):
    action = [1, 0] #dummy action is to go north
    self.loc = self.loc + action # need to define action
    if self.bin is not None:
      self.bin.loc = self.loc




class orchardBin(object):
  """docstring for orchardBin"""
  def __init__(self, loc, capacity = 0.0):
    self.loc = loc
    self.capacity = 0.0 #Default bin is empty



class workerGroup(object):
  """docstring for workerGroup"""
  def __init__(self, loc, rate):
    self.loc = loc

  def pickFruit(self, orchardBin):
    if self.loc == orchardBin.loc:
      orchardBin.capacity += .1 * random.random() #randomly fill up to 10% of a bin
      orchardBin.capacity = min(100.0, orchardBin.capacity)

    
    
    
    
if __name__ == '__main__':
  num_rows = 5
  row_size = 5
  num_bots = 1
  num_bins = 0
  num_workers = 0
  sim = simulator(num_rows, row_size, num_bots, num_bins, num_workers)
  sim.drawSimulator()