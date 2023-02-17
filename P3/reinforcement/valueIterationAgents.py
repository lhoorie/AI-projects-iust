 # valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


from queue import Empty
import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for iterate in range(self.iterations):
            values = util.Counter()
            for state in self.mdp.getStates():
                if not self.mdp.isTerminal(state):
                    action = self.getAction(state)
                    values[state] = self.computeQValueFromValues(state, action)
            self.values = values


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        states = self.mdp.getTransitionStatesAndProbs(state, action)
        qValue = 0
        for nextState, t in states: #T(s,a,s')  & s'
            gamma = self.discount #gamma
            v = self.values[nextState] #V(s')
            r = self.mdp.getReward(state, action, nextState) #Reward(s,a,s')
            qValue += t * (r + gamma * v)
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        possibleActions = self.mdp.getPossibleActions(state)

        actionsValue = util.Counter()

        for action in possibleActions:
            actionsValue[action] = self.getQValue(state, action)

        return actionsValue.argMax()


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        allStates = self.mdp.getStates()

        for iterate in range(self.iterations):
            i = iterate % len(allStates)
            state = allStates[i]
            possibleActions = self.mdp.getPossibleActions(state)

            if not self.mdp.isTerminal(state):  
                values = []
                for action in possibleActions:
                    values.append(self.computeQValueFromValues(state, action))
                self.values[state] = max(values)
        return

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        allStates = self.mdp.getStates()
        pQueue = util.PriorityQueue()
        predecessors = dict()
        allIterations = self.iterations

        #Compute diff
        for state in allStates:
            if not self.mdp.isTerminal(state):
                possibleActions = self.mdp.getPossibleActions(state)
                qValues= []
                for action in possibleActions:
                    qValues.append(self.computeQValueFromValues(state, action))
                value = max(qValues)
                diff = - abs(value - self.values[state])
                pQueue.update(state, diff)

        #Compute predecessors
        for state in allStates:
            if not self.mdp.isTerminal(state):
                possibleActions = self.mdp.getPossibleActions(state)
                for action in possibleActions:
                    tANDp = self.mdp.getTransitionStatesAndProbs(state, action)
                    for nextState, t in tANDp:
                        if nextState in predecessors:
                            predecessors[nextState].add(state)
                        else:
                            predecessors[nextState] = {state}

        for iteration in range(allIterations):
            if pQueue.isEmpty():
                return
            
            state = pQueue.pop()
            if not self.mdp.isTerminal(state):
                possibleAction = self.mdp.getPossibleActions(state)
                qValues= []
                for action in possibleAction:
                    qValues.append(self.computeQValueFromValues(state, action))
                self.values[state] = max(qValues)

            for pState in predecessors[state]:
                if not self.mdp.isTerminal(pState):
                    possibleAction = self.mdp.getPossibleActions(pState)
                    qValues= []
                    for action in possibleAction:
                        qValues.append(self.computeQValueFromValues(pState, action))
                    qValue = max(qValues)
                    diff = - abs(qValue - self.values[pState])
        
                    if self.theta > diff:
                        pQueue.update(pState, diff)    

