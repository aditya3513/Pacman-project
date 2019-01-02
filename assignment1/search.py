# search.py
# ---------
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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    
    
    fringe = util.Stack()
    fringe.push(Node(problem.getStartState()))
    Visited_Node_set = []

    while True:
        if fringe.isEmpty():
            return []

        node = fringe.pop()
        
        if problem.isGoalState(node.get_current_State()):
            return node.get_current_Actions()
        if node.get_current_State() not in Visited_Node_set:
            Visited_Node_set.append(node.get_current_State())
            for node_temp in expand_node(node, problem):
                fringe.push(node_temp)



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    
    fringe = util.PriorityQueue()
    node = Node(problem.getStartState())
    fringe.push(node, node.getDepth_value())
    Visited_Node_set = []

    while True:
        if fringe.isEmpty():
            return []

        node = fringe.pop()
        
        if problem.isGoalState(node.get_current_State()):
            return node.get_current_Actions()
        if node.get_current_State() not in Visited_Node_set:
            Visited_Node_set.append(node.get_current_State())
            for node_temp in expand_node(node, problem):
                fringe.push(node_temp, node.getDepth_value())




def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    
    fringe = util.PriorityQueue()
    node = Node(problem.getStartState())
    node.setAddedCost_value(0)
    fringe.push(node, node.getAddedCost_value())
    Visited_Node_set = []

    while True:
        if fringe.isEmpty():
            return []

        node = fringe.pop()
        
        if problem.isGoalState(node.get_current_State()):
            return node.get_current_Actions()
        if node.get_current_State() not in Visited_Node_set:
            Visited_Node_set.append(node.get_current_State())
            for node_temp in expand_node(node, problem):
                fringe.push(node_temp, node_temp.getAddedCost_value())


            

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    
    fringe = util.PriorityQueue()
    node = Node(problem.getStartState())
    node.setAddedCost_value(0)
    fringe.push(node, node.getAddedCost_value() + heuristic(node.get_current_State(), problem))
    Visited_Node_set = []

    while True:
        if fringe.isEmpty():
            return []

        node = fringe.pop()
        
        if problem.isGoalState(node.get_current_State()):
            return node.get_current_Actions()
        if node.get_current_State() not in Visited_Node_set:
            Visited_Node_set.append(node.get_current_State())
            insert_Nodes_C_H(fringe, expand_node(node, problem), heuristic, problem)



""" DEFINING NODE CLASS """
class Node:
    
    def __init__(self, state):
        self.actionList = []
        self.state = state
        self.AddedCost = 0

    def get_current_State(self):
        return self.state

    def get_current_Actions(self):
        return self.actionList
  
    def setActionList(self, actions):
        self.actionList = actions[:]

    def addAction(self, action):
        self.actionList.append(action)

    def getDepth_value(self):
        return len(self.actionList)

    def getAddedCost_value(self):
        return self.AddedCost

    def setAddedCost_value(self, cost):
        self.AddedCost = cost


"""     HELPER FUNCTION USED IN VRIOUS FUNCTIONS """

def expand_node(node, problem):
    childList = []
    #print node.get_current_Actions()
    successors = problem.getSuccessors(node.get_current_State())
    #print successors
    for i in range(len(successors)):
        successor = successors[i]
        child_node = Node(successor[0])
        child_node.setActionList(node.get_current_Actions())
        child_node.addAction(successor[1])
        child_node.setAddedCost_value(node.getAddedCost_value() + successor[2])
        childList.append(child_node)

    return childList

def insert_Nodes_C_H(queue, nodeList, heuristic, problem):
    for node in nodeList:
        queue.push(node, node.getAddedCost_value() + heuristic(node.get_current_State(), problem))

""" ------------------------------------------------------------------------"""


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
