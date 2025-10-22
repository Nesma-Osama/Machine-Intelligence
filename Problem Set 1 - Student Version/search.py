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
    frontier=[]# stack 
    explored=[]# it is a graph representation
    frontier.append((initial_state,[]))# add the initail state
    while True:
        # if the frontier is empty
        if len(frontier)==0:
            return None
        # pop the node
        node,path=frontier.pop()
        explored.append(node)
        # check if the node is a goal
        if problem.is_goal(node):
            return path
        # get the actions
        actions=problem.get_actions(node)
        for action in actions:
            successor=problem.get_successor(node,action)
            if successor not in explored and all([successor!=s[0] for s in frontier]):
                frontier.append((successor,path+[action]))
            
        
    

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    frontier=[]
    explored=[]
    counter=0# if there are two path have the same total cost
    heapq.heappush(frontier,(0,counter,initial_state,[]))# add the initail state with cost =0 and empty path
    while True:
        # check if it is not empty
        if len(frontier)==0:
            return None
        # get the first node
        cost,_,node,path=heapq.heappop(frontier)
        # add it to explored
        explored.append(node)
        # if it is a goal
        if problem.is_goal(node):
            return path
        actions=problem.get_actions(node)
        for action in actions:
            successor=problem.get_successor(node,action)
            # if it is explored ignore it
            if successor in explored:
                continue
            # add the cost of the action
            new_cost=cost+problem.get_cost(node,action)
            # if it is not frontier add it
            if all(successor!=s[2] for s in frontier):
                counter+=1
                heapq.heappush(frontier,(new_cost,counter,successor,path+[action]))
            else:
                for i in range(len(frontier)):
                    if frontier[i][2]==successor:
                        if frontier[i][0]>new_cost:
                            frontier[i]=(new_cost,counter,successor,path+[action])
                            heapq.heapify(frontier)
        
def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    NotImplemented()

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    NotImplemented()