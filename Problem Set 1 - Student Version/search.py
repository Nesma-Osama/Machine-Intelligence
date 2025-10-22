from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    ## need to increase the time limit
    #TODO: ADD YOUR CODE HERE
    frontier=deque()# it is a queue
    explored=[]# it is a graph version so need explored
    # check if the initail state is the goal return empty path
    if problem.is_goal(initial_state):
        return[]
    frontier.append((initial_state,[]))# add the initial state and the path
    while True:
        # check if is no node return None
        if len(frontier)==0:
            return None
        # get node , path from frontier
        node,path=frontier.popleft()
        # add it to explored to not check it again
        explored.append(node)
        # get all actions
        actions=problem.get_actions(node)
        for action in actions:
            # get the successor
            successor=problem.get_successor(node,action)
            # check if it not explored before on in the frontier
            if successor not in explored and all(successor !=s[0] for s in frontier):
                if problem.is_goal(successor):
                    return path+[action]
                frontier.append((successor,path+[action]))
            
                
                
            
        

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    NotImplemented()
    

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    NotImplemented()

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    NotImplemented()

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    NotImplemented()