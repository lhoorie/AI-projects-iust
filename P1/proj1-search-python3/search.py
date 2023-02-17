# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from pickle import APPEND
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # Initializing

    myStack=util.Stack()
    startNode=problem.getStartState()
    myStack.push([startNode, "Start"])
    fringeSet=[]
    closedSet=[]
    path={}

    # DFS
    while(myStack.isEmpty() == False):
        currentNode=myStack.pop()

        if(problem.isGoalState(currentNode[0])): # GoalState Checking
            break
        else:
            if(currentNode[0] not in fringeSet): # Add to fringeSet
                fringeSet.append(currentNode[0])
            else:
                continue

            nextSteps=problem.getSuccessors(currentNode[0])

            for node in nextSteps:
                if(node[0] not in fringeSet):
                    myStack.push(node)
                    path[node]= currentNode

    while(currentNode is not None):
        closedSet.append(currentNode[1])

        if(currentNode[0]==startNode):
            currentNode=None  
        else:
            currentNode=path[currentNode]

    closedSet.reverse() 
    res=closedSet[1:]

    return res


def iterativeDp(problem, limit):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # Initializing

    myStack=util.Stack()
    startNode=problem.getStartState()
    myStack.push([startNode, "Start"])
    fringeSet=[]
    closedSet=[]
    path={}

    temp = 100

    # DFS
    while(myStack.isEmpty() == False and temp <= limit):
        currentNode=myStack.pop()

        if(problem.isGoalState(currentNode[0])): # GoalState Checking
            break
        else:
            if(currentNode[0] not in fringeSet): # Add to fringeSet
                fringeSet.append(currentNode[0])
            else:
                continue

            nextSteps=problem.getSuccessors(currentNode[0])

            for node in nextSteps:
                if(node[0] not in fringeSet):
                    myStack.push(node)
                    path[node]= currentNode
            
            if(len(fringeSet) == temp):
                break

        temp +=100

    while(currentNode is not None):
        closedSet.append(currentNode[1])

        if(currentNode[0]==startNode):
            currentNode=None  
        else:
            currentNode=path[currentNode]

    closedSet.reverse() 
    res=closedSet[1:]

    return res



def depthFirstSearchWithLimit(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # Initializing

    myStack=util.Stack()
    startNode=problem.getStartState()
    myStack.push([startNode, "Start"])
    fringeSet=[]
    closedSet=[]
    path={}

    # DFS
    while(myStack.isEmpty() == False):
        currentNode=myStack.pop()

        if(problem.isGoalState(currentNode[0])): # GoalState Checking
            break
        else:
            if(currentNode[0] not in fringeSet): # Add to fringeSet
                fringeSet.append(currentNode[0])
            else:
                continue

            nextSteps=problem.getSuccessors(currentNode[0])

            for node in nextSteps:
                if(node[0] not in fringeSet):
                    myStack.push(node)
                    path[node]= currentNode
            
            if(len(fringeSet) == 500):
                break

    while(currentNode is not None):
        closedSet.append(currentNode[1])

        if(currentNode[0]==startNode):
            currentNode=None  
        else:
            currentNode=path[currentNode]

    closedSet.reverse() 
    res=closedSet[1:]

    return res


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Initializing
    myQueue=util.Queue()
    startNode=problem.getStartState()
    myQueue.push([startNode, "Start"])
    fringeSet=[]
    closedSet=[]
    path={}

    # BFS
    while(myQueue.isEmpty() == False):
        currentNode=myQueue.pop()

        if(problem.isGoalState(currentNode[0])): # GoalState Checking
            break
        else:
            if(currentNode[0] not in fringeSet): # Add to fringeSet
                fringeSet.append(currentNode[0])
            else:
                continue

            nextSteps=problem.getSuccessors(currentNode[0])

            for node in nextSteps:
                if(node[0] not in fringeSet):
                    myQueue.push(node)
                    path[node]= currentNode

    while(currentNode is not None):
        closedSet.append(currentNode[1])

        if(currentNode[0]==startNode):
            currentNode=None  
        else:
            currentNode=path[currentNode]

    closedSet.reverse() 
    res=closedSet[1:]

    return res
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Initializing
    myQueue=util.PriorityQueueWithFunction(lambda x: x[2])
    startNode=problem.getStartState()
    myQueue.push([startNode, "Start", 0])
    fringeSet=[]
    closedSet=[]
    path={}

    # UCS
    while(myQueue.isEmpty() == False):
        currentNode=myQueue.pop()

        if(problem.isGoalState(currentNode[0])): # GoalState Checking
            break
        else:
            if(currentNode[0] not in fringeSet): # Add to fringeSet
                fringeSet.append(currentNode[0])
            else:
                continue

            nextSteps=problem.getSuccessors(currentNode[0])

            for nextNode in nextSteps:
                cost=currentNode[2]+nextNode[2]
                if(nextNode[0] not in fringeSet):
                    myQueue.push((nextNode[0],nextNode[1], cost))
                    path[(nextNode[0],nextNode[1])]= currentNode

    while(currentNode != None):
        closedSet.append(currentNode[1])

        if(currentNode[0]==startNode):
            currentNode=None  
        else:
            currentNode=path[(currentNode[0],currentNode[1])]

    closedSet.reverse() 
    res=closedSet[1:]

    return res

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Initializing
    myQueue=util.PriorityQueueWithFunction(lambda x: x[2] + heuristic(x[0], problem))
    startNode=problem.getStartState()
    myQueue.push([startNode, "Start", 0])
    fringeSet=[]
    closedSet=[]
    path={}

    # A*
    while(myQueue.isEmpty() == False):
        currentNode=myQueue.pop()

        if(problem.isGoalState(currentNode[0])): # GoalState Checking
            break
        else:
            if(currentNode[0] not in fringeSet): # Add to fringeSet
                fringeSet.append(currentNode[0])
            else:
                continue

            nextSteps=problem.getSuccessors(currentNode[0])

            for nextNode in nextSteps:
                cost=currentNode[2]+nextNode[2]
                if(nextNode[0] not in fringeSet):
                    myQueue.push((nextNode[0],nextNode[1], cost))
                    path[(nextNode[0],nextNode[1])]= currentNode

    while(currentNode != None):
        closedSet.append(currentNode[1])

        if(currentNode[0]==startNode):
            currentNode=None  
        else:
            currentNode=path[(currentNode[0],currentNode[1])]

    closedSet.reverse() 
    res=closedSet[1:]

    return res


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
