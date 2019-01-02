# multiAgents.py
# --------------
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

"""

''''''ASSIGNMENT COMPLETED IN A GROUP WITH KSHITIZ ADLAKHA'''''

"""
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

win = float("inf")

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
        currFoodList = currentGameState.getFood()
        capsuleList = currentGameState.getCapsules()
        currPos = currentGameState.getPacmanPosition()

        large_val = 10000000000
        score = 0
        x, y = newPos
        if (newPos == currPos and check_pacman_stop(action)):
            score = - float(large_val)

        for n in newScaredTimes:
            if (ghost_present(newGhostStates, newPos) == True or check_pacman_stop(action)) and n == 0:
                score = - float(large_val)

            else:
                score = (min(food_manhatt_dist_list(currFoodList, newPos, capsuleList)))

                if float(score) == 0:
                    score = 1 / (float(score) + 1)
                else:
                    score = 1 / float(score)

        return score

def ghost_present(newGhostStates, newPos):

        for ghost_state in newGhostStates:
            ghost_pos = ghost_state.getPosition()
            if newPos == ghost_pos:
                return True
            else:
                return False

def food_manhatt_dist_list(food, pos, capsule):
        my_list = []
        large_val = 10000000000
        distance = float(large_val)
        my_list.append(distance)
        for f in food.asList():
            distance = manhattanDistance(f, pos)
            my_list.append(distance)
        # considering capsule location
        for c in capsule:
            distance = manhattanDistance(c, pos)
            my_list.append(distance)
        return my_list

def check_pacman_stop(action):

        if ("Stop" in action):
            return True
        else:
            return False


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
      Code implemented using algorithm given at

      https://en.wikipedia.org/wiki/Minimax

    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        bestScore = float("-inf")
        bestMove = Directions.STOP
        for actions in gameState.getLegalActions(0):
            child = gameState.generateSuccessor(0, actions)
            score = self.minimax(child, self.depth, 0)
            if score> bestScore:
                bestScore=score
                bestMove=actions
        return bestMove

    def minimax(self, gameState, depth, agentIndex):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        numAgents = gameState.getNumAgents()
        newIndex = (agentIndex + 1) % numAgents
        if newIndex == 0:
            value = float("-inf")
            temp_states = gameState.getLegalActions(newIndex)
            for action in temp_states:
                child=gameState.generateSuccessor(0, action)
                value = max(value, self.minimax(child, depth, newIndex))
            return value
        else:
            value = float("inf")
            temp_states = gameState.getLegalActions(newIndex)
            for action in temp_states:
                if newIndex >= gameState.getNumAgents() - 1:
                    child = gameState.generateSuccessor(newIndex, action)
                    value = min(value, self.minimax(child, depth - 1, newIndex))
                else:
                    child = gameState.generateSuccessor(newIndex, action)
                    value = min(value, self.minimax(child, depth, newIndex))
            return value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
      Implaemented using algorithm given at

      https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

    """
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha = float("-inf")
        beta = float("inf")
        bestMove = Directions.STOP
        for actions in gameState.getLegalActions(0):
            child = gameState.generateSuccessor(0, actions)
            score = self.alphabeta(child, self.depth, alpha, beta, 0)
            if score> alpha:
                alpha=score
                bestMove=actions
        return bestMove

    def alphabeta(self, gameState, depth, alpha, beta, agentIndex):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        numAgents = gameState.getNumAgents()
        newIndex = (agentIndex + 1) % numAgents
        if newIndex == 0:
            value = float("-inf")
            temp_states = gameState.getLegalActions(newIndex)
            for action in temp_states:
                child=gameState.generateSuccessor(0, action)
                value = max(value, self.alphabeta(child, depth, alpha, beta, newIndex))
                if value > beta:
                    return value
                alpha = max(alpha, value)
            return value
        else:
            value = float("inf")
            temp_states = gameState.getLegalActions(newIndex)
            for action in temp_states:
                if newIndex >= gameState.getNumAgents() - 1:
                    child = gameState.generateSuccessor(newIndex, action)
                    value = min(value, self.alphabeta(child, depth - 1, alpha, beta, newIndex))
                else:
                    child = gameState.generateSuccessor(newIndex, action)
                    value = min(value, self.alphabeta(child, depth, alpha, beta, newIndex))
                if value < alpha:
                    return value
                beta = min(beta, value)
            return value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
      Implemented algorithm given at
      https://en.wikipedia.org/wiki/Expectiminimax_tree
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        bestScore = float("-inf")
        bestMove = Directions.STOP
        for actions in gameState.getLegalActions(0):
            child = gameState.generateSuccessor(0, actions)
            score = self.expectimax(child, self.depth, 0)
            if score > bestScore:
                bestScore = score
                bestMove = actions
        return bestMove

    def expectimax(self, gameState, depth, agentIndex):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        numAgents = gameState.getNumAgents()
        newIndex = (agentIndex + 1) % numAgents
        if newIndex < agentIndex:
            depth -=1
        if newIndex == 0:
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            value = float("-inf")
            temp_states = gameState.getLegalActions(newIndex)
            for action in temp_states:
                child = gameState.generateSuccessor(0, action)
                value = float(max(value, self.expectimax(child, depth, newIndex)))
            return value
        else:
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            value = 0.0
            temp_states = gameState.getLegalActions(newIndex)
            p = 1.0 / len(temp_states)
            for action in temp_states:
                child = gameState.generateSuccessor(newIndex, action)
                value += self.expectimax(child, depth, newIndex)*p
            return value

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    currFoodList = currentGameState.getFood()
    capsuleList = currentGameState.getCapsules()
    large_val = 10000000000
    score = 0
    x, y = newPos
    for n in ScaredTimes:
        if (ghost_present(GhostStates, newPos) == True) and n == 0:
            score = - float(large_val)
        else:
            score = (min(food_manhatt_dist_list(currFoodList, newPos, capsuleList)))
            if float(score) == 0:
                score = 1 / (float(score) + 1)
            else:
                score = 1 / float(score)
    return score+currentGameState.getScore()+sum(ScaredTimes)


# Abbreviation
better = betterEvaluationFunction

