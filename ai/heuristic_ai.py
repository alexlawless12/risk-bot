import random
from risktools import *
from gui.aihelper import *
from gui.turbohelper import *


def getAction(state, time_left=None):

    actions = getAllowedActions(state)
    my_action, my_action_value = None, None
    for action in actions:
        # Simulate the future states of the action and get probabilities
        possible_states, probabilities = simulateAction(state, action)

        current_value = 0.0
        for i in range(len(possible_states)):
            # Get the value of the state
            current_value += (probabilities[i] *
                              heuristicEvaluation(possible_states[i]))

        if my_action is None or current_value > my_action_value:
            my_action = action
            my_action_value = current_value

    return my_action


def heuristicEvaluation(state):
    heuristic_value = 0.0

    weight_territories_owned = 0.4
    weight_armies_fraction = 0.3
    weight_border_protection = 0.3

    # Finds number of territories current player owns
    territories_owned = len(
        [territory for territory in state.owners if territory == state.current_player])

    # Finds the fraction of current player's armies over all armies on the board
    armies = calculate_player_army_fraction(state)

    # Finds how well the current player has their bordering territories protected
    border_score = calculate_border_protection_score(state)

    heuristic_value = (weight_territories_owned * territories_owned) + (
        weight_armies_fraction * armies) + (weight_border_protection * border_score)

    return heuristic_value


def calculate_player_army_fraction(state):
    current_player_id = state.current_player

    # Calculate total armies on the board
    total_armies = sum(state.armies)

    # Find the current player's armies
    current_player_armies = sum(armies for owner_id, armies in enumerate(
        state.armies) if owner_id == current_player_id)

    # Calculate fraction
    if total_armies == 0:
        return 0  # Avoid division by zero
    else:
        fraction = current_player_armies / total_armies
        return fraction


def calculate_border_protection_score(state):
    current_player_id = state.current_player
    border_protection_score = 0

    # Iterate through each territory
    for territory_id, owner_id in enumerate(state.owners):
        territory = state.board.territories[territory_id]
        # Check if the territory is owned by the current player and borders an enemy territory
        if owner_id == current_player_id and any(state.owners[neighbor_id] != current_player_id for neighbor_id in territory.neighbors):
            # Calculate the protection score for the border territory
            # Initial protection score is the number of armies on the territory
            protection_score = state.armies[territory_id]

            # Consider the proximity of enemy territories
            for neighbor_id in territory.neighbors:
                if state.owners[neighbor_id] != current_player_id:
                    # Reduce protection score if neighboring territory is owned by an enemy
                    # Subtract the number of enemy armies from protection score
                    protection_score -= state.armies[neighbor_id]

            # Add the protection score for this border territory to the total score
            # Ensure protection score is non-negative
            border_protection_score += max(protection_score, 0)

    return border_protection_score


# Need below code for GUI


def aiWrapper(function_name, occupying=None):
    game_board = createRiskBoard()
    game_state = createRiskState(game_board, function_name, occupying)
    action = getAction(game_state)
    return translateAction(game_state, action)


def Assignment(player):
    # Need to Return the name of the chosen territory
    return aiWrapper('Assignment')


def Placement(player):
    # Need to return the name of the chosen territory
    return aiWrapper('Placement')


def Attack(player):
 # Need to return the name of the attacking territory, then the name of the defender territory
    return aiWrapper('Attack')


def Occupation(player, t1, t2):
 # Need to return the number of armies moving into new territory
    occupying = [t1.name, t2.name]
    return aiWrapper('Occupation', occupying)


def Fortification(player):
    return aiWrapper('Fortification')
