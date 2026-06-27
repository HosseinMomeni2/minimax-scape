"""Student AI Template — Neon Hunt

IMPORTANT: Replace STUDENT_ID with your own 10-digit numeric student code.

Only these four functions are TODO for students:
1. evaluate
2. minimax
3. alpha_beta
4. choose_player_move

The game-rule helpers are already provided:
- get_possible_moves
- apply_move
- is_terminal
"""
# TODO: write your own 10-digit numeric student code here.
# Example: STUDENT_ID = "4021234567"
STUDENT_ID = "4023613071"

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
    routes = escape_routes(state, state.player)

    # TODO: improve this heuristic.
    return float(-6.0 * d_exit + 4.0 * d_monster + 2.0 * routes)


def minimax(state, depth: int, maximizing_player: bool, stats=None):
    """Depth-limited Minimax from the Player's perspective."""
    # TODO: implement minimax.
    # CAUTION: people at work.

    ### base case
    if(is_terminal(state) or depth==0):
        return evaluate(state)
    

    ###maximizing player:
    if maximizing_player:
        max_val = -inf
        moves = get_possible_moves(state, AGENT_PLAYER)
        for move in moves:
            new_state = apply_move(state, move, AGENT_PLAYER)
            max_val = max(minimax(new_state, depth-1, not maximizing_player, stats), max_val)
        return max_val
    
    ###minimizing player:
    else:
        min_val = inf
        moves = get_possible_moves(state, AGENT_MONSTER)
        for move in moves:
            new_state = apply_move(state, move, AGENT_MONSTER)
            min_val = min(minimax(new_state, depth-1, not maximizing_player, stats), min_val)
        return min_val


def alpha_beta(state, depth, alpha, beta, maximizing_player, stats=None):
    """Minimax with alpha-beta pruning from the Player's perspective."""
    # TODO: implement alpha-beta pruning.
    raise NotImplementedError("Implement alpha_beta(state, depth, alpha, beta, maximizing_player, stats=None)")


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
    otp = {"best_move": "",
           "scores": {},
           "states_explored": 0,
           "pruned_branches": 0,
           "principal_variation": []}

    moves = get_possible_moves(state, AGENT_PLAYER)
    if not moves:
        return {
            "best_move": None,
            "scores": {},
            "states_explored": 0,
            "pruned_branches": 0,
            "principal_variation": [],
        }

    # TODO: call alpha_beta or minimax for each candidate move and return best.
    best_move = moves[0]
    best_val = -inf
    for move in moves:
        new_state = apply_move(state, move, AGENT_PLAYER)
        new_val = minimax(new_state, depth, False)

        otp['scores'][move] = new_val

        if new_val > best_val:
            best_val = new_val
            best_move = move

    otp["best_move"] = best_move
    return otp