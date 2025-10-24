from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented

# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    cache = problem.cache()
    
    # create a cache key based on crate positions only
    # using frozenset because it's hashable and order-independent
    # this allows us to avoid recomputing the heuristic for identical crate configurations
    cache_key = frozenset(state.crates)
    if cache_key in cache:
        return cache[cache_key]
    
    # convert goals to a list for easier iteration
    # goals are the target positions where crates need to be placed
    goals_list = list(state.layout.goals)
    
    # calculate the sum of minimum Manhattan distances
    # this heuristic estimates the minimum cost to move all crates to goals
    total = 0
    for crate in state.crates:
        # for each crate, find the minimum Manhattan distance to any goal
        # this is admissible because it's the minimum possible moves needed
        # without considering obstacles or other crates
        min_dist = min(abs(crate.x - g.x) + abs(crate.y - g.y) for g in goals_list)
        total += min_dist
    
    # Store the result in cache for future use
    cache[cache_key] = total
    return total
