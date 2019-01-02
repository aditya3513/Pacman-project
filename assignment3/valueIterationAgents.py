# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

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

        Here what we do is :
        1) iterate over the no if iterations given in self.iteration by step of 1
        2) get all states in mdp and initialize counter to 0 by default, when using util.Counter
        3) iterate over the state_set and find possibel action for each state
        4) for each action find q value and update value of each counter for each state by that q value
            else the vale added to counter is zero


        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        counter = util.Counter()

        for k in range(0, self.iterations, 1):

            state_set = mdp.getStates()
            counter = util.Counter()

            for s in state_set:

                possible_actions = mdp.getPossibleActions(s)
                max = float("-inf")

                for action in possible_actions:
                    q_star = self.computeQValueFromValues(s, action)

                    if q_star > max:
                        max = q_star
                        counter[s] = max
            self.values = counter
        print "here it is"
        print self.values


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.

        This is how it works :

        1) first we get all trans states and the transition probs for each state.

        2) then we calculate reward on basis of the current state, action,
        and new state which we reach after that action

        3) we calculate V* of the new state from getValue function.

        4) Now we use the formula and compute Q value :

        Q* = SUMMATION  [trans_prob * (reward + V*)]

        """
        "*** YOUR CODE HERE ***"
        q_star = 0

        for state_new, trans_prob in self.mdp.getTransitionStatesAndProbs(state, action):
            reward = self.mdp.getReward(state, action, state_new)
            v_star = self.discount * self.getValue(state_new)
            value = trans_prob * (reward + v_star)
            q_star = q_star + value
        return q_star

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.

            This is how it works :

            1) set action_to_do as none so that if no case matches then we send action as none
            2) now we get all possible ations for the current state
            3) iterating all over the states we compute Q value of each action and
                if Q value is greater than Q value of previous states
                then set action_to_do as current action
            4) return value of action_to_do

        """
        action_to_do = None
        max = float("-inf")

        possible_actions = self.mdp.getPossibleActions(state)
        for action in possible_actions:
            q_star = self.computeQValueFromValues(state, action)
            if q_star > max:
                action_to_do = action
                max = q_star

        return action_to_do


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
