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
    frontier = [] # priority queue
    explored = set() # to keep track of explored states
    counter = 0 # to break ties in the priority queue by giving index to each entry
    
    initial_h = heuristic(problem, initial_state) # heuristic cost for the initial state

    # push initial state to frontier: (f_cost, counter, state, path, g_cost)
    # here f_cost = g_cost + h_cost; for initial state, g_cost = 0
    heapq.heappush(frontier, (initial_h, counter, initial_state, [], 0))
    counter += 1
    
    while frontier:
        # pop the node with the lowest f_cost
        f_cost, _, state, path, g_cost = heapq.heappop(frontier)
        
        # if the state has already been explored, skip it
        if state in explored:
            continue
            
        # if the state is a goal, return the path
        if problem.is_goal(state):
            return path

        # mark the state as explored
        explored.add(state)
        
        # for all possible actions from the current state
        for action in problem.get_actions(state):
            # get the successor state
            successor = problem.get_successor(state, action)

            # if the successor has been explored, we ignore it
            # because if we calculated the f(A->B) then we don't care about f(B->A), it might be even worse
            if successor not in explored:
                action_cost = problem.get_cost(state, action) # get the cost of the current action
                new_g_cost = g_cost + action_cost # total cost from start to successor = current path cost + this action's cost
                new_h_cost = heuristic(problem, successor)
                new_f_cost = new_g_cost + new_h_cost # f_cost = g_cost + h_cost
                new_path = path + [action]
                
                heapq.heappush(frontier, (new_f_cost, counter, successor, new_path, new_g_cost))
                counter += 1 # increment counter for tie-breaking
    
    return None
    

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # same as A* but f_cost = h_cost only
    frontier = []
    explored = set()
    counter = 0
    
    initial_h = heuristic(problem, initial_state)
    # push initial state to frontier: (f_cost, counter, state, path)
    heapq.heappush(frontier, (initial_h, counter, initial_state, []))
    counter += 1
    
    while frontier:
        f_cost, _, state, path = heapq.heappop(frontier)
        
        if state in explored:
            continue
            
        if problem.is_goal(state):
            return path
            
        explored.add(state)
        
        for action in problem.get_actions(state):
            successor = problem.get_successor(state, action)
            
            if successor not in explored:
                new_h_cost = heuristic(problem, successor)
                new_f_cost =  new_h_cost # f_cost = h_cost only
                new_path = path + [action]
                
                heapq.heappush(frontier, (new_f_cost, counter, successor, new_path))
                counter += 1
    
    return None