# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    self.nearestFood = self.getNearstFood(gameState);
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """



    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    WORSTSTATE=-10000;
    BAD_STATE=-99999;
    if newPos==newGhostStates[0].configuration.pos:
      return WORSTSTATE;

    if action==Directions.STOP:
      return BAD_STATE;


    distance = manhattanDistance(self.nearestFood, newPos);

    return -distance;

    return successorGameState.getScore()

    # Useful information you can extract from a GameState (pacman.py)
  def getNearstFood(self,gameState):
        minDistance = 10000;
        distance = 0;
        listOfFood = gameState.getFood();
        x = 0;
        for food in listOfFood:
            y = 0;
            for f in food:
                if f == True:
                    distance = manhattanDistance((x, y),gameState.getPacmanPosition());
                    if (minDistance > distance):
                        minDistance = distance;
                        nearestPoint = (x, y);
                y += 1;
            x += 1;
        return nearestPoint;


def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"


    def maxValue(state,depth):
        if depth == self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        v=-999999
        listValue = state.getLegalActions(0)
        if Directions.STOP in listValue:
          listValue.remove(Directions.STOP)


        scores = [minValue(state.generateSuccessor(0, action), depth) for action in  listValue]
        bestScore = max(scores)
        v = max( v,bestScore)
        return v




    def minValue(state,depth):
      v=99999
      if depth == self.depth or state.isWin() or state.isLose():
          return self.evaluationFunction(state)
      depth += 1
      if state.getNumAgents()<2:
          return []
      listValue = state.getLegalActions(1)


      stateofghost = [state.generateSuccessor(1, action) for action in  listValue ]
      for i in range(2,state.getNumAgents()):
          ghosts=[]
          legalact=state.getLegalActions(i)
          for g in stateofghost:
              if g.isLose():
                  return self.evaluationFunction(g)
              newghosts = [g.generateSuccessor(i, action) for action in state.getLegalActions(i)]
              ghosts=newghosts+ghosts
          stateofghost=ghosts

      scores = [maxValue(g,depth) for g in stateofghost]

      v = min(v,min(scores))
      return v

    legalMoves = gameState.getLegalActions(0)

    if Directions.STOP in legalMoves:
        legalMoves.remove(Directions.STOP)
     #self.cnt=0

    scores = [minValue(gameState.generateSuccessor(0, action), 0) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
    move= legalMoves[chosenIndex]
    return move



    util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"

    def maxValue(state,alfa,beta,depth):
        if depth == self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        v=-999999
        listValue = state.getLegalActions(0)
        if Directions.STOP in listValue:
          listValue.remove(Directions.STOP)

        for action in listValue:
          v = max(v,minValue(state.generateSuccessor(0, action),alfa,beta, depth))
          if v>=beta :
             return v
          alfa = max(alfa,v)
        return v

    def minValue(state,alfa,beta, depth):
        v = 99999
        if depth == self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        depth += 1
        if state.getNumAgents() < 2:
            return []
        listValue = state.getLegalActions(1)

        stateofghost = [state.generateSuccessor(1, action) for action in listValue]
        for i in range(2, state.getNumAgents()):
            ghosts = []
            legalact = state.getLegalActions(i)
            for g in stateofghost:
                if g.isLose():
                    return self.evaluationFunction(g)
                newghosts = [g.generateSuccessor(i, action) for action in state.getLegalActions(i)]
                ghosts = newghosts + ghosts
            stateofghost = ghosts

        for g in stateofghost:
            v = min(v,maxValue(g, alfa,beta,depth))
            if v<=alfa:
                return v
            beta = min(beta,v)
        return v

    beta = 99999
    alfa = -99999
    bestScore = -99999
    legalMoves = gameState.getLegalActions(0)

    if Directions.STOP in legalMoves:
        legalMoves.remove(Directions.STOP)
    # self.cnt=0




    list = []
    for action in legalMoves:
        scores = minValue(gameState.generateSuccessor(0, action), alfa, beta, 0)
        if scores > alfa:
            list = [action]
            alfa = scores
        elif scores == alfa:
            list = list + [action]
        bestScore = max(scores, bestScore)
    chosenIndex = random.choice(list)  # Pick randomly among the best
    return chosenIndex
    util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

