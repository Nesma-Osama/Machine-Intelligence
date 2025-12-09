from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        # check terminal state
        if self.mdp.is_terminal(state):
            return 0
        # get all actions
        actions = self.mdp.get_actions(state)
        # max_utility its initially -infinity
        max_utility = float('-inf')
        for action in actions:
           # get all states that achieve from action
           next_states = self.mdp.get_successor(state, action)
           # sum(p(s'|s,a)[ R(s,a,s') + gamma*U(s') ])
           # summation initially to 0
           sum_utility = 0
           # calculate the equation
           for next_state, prob in next_states.items():
               sum_utility+=prob*(self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state])
            # update max_utility if sum_utility is greater
           if sum_utility > max_utility:
                max_utility = sum_utility
        return max_utility
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function
        # get all states
        states=self.mdp.get_states()
        changed_states={}
        max_change=float('-inf')
        # loop over all states
        for state in states:
            # call the compute bellman function
            new_utility=self.compute_bellman(state)
            # add it to changed_states
            changed_states[state]=new_utility
            # check if the change is greater than tolerance
            change=abs(new_utility - self.utilities[state])
            if change > max_change:
                max_change=change
        # update utilities
        self.utilities=changed_states
        # check convergence
        if max_change <= tolerance:
            return True
        else:   
            return False                
                
    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        #TODO: Complete this function to apply value iteration for the given number of iterations
        for i in range(iterations):
            # call update function
            converged=self.update(tolerance)
            # check convergence
            if converged:
                return i+1
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        # check terminal state
        if self.mdp.is_terminal(state):
            return None
        # get all actions
        actions = self.mdp.get_actions(state)
        # best_action initially None
        best_action = None
        max_utility = float('-inf')
        for action in actions:
            # get all states that achieve from action
            next_states = self.mdp.get_successor(state, action)
            # sum(p(s'|s,a)[ R(s,a,s') + gamma*U(s') ])
            # summation initially to 0
            sum_utility = 0
            # calculate the equation
            for next_state, prob in next_states.items():
                sum_utility += prob * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state])
            # update best_action if sum_utility is greater
            if sum_utility > max_utility:
                max_utility = sum_utility
                best_action = action
        return best_action
        
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
