from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
from typing import Optional

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def minimax_search(current_state: S, depth: int) -> Tuple[float, Optional[A]]:
        # Check if current state is terminal
        terminal, values = game.is_terminal(current_state)
        if terminal:
            return values[0], None
        
        # Check depth limit
        if depth == max_depth and max_depth != -1:
            return heuristic(game, current_state, 0), None
        
        current_player = game.get_turn(current_state)
        actions = game.get_actions(current_state)
        
        # Initialize best value based on player type
        if current_player == 0:  # Max player
            best_value = float('-inf')
            best_action = None
            for action in actions:
                next_state = game.get_successor(current_state, action)
                value, _ = minimax_search(next_state, depth + 1)
                if value > best_value:
                    best_value = value
                    best_action = action
            return best_value, best_action
        else:  # Min player
            best_value = float('inf')
            best_action = None
            for action in actions:
                next_state = game.get_successor(current_state, action)
                value, _ = minimax_search(next_state, depth + 1)
                if value < best_value:
                    best_value = value
                    best_action = action
            return best_value, best_action
    
    return minimax_search(state, 0)

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def alpha_beta_search(current_state: S, current_depth: int, alpha: float, beta: float) -> Tuple[float, Optional[A]]:
        # Check if state is terminal
        terminal_status, terminal_values = game.is_terminal(current_state)
        if terminal_status:
            return terminal_values[0], None
        
        # Check depth limit
        if current_depth == max_depth and max_depth != -1:
            return heuristic(game, current_state, 0), None
        
        current_player = game.get_turn(current_state)
        possible_moves = game.get_actions(current_state)
        
        best_move = None
        # Max player logic
        if current_player == 0:
            current_max = float('-inf')
            for move in possible_moves:
                child_state = game.get_successor(current_state, move)
                child_value, _ = alpha_beta_search(child_state, current_depth + 1, alpha, beta)
                if child_value > current_max:
                    current_max = child_value
                    best_move = move
                # Update alpha and check for pruning
                alpha = max(alpha, current_max)
                if current_max >= beta:
                    break  # Beta cutoff
            return current_max, best_move
        # Min player logic  
        else:
            current_min = float('inf')
            for move in possible_moves:
                child_state = game.get_successor(current_state, move)
                child_value, _ = alpha_beta_search(child_state, current_depth + 1, alpha, beta)
                if child_value < current_min:
                    current_min = child_value
                    best_move = move
                beta = min(beta, current_min)
                if current_min <= alpha:
                    break  # Alpha cutoff
            return current_min, best_move
    
    return alpha_beta_search(state, 0, float('-inf'), float('inf'))

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def ordered_alpha_beta(current_state: S, current_depth: int, alpha: float, beta: float) -> Tuple[float, Optional[A]]:
        terminal_check, terminal_scores = game.is_terminal(current_state)
        if terminal_check:
            return terminal_scores[0], None
        
        if current_depth == max_depth and max_depth != -1:
            return heuristic(game, current_state, 0), None
        
        player_turn = game.get_turn(current_state)
        action_list = game.get_actions(current_state)
        
        # Create move-state pairs with heuristic scores for ordering
        move_states = []
        for action in action_list:
            next_state = game.get_successor(current_state, action)
            move_states.append((action, next_state))
        
        # Sort moves based on heuristic (good moves first)
        if player_turn == 0:  # Sort high to low
            move_states.sort(key=lambda x: heuristic(game, x[1], 0), reverse=True)
        else:  # Sort low to high
            move_states.sort(key=lambda x: heuristic(game, x[1], 0))
        
        optimal_action = None
        if player_turn == 0:
            max_eval = float('-inf')
            for action, next_state in move_states:
                eval_score, _ = ordered_alpha_beta(next_state, current_depth + 1, alpha, beta)
                if eval_score > max_eval:
                    max_eval = eval_score
                    optimal_action = action
                alpha = max(alpha, max_eval)
                # Prune if possible
                if max_eval >= beta:
                    break
            return max_eval, optimal_action
        # Min node processing
        else:
            min_eval = float('inf')
            for action, next_state in move_states:
                eval_score, _ = ordered_alpha_beta(next_state, current_depth + 1, alpha, beta)
                if eval_score < min_eval:
                    min_eval = eval_score
                    optimal_action = action
                beta = min(beta, min_eval)
                # Prune if possible
                if min_eval <= alpha:
                    break
            return min_eval, optimal_action
    
    return ordered_alpha_beta(state, 0, float('-inf'), float('inf'))

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def expectimax_search(current_state: S, current_depth: int) -> Tuple[float, Optional[A]]:
        is_terminal, terminal_values = game.is_terminal(current_state)
        if is_terminal:
            return terminal_values[0], None
        
        if current_depth == max_depth and max_depth != -1:
            return heuristic(game, current_state, 0), None
        
        current_agent = game.get_turn(current_state)
        legal_actions = game.get_actions(current_state)
        
        # Maximize
        if current_agent == 0:
            maximum_score = float('-inf')
            selected_action = None
            for action in legal_actions:
                successor = game.get_successor(current_state, action)
                score, _ = expectimax_search(successor, current_depth + 1)
                if score > maximum_score:
                    maximum_score = score
                    selected_action = action
            return maximum_score, selected_action
        # Expect average
        else:
            total_score = 0.0
            action_count = len(legal_actions)
            for action in legal_actions:
                successor = game.get_successor(current_state, action)
                score, _ = expectimax_search(successor, current_depth + 1)
                total_score += score
            # Return average score (no action choice for chance nodes)
            return total_score / action_count, None
    
    return expectimax_search(state, 0)