
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import random, copy, operator


class simulator(object):
  """docstring for simulator"""
  def __init__(self, num_rows, row_size, num_bots, num_bins, num_wkrs):
    #random init

    self.num_rows = num_rows
    self.row_size = row_size

    self.orchard_map = [[None for ii in range(row_size+2)] for jj in range(3*self.num_rows)]

    for row_id, row in enumerate(self.orchard_map):
      for spot_id, spot in enumerate(row):
        if spot_id == 0:
          #self.orchard_map[row_id][spot_id] = "depot"
          self.orchard_map[row_id][spot_id] = cell("depot")
        elif spot_id == len(row)-1:
          self.orchard_map[row_id][spot_id] = cell("headlands")
          #self.orchard_map[row_id][spot_id] = "headlands"
        else:
          if row_id%3 == 1:
            self.orchard_map[row_id][spot_id] = cell("path")
            #self.orchard_map[row_id][spot_id] = "orchard"
          else:
            self.orchard_map[row_id][spot_id] = cell("orchard")
            #self.orchard_map[row_id][spot_id] = "path"

    self.wkrs = {}
    self.bots = {}
    self.bins = {}

    self.num_bins = num_bins
    self.collected_bins = 0
    self.profit = 0

    # for ii in range(num_wkrs):
    while len(self.wkrs) < num_wkrs:
      worker_loc = [random.randint(0, num_rows-1)*3+1, 1+random.randint(0, row_size-1)]
      for worker in self.wkrs:
        if worker_loc == self.wkrs[worker].loc:
          break
      else:
        worker_id = len(self.wkrs)
        self.wkrs[worker_id] = workerGroup(worker_loc)
        self.orchard_map[worker_loc[0]][worker_loc[1]].bins.append(worker_id) 

    while len(self.bots) < num_bots:
      bot_loc = [random.randint(0, num_rows*2+1), 0]
      for bot in self.bots:
        if bot_loc == self.bots[bot].loc:
          break
      else:
        bot_id = len(self.bots)
        self.bots[bot_id] = bindog(bot_loc)
        self.orchard_map[bot_loc[0]][bot_loc[1]].bots.append(bot_id)

    for bin_id, worker in enumerate(self.wkrs):
      bin_loc = [x for x in self.wkrs[worker].loc]
      self.bins[bin_id] = orchardBin(bin_loc)
      self.orchard_map[bin_loc[0]][bin_loc[1]].bins.append(bin_id)


  def pickFruit(self, worker):
    worker = self.wkrs[worker]
    x, y = worker.loc
    current_cell = self.orchard_map[x][y]

    if len(current_cell.bins) > 0:
      current_bin = self.bins[current_cell.bins[0]]
      max_picked = min((.1 + .1 * random.random())*worker.efficiency, current_bin.capacity)
      #max_picked = min(.2, self.bins[current_cell.bins[0]].capacity)

      total_apples_picked = 0
      for side in [1, -1]:
        apples_picked_side = 0
        max_picked_side = max_picked/2
      
        orchard_apples_picked = min(self.orchard_map[x+side][y].apples, max_picked_side)
        apples_picked_side += orchard_apples_picked
        self.orchard_map[x+side][y].apples -= orchard_apples_picked

        if apples_picked_side < max_picked_side:
          side_remaining = max_picked_side - apples_picked_side
          for offset in [-1, 1]:
            if self.orchard_map[x+side][y+offset].terrain == "orchard":
              orchard_apples_picked = min(self.orchard_map[x+side][y+offset].apples, side_remaining/2)
              apples_picked_side += orchard_apples_picked
              self.orchard_map[x+side][y+offset].apples -= orchard_apples_picked
        total_apples_picked += apples_picked_side
      current_bin.capacity -= total_apples_picked


  def step(self):
    for bot in self.bots:
      bot = self.bots[bot]
      bot.takeAction(bot.plan[0], self)
      


    for worker in self.wkrs:
      self.pickFruit(worker)



  def drawSimulator(self):
    scale = 10
    #img_size = [(self.num_rows*2+1)*scale, self.row_size+2*scale]
    fig1 = plt.figure()
    ax1 = plt.gca()

    plt.xlim((-.5, (self.num_rows*3-.5)))
    plt.ylim((-.5, self.row_size+1.5))

    for row_id, row in enumerate(self.orchard_map):
      for col_id, item in enumerate(row):
        if item.terrain == "orchard":
          ax1.add_patch(patches.Rectangle((row_id-.5, col_id-.5), 1., 1., facecolor="#228b22"))
          plt.text(row_id, col_id, str(item.apples)[:4])
        elif item.terrain == "headlands":
          ax1.add_patch(patches.Rectangle((row_id-.5, col_id-.5), 1., 1., facecolor="#776b46"))
        elif item.terrain == "depot":
          ax1.add_patch(patches.Rectangle((row_id-.5, col_id-.5), 1., 1., facecolor="#ffc000"))


    for bot in self.bots:
      drawBindog(ax1, self.bots[bot])
      plt.text(self.bots[bot].loc[0]-.1, self.bots[bot].loc[1]-.05, bot)

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
        res.append(self.wkrs[worker].loc)

    return res


  def getBinDeliveryRequests(self):
    res = []

    for worker in self.wkrs:
      if self.wkrs[worker].delivery:
        res.append(self.wkrs[worker].loc)
        
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
  def __init__(self, terrain):
    self.terrain = terrain
    
    if self.terrain is not 'orchard':
      self.bins = []
      self.wkrs = []
      self.bots = []
      self.apples = None
    else:
      self.bins = None
      self.bots = None
      self.wkrs = None
      self.apples = .9 + .2*random.random()


class bindog(object):
  """docstring for bindog"""
  def __init__(self, loc):
    self.loc = loc
    self.status = "idle" #robot starts idle
    self.target = None #Default no target
    self.bin = None #Robot Starts with No Bin

  def takeAction(self, action, sim):
    if action == "N":
      proceed = True
      print sim.orchard_map[self.loc[0]]
      for map_cell in sim.orchard_map[self.loc[0]]:
        if map_cell.terrain == "path" and len(map_cell.bots) > 0:
          proceed = False
      if proceed:
        self.moveBot([0, 1], sim)
        bot.plan = bot.plan[1:]
      #go North
      return 0
    elif action == "S":
      self.moveBot([0, -1], sim)
      bot.plan = bot.plan[1:]
      #go South
      return 0
    elif action == "E":
      self.moveBot([1, 0], sim)
      bot.plan = bot.plan[1:]
      #go East
      return 0
    elif action == "W":
      self.moveBot([-1, 0], sim)
      bot.plan = bot.plan[1:]
      #go West
      return 0
    elif action == "P":
      self.placeBin()
      return 0
    elif action == "G":
      self.getBin(sim.orchard_map)
      return 0
    else:
      return 0

  def getBin(self, orchard_map):
    if len(orchard_map[self.loc[0]][self.loc[1]].bins) > 0:
      self.bin = orchard_map[self.loc[0]][self.loc[1]].bins[0]


  def placeBin(self):
    if self.bin is not None:
      self.bin = None

  def moveBot(self, action, sim):
    self.loc = map(operator.add, self.loc, action) # need to define action
    if self.bin is not None:
      sim.bins[self.bin].loc = self.loc

 
  def hasBin(self):
    return self.bin is not None


class orchardBin(object):
  """docstring for orchardBin"""
  def __init__(self, loc, capacity = 1.0):
    self.loc = loc
    self.capacity = capacity #Default bin is empty, bin is full if capacity = 0
    self.bot_assigned = False

  def estimateTimeToFull(self):
    picking_rate = .15
    return self.capacity / picking_rate



class workerGroup(object):
  """docstring for workerGroup"""
  def __init__(self, loc):
    self.loc = loc
    self.efficiency = .9+random.random()*.2
    self.pickup = False
    self.delivery = False


  def pickupRequest(self):
    self.pickup = True

  def deliveryRequest(self):
    self.delivery = True
  

    
if __name__ == '__main__':
  # num_rows = 10
  # row_size = 10
  # num_bots = 5
  # num_bins = 30
  # num_wkrs = 5
  sim = simulator(5, 5, 1, 30, 1)
  bot = sim.bots[sim.bots.keys()[0]]
  bot.plan = ["N", "S", "E", "W"]
  sim.step()
  print bot.loc
  sim.drawSimulator()
  sim.step()
  print bot.loc
  sim.drawSimulator()
  sim.step()
  print bot.loc
  sim.drawSimulator()
  sim.step()
  print bot.loc
  sim.drawSimulator()