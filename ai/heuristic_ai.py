import random
from risktools import *
from gui.aihelper import *
from gui.turbohelper import *


def getAction(state, time_left=None):

    actions = getAllowedActions(state)
    my_action, my_action_value = None, None
    if state.turn_type == "Attack":
        return actions[0]

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

# def heuristicEvaluation(state, possible_state):
    
#     current_player = state.current_player
    
#     # Check if state.owners and possible_state.owners are not None
#     if state.owners is None or possible_state.owners is None:
#         return False
    
#     enemy_border_score_current, enemy_border_score_possible = 1, 0

#     if state.turn_type == "Place":
        
#         enemy_border_score_current = calculateEnemyBorderScore(state, current_player)
        
#         # Calculate enemy border score for the possible state
#         enemy_border_score_possible = calculateEnemyBorderScore(possible_state, current_player)

#     current_player_territories, possible_player_territories = 0, 1
#     if state.turn_type == "Attack":
#         # Count the number of territories owned by the current player in the current state
#         current_player_territories = sum(1 for t in state.owners if t is not None and state.owners[t] == current_player)
        
#         # Count the number of territories owned by the current player in the possible state
#         possible_player_territories = sum(1 for t in possible_state.owners if t is not None and possible_state.owners[t] == current_player)
    
#     # Check if the current player has more territories in the possible state compared to the current state
#     return 1 if (possible_player_territories > current_player_territories) and (enemy_border_score_possible > enemy_border_score_current) else 0

# def calculateEnemyBorderScore(state, current_player):
#     # Calculate enemy border score
#     enemy_border_score = 0
#     owned_territories = [t for t in state.owners if state.owners[t] == current_player]
#     for territory in owned_territories:
#         for neighbor in state.board.territories[territory].neighbors:
#             if state.owners[neighbor] != current_player:
#                 enemy_border_score += state.armies[territory] / len(owned_territories)
#     return enemy_border_score

def heuristicEvaluation(state):
    weight_territories_owned = 0.0
    weight_armies_fraction = 0.0
    weight_border_protection = 0.3
    weight_attack_vulnerability = 0.1
    weight_troop_distribution=0.3
    weight_strategic_importance = 0.4  # New weight for considering strategic importance of territories

    # Calculate the number of territories owned by the current player
    territories_owned = len([territory for territory in state.owners if territory == state.current_player])

    # Calculate the fraction of current player's armies over all armies on the board
    armies_fraction = calculate_player_army_fraction(state)

    # Calculate the protection score for the current player's bordering territories
    border_protection = calculate_border_protection_score(state)

    # Evaluate the behavior of the Attacker AI
    if state.turn_type == 'Attack':
        # The Attacker AI always chooses to attack if possible
        attack_score = 1.0  # Maximize attack score when the turn type is Attack
    else:
        # If the turn type is not Attack, assign a lower attack score
        attack_score = 0.0

    # Evaluate the behavior of the AI in distributing troops evenly
    troop_distribution_score = evaluate_troop_distribution(state)  # You need to define this function

    # Evaluate the strategic importance of territories
    strategic_importance_score = evaluate_strategic_importance(state)  # You need to define this function

    # Calculate the heuristic value as a weighted sum of all factors
    heuristic_value = (weight_territories_owned * territories_owned) + \
                      (weight_armies_fraction * armies_fraction) + \
                      (weight_border_protection * border_protection) + \
                      (weight_attack_vulnerability * attack_score) + \
                      (weight_strategic_importance * strategic_importance_score) + \
                      (weight_troop_distribution * troop_distribution_score)

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

def evaluate_troop_distribution(state):
    """
    Evaluate troop distribution across territories and encourage more aggressive troop concentration on front lines.
    """
    total_armies = sum(state.armies)
    num_territories = len(state.owners)

    # Calculate the average number of armies per territory
    avg_armies_per_territory = total_armies / num_territories

    # Calculate the standard deviation of armies per territory
    std_deviation = 0
    for armies in state.armies:
        std_deviation += (armies - avg_armies_per_territory) ** 2
    std_deviation = (std_deviation / num_territories) ** 0.5

    # Calculate the fraction of armies on front lines (territories bordering opponents)
    front_line_armies = sum(state.armies[territory_id] for territory_id, owner_id in enumerate(state.owners) if
                            any(state.owners[neighbor_id] != owner_id for neighbor_id in
                                state.board.territories[territory_id].neighbors))

    # Increase score for aggressive troop concentration on front lines
    aggressive_score = front_line_armies / total_armies

    # Return the aggressive score
    return aggressive_score


def evaluate_strategic_importance(state):
    """
    Evaluate the strategic importance of territories based on factors such as borders with opponents and potential for expansion.
    """
    strategic_importance_score = 0

    for territory_id, owner_id in enumerate(state.owners):
        territory = state.board.territories[territory_id]

        # Check if the territory borders an opponent
        if any(state.owners[neighbor_id] != owner_id for neighbor_id in territory.neighbors):
            # Increase strategic importance score for territories bordering opponents
            strategic_importance_score += 1

        # Consider other factors such as potential for expansion, proximity to continents, etc.

    return strategic_importance_score

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
