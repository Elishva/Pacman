# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 74].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.18].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """

  start=problem.getStartState()
  frontier=util.Stack()
  explored={}
  frontier.push(((start,[],0),[]))
  while not frontier.isEmpty():
      node=frontier.pop()
      point,dir,cost=node[0]
      path=node[1]

      if  problem.isGoalState(point):
          return path

      explored[point]=0
      s= problem.getSuccessors(point)
      for p in s:
          pPoint, pDir, pCost = p
          if pPoint not in explored and not isExsist(frontier,pPoint):
              state=((pPoint,pDir,cost+pCost),path+[pDir])
              frontier.push(state)
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def isExsist(f,point):

    for p in f.list:
        node,path=p
        if point==node[0]:
            return True
    return False



def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 74]"
  "*** YOUR CODE HERE ***"
  start = problem.getStartState()
  frontier = util.Queue()
  explored = {}
  frontier.push(((start,"", 0), []))
  if problem.isGoalState(start):
      return None

  while not frontier.isEmpty():
      node,path=frontier.pop()
      point,dir,cost=node
      explored[point]=0
      s = problem.getSuccessors(point)
      for child in s:
          cPoint,cdir,cCost=child
          if(cPoint not in explored and not isExsist(frontier,cPoint)):
              if problem.isGoalState(cPoint):
                  return path+[cdir]
              state=(child,path+[cdir])
              frontier.push(state)


  util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  start = problem.getStartState()
  frontier = util.PriorityQueue()
  explored = {}
  frontier.push(((start, "", 0), []),0)
  while not frontier.isEmpty():
     node,path=frontier.pop()
     point, dir, cost = node

     if point in explored:
         continue
     explored[point] = 0
     s = problem.getSuccessors(point)
     if problem.isGoalState(point):
         return path
     for child in s:
         cPoint, cdir, cCost = child
         if cPoint not in explored :

             state = (((cPoint, cdir, cCost+cost), path + [cdir]))
             frontier.push(state,cost+cCost)
         else :
             for p in frontier.heap :
                 pKey, pState =p
                 node,pPath=pState
                 pPoint,pdir,pCost=node
                 if cPoint==pPoint:
                     if cost+cCost<pCost:
                         frontier.heap.remove(p)
                         state = (((cPoint, cdir, cCost + cost), path + [cdir]))
                         frontier.push(state,cost+cCost)



  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()


def isExsistHeap(f,point):

    for p in f.heap:
       proir,node=p
       if point==node[0][0]:
            return True
    return False
def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  start = problem.getStartState()
  frontier = util.PriorityQueue()
  explored = {}
  frontier.push(((start, "", 0), []),  heuristic(start, problem))
  while not frontier.isEmpty():
      node, path = frontier.pop()
      point, dir, cost = node
      if problem.isGoalState(point):
          return path
      explored[point] = 0
      s = problem.getSuccessors(point)

      for child in s:
          cPoint, cdir, cCost = child
          if cPoint not in explored and not isExsistHeap(frontier, cPoint):
              h= heuristic(cPoint, problem)
              state = (((cPoint, cdir, cCost + cost), path + [cdir]))
              frontier.push(state, cost + cCost+h)
          else:
              if isExsistHeap(frontier,cPoint):
                for p in frontier.heap:
                  pKey, pState = p
                  node, pPath = pState
                  pPoint, pdir, pCost = node
                  if cPoint == pPoint:
                      if cost + cCost < pCost:
                          frontier.heap.remove(p)
                          state = (((cPoint, cdir, cCost + cost), path + [cdir]))
                          frontier.push(state, cost + cCost+pKey)
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch