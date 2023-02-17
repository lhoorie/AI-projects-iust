# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
from game import Agent
import math

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
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
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print(successorGameState)
        # print(newPos)
        # print(newFood)                                  #####JUST FOR TESTING#####
        #for a in newGhostStates:
        #   print(a)
        # print(newScaredTimes)
        # print(currentGameState)


        foodsStates = currentGameState.getFood()
        foodsList = foodsStates.asList()
        mDis = []

        for food in foodsList:
            mDis.append(-manhattanDistance(food, newPos))

        res = max(mDis)
        
        for i, state in enumerate(newGhostStates):
            if newScaredTimes[i] == 0 and state.getPosition() == newPos:
                return -999

        return res

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

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        # print(gameState.getLegalActions(0))
        # print(gameState.getNumAgents())
        # print(gameState.isWin())


        def value(s, i, d):
            if s.isLose() or s.isWin() or d==0:
                return self.evaluationFunction(s)
            if i==0:
                return maxValue(s,i,d)
            else:
                return minValue(s,i,d)

        def maxValue(s,i,d):
            v = -math.inf
            legalActions = s.getLegalActions(i)
            successors = []

            for action in legalActions:
                successors.append(s.generateSuccessor(i,action))

            for successor in successors:
                v = max(v, value(successor, (i+1)%s.getNumAgents(), d-1))

            return v

        def minValue(s,i,d):
            v = math.inf
            legalActions = s.getLegalActions(i)
            successors = []

            for action in legalActions:
                successors.append(s.generateSuccessor(i,action))

            for successor in successors:
                v = min(v, value(successor, (i+1)%s.getNumAgents(), d-1))

            return v


        legalActions = gameState.getLegalActions(0)
        scores = []
        d = self.depth * gameState.getNumAgents()

        for action in legalActions:
                scores.append(value(gameState.generateSuccessor(0, action), 1, d - 1))

        bestScore = max(scores)
        
        for i in range(len(scores)):
            if scores[i]==bestScore:
                index = i

        return legalActions[index]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def value(self, s, d, a, b, i):
            if s.isLose() or s.isWin() or d==0:
                return self.evaluationFunction(s)
            if s.getNumAgents()==i:
                return value(self, s, d-1, a, b, 0)
            if i==0:
                    return maxValue(self, s, d, a, b, i)
            else:
                return minValue(self, s, d, a, b, i)
            

        def maxValue(self, s, d, a, b, i):
            maxValue = -math.inf
            legalActions = s.getLegalActions(i)
            bestAction = None

            for action in legalActions:
                v=value(self, s.generateSuccessor(i, action), d, a, b, i+1)
                if(maxValue<v):
                    maxValue=v
                    bestAction=action
                a=max(a,v)
                if b<a:
                    break
            if d==self.depth:
                return bestAction
            else:
                return maxValue

        def minValue(self, s, d, a, b, i):
            v = math.inf
            legalActions = s.getLegalActions(i)

            for action in legalActions:
                v=min(v, value(self, s.generateSuccessor(i, action), d, a, b, i+1))
                b=min(b,v)
                if b<a:
                    break
            return v
        
        return value(self, gameState, self.depth, -math.inf, math.inf, 0)

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

        def value(s, i, d):
            if s.isLose() or s.isWin() or d==0:
                return self.evaluationFunction(s)
            if i==0:
                return maxValue(s,i,d)
            else:
                return expValue(s,i,d)

        def maxValue(s,i,d):
            v = -math.inf
            legalActions = s.getLegalActions(i)
            successors = []

            for action in legalActions:
                successors.append(s.generateSuccessor(i,action))

            for successor in successors:
                v = max(v, value(successor, (i+1)%s.getNumAgents(), d-1))

            return v

        def expValue(s,i,d):
            v = 0
            legalActions = s.getLegalActions(i)
            successors = []

            for action in legalActions:
                successors.append(s.generateSuccessor(i,action))

            l=len(successors)

            for successor in successors:
                v += value(successor, (i+1)%s.getNumAgents(), d-1)

            v=v/l

            return v


        legalActions = gameState.getLegalActions(0)
        scores = []
        d = self.depth * gameState.getNumAgents()

        for action in legalActions:
                scores.append(value(gameState.generateSuccessor(0, action), 1, d-1))

        bestScore = max(scores)
        
        for i in range(len(scores)):
            if scores[i]==bestScore:
                index = i

        return legalActions[index]

class assignValueToAgents:
    def __init__(self):
        self.ghost = random.randint(8,12)
        self.scaredGhost = random.randint(48,52)
        self.food = self.ghost
    
def isScared(ghostPosition):
    return ghostPosition.scaredTimer > 0

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    score = currentGameState.getScore()
    agentValues = assignValueToAgents()
    

    ghostValue = 10
    foodValue = 10 
    scaredGhostValue = 50 
    values = []
    foodDis = []

    for ghostPosition in newGhostStates:
        mDis = manhattanDistance(newPos, ghostPosition.getPosition())

        try:
            if isScared(ghostPosition):
                values.append(("+" , agentValues.scaredGhost/mDis))
            else:
                values.append(("-" , agentValues.ghost/mDis))
        except:
            pass

    for v in values:
        if v[0] == "+":
            score += v[1]
        else:
            score -= v[1]

    for foodPos in newFood.asList():
        foodDis.append(manhattanDistance(newPos, foodPos))

    if foodDis:
        score += agentValues.food/min(foodDis)

    return score

# Abbreviation
better = betterEvaluationFunction