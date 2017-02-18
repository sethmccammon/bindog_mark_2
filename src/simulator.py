
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import random


class simulator(object):
  """docstring for simulator"""
  def __init__(self, num_rows, row_size, num_bots, num_bins, num_workers):
    #random init

    self.num_rows = num_rows
    self.row_size = row_size

    self.orchard_map = None

    self.wkrs = {}
    self.bots = {}
    self.bins = {}

    self.num_bins = num_bins
    self.collected_bins = 0
    self.profit = 0


    # for ii in range(num_wkrs):
    while len(self.wkrs) < num_wkrs:
      worker_loc = [random.randint(0, num_rows-1)*2+1, 1+random.randint(0, row_size-1)]
      for worker in self.wkrs:
        if worker_loc == self.wkrs[worker].loc:
          break
      else:
        self.wkrs[len(self.wkrs)] = workerGroup(worker_loc)

    for ii in range(num_bots):
      #where should the robots start?
      bot_loc = [0, 0]
      self.bots[ii] = bindog(bot_loc)

    for ii, worker in enumerate(self.wkrs):
      self.bins[ii] = orchardBin(self.wkrs[worker].loc)




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
      drawBindog(ax1, self.bots[bot])

    for worker in self.wkrs:
      loc = self.wkrs[worker].loc
      ax1.add_patch(patches.Rectangle((loc[0]-.45, loc[1]-.45), .9, .9, facecolor="#c0ffee"))

    for bin in self.bins:
      drawBin(ax1, self.bins[bin])

    plt.show()


  def getIdleBots(self):
    # Function which returns a list of idle robots in the simulator
    idle_bots = []

    for key, item in self.bots.iteritems():
      if item.status == "idle":
        idle_bots.append(key)

    return idle_bots


  def getBinPickupRequests(self):
    res = []

    for worker in self.wkrs:
      if self.wkrs[worker].pickup:
        res.append(self.wkrs[worker.loc])

    return res


  def getBinDeliveryRequests(self):
    res = []

    for worker in self.wkrs:
      if self.wkrs[worker].delivery:
        res.append(self.wkrs[worker.loc])
        
    return res


def drawBin(ax1, bin_in):
  loc = bin_in.loc
  ax1.add_patch(patches.Rectangle((loc[0]-.3, loc[1]-.3), .6, .6, facecolor="purple"))

def drawBindog(ax1, bot):
  loc = bot.loc
  ax1.add_patch(patches.Rectangle((loc[0]-.25, loc[1]-.25), .5, .5, facecolor="#7b9095"))
  ax1.add_patch(patches.Circle((loc[0]-.25, loc[1]-.25), .1, color='k'))
  ax1.add_patch(patches.Circle((loc[0]+.25, loc[1]-.25), .1, color='k'))
  if bot.bin is not None:
    ax1.add_patch(patches.Rectangle((loc[0]-.2, loc[1]-.2), .4, .4, facecolor="k"))




class cell(object):
  """docstring for cell"""
  def __init__(self, arg):
    super(cell, self).__init__()
    self.arg = arg
    




class bindog(object):
  """docstring for bindog"""
  def __init__(self, loc):
    self.loc = loc
    self.status = "idle" #robot starts idle
    self.target = None #Default no target
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
  def __init__(self, loc):
    self.loc = loc
    self.pickup = False
    self.delivery = False

  def pickFruit(self, orchardBin):
    if self.loc == orchardBin.loc:
      orchardBin.capacity += .1 * random.random() #randomly fill up to 10% of a bin
      orchardBin.capacity = min(1.0, orchardBin.capacity)

  def pickupRequest(self):
    self.pickup = True

  def deliveryRequest(self):
    self.delivery = True
  
    
    
if __name__ == '__main__':
  num_rows = 10
  row_size = 10
  num_bots = 5
  num_bins = 0
  num_wkrs = 15
  sim = simulator(num_rows, row_size, num_bots, num_bins, num_wkrs)




  sim.drawSimulator()