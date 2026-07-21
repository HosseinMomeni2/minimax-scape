from math import inf

from neon_hunt.config import AGENT_PLAYER, AGENT_MONSTER
from neon_hunt.engine import bfs_distance, escape_routes
from neon_hunt.ai.student_support import get_possible_moves, apply_move, is_terminal


def evaluate(state):
    """Return a score from the Player/Hacker perspective.

    Higher is better for the player.

    Suggested ideas:
    - PLAYER_WIN should be a very large positive score.
    - MONSTER_WIN should be a very large negative score.
    - Being closer to the exit is good.
    - Being farther from the monster is good.
    - Having more escape routes is good.
    """
    result = is_terminal(state)
    if result == "PLAYER_WIN":
        return 100000.0
    if result == "MONSTER_WIN":
        return -100000.0

    d_exit = bfs_distance(state, state.player, state.exit)
    d_monster = bfs_distance(state, state.player, state.monster)
    d_monster_exit = bfs_distance(state, state.monster, state.exit)
    routes = escape_routes(state, state.player)

    mul_exit = -11.0
    mul_monster = 6.0
    mul_monster_exit = 9.0
    mul_routes = 3.0

    return float(mul_exit * d_exit +
                 mul_monster * d_monster +
                 mul_monster_exit * d_monster_exit +
                 mul_routes * routes)


def minimax(state, depth: int, maximizing_player: bool, stats=None):
    """Depth-limited Minimax from the Player's perspective."""

    ### base case
    if (is_terminal(state) != "ONGOING" or depth == 0):
        return 0.99 * evaluate(state), list()
    
    if stats is None:
        stats = {}

    ### maximizing player:
    if maximizing_player:
        max_val = -inf
        best_move = None
        best_variation = list()
        moves = get_possible_moves(state, AGENT_PLAYER)

        if not moves:
            return evaluate(state), list()
        
        for move in moves:
            stats["states_explored"] = stats.get("states_explored", 0) + 1

            new_state = apply_move(state, move, AGENT_PLAYER)
            new_value, new_variation = minimax(new_state, depth-1, not maximizing_player, stats)

            if new_value > max_val:
                max_val, best_move = new_value, move
                best_variation = new_variation.copy()
        
        best_variation.append(best_move)
        return 0.99 * max_val, best_variation
    
    ### minimizing player:
    else:
        min_val = inf
        best_move = None
        best_variation = list()
        moves = get_possible_moves(state, AGENT_MONSTER)

        if not moves:
            return evaluate(state), list()
        
        for move in moves:
            stats["states_explored"] = stats.get("states_explored", 0) + 1

            new_state = apply_move(state, move, AGENT_MONSTER)
            new_value, new_variation = minimax(new_state, depth-1, not maximizing_player, stats)

            if new_value < min_val:
                min_val, best_move = new_value, move
                best_variation = new_variation.copy()
        
        best_variation.append(best_move)
        return 0.99 * min_val, best_variation


def alpha_beta(state, depth, alpha, beta, maximizing_player, stats=None):
    """Minimax with alpha-beta pruning from the Player's perspective."""
    
    ### base case
    if (is_terminal(state) != "ONGOING" or depth == 0):
        return 0.99 * evaluate(state), list()
    
    if stats is None:
        stats = {}
    
    ### maximizing player:
    if maximizing_player:
        m_cnt = 0
        max_val = -inf
        best_move = None
        best_variation = list()
        moves = get_possible_moves(state, AGENT_PLAYER)

        if not moves:
            return evaluate(state), list()
        
        for move in moves:
            stats["states_explored"] = stats.get("states_explored", 0) + 1
            m_cnt += 1
            
            new_state = apply_move(state, move, AGENT_PLAYER)
            new_value, new_variation = alpha_beta(new_state, depth-1, alpha, beta, not maximizing_player, stats)
            
            if new_value > max_val:
                max_val, best_move = new_value, move
                best_variation = new_variation.copy()
                alpha = max(alpha, max_val)
            
            if max_val >= beta:
                stats["pruned_branches"] = stats.get("pruned_branches", 0) + len(moves) - m_cnt
                best_variation.append(best_move)
                
                return 0.99 * max_val, best_variation
        
        best_variation.append(best_move)
        return max_val, best_variation
    
    ### minimizing player:
    else:
        m_cnt = 0
        min_val = inf
        best_move = None
        best_variation = list()
        moves = get_possible_moves(state, AGENT_MONSTER)

        if not moves:
            return evaluate(state), list()

        for move in moves:
            stats["states_explored"] = stats.get("states_explored", 0) + 1
            m_cnt += 1
            
            new_state = apply_move(state, move, AGENT_MONSTER)
            new_value, new_variation = alpha_beta(new_state, depth-1, alpha, beta, not maximizing_player, stats)

            if new_value < min_val:
                min_val, best_move = new_value, move
                best_variation = new_variation.copy()
                beta = min(beta, min_val)
            
            if min_val <= alpha:
                stats["pruned_branches"] = stats.get("pruned_branches", 0) + len(moves) - m_cnt
                best_variation.append(best_move)
                
                return min_val, best_variation
        
        best_variation.append(best_move)
        return 0.99 * min_val, best_variation


def choose_player_move(state, depth, use_alpha_beta=True):
    """Choose the Player/Hacker move using minimax or alpha-beta.

    Return format:
    {
        "best_move": "UP",
        "scores": {"UP": 1.2, "DOWN": -5.0},
        "states_explored": 42,
        "pruned_branches": 7,
        "principal_variation": []
    }
    """

    otp = {"best_move": None,
           "scores": {},
           "states_explored": 0,
           "pruned_branches": 0,
           "principal_variation": []}

    moves = get_possible_moves(state, AGENT_PLAYER)
    if not moves:
        return otp

    best_val = -inf
    best_move = None
    best_stats = {}
    principal_variation = list()
    
    for move in moves:
        new_state = apply_move(state, move, AGENT_PLAYER)
        new_stats = {}

        if use_alpha_beta:
            new_val, new_variation = alpha_beta(new_state, depth, -inf, inf, False, new_stats)
        else:
            new_val, new_variation = minimax(new_state, depth, False, new_stats)

        if new_val > best_val:
            best_val = new_val
            best_move = move
            best_stats = new_stats.copy()
            principal_variation = new_variation.copy()
        
        otp["scores"][move] = new_val

    otp["best_move"] = best_move
    otp["states_explored"] = best_stats.get("states_explored", 0)
    otp["pruned_branches"] = best_stats.get("pruned_branches", 0)
    otp["principal_variation"] = principal_variation[::-1] # reverse

    return otp