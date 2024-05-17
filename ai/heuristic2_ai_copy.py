import random
from risktools import *
from gui.aihelper import *
from gui.turbohelper import *


def getAction(state, config, time_left=None):
    weights = config.get("weights", {})

    # Finds all possible actions and stores them in a list
    actions = getAllowedActions(state)

    # Fortify logic
    if state.turn_type == "Preassign":
        return getPreAssignAction(state, weights, actions)

    # Attack logic
    if state.turn_type == "Attack":
        return getAttackAction(state, weights, actions)

    # Place logic
    if state.turn_type == "Place":
        return getPlaceAction(state, weights, actions)

    # Occupy logic
    if state.turn_type == "Occupy":
        return getOccupyAction(state, weights, actions)

    # PrePlace logic
    if state.turn_type == "PrePlace":
        return getPrePlaceAction(state, weights, actions)

    # Fortify logic
    if state.turn_type == "Fortify":
        return getFortifyAction(state, weights, actions)

    # If it is none of these turn types, returns a random action
    return random.choice(actions)


def getAttackAction(state, weights, actions):
    weight_aggression = weights.get("weight_aggression")
    weight_attack_risk = weights.get("weight_attack_risk")
    max_ratio = 0.0
    best_action = actions[0]
    for a in actions:
        cur_ratio = 0.0
        territory_attacked_id = state.board.territory_to_id.get(a.to_territory)
        territory_attacked_from_id = state.board.territory_to_id.get(
            a.from_territory)
        if territory_attacked_id is None or territory_attacked_from_id is None:
            continue
        cur_ratio = state.armies[territory_attacked_from_id] / \
            state.armies[territory_attacked_id]
        risk_adjusted_ratio = cur_ratio * weight_attack_risk
        if risk_adjusted_ratio > max_ratio:
            max_ratio = risk_adjusted_ratio
            best_action = a
    return best_action


def getPreAssignAction(state, weights, actions):
    continent_weight = weights.get("weight_continent")
    weight_continent_control = weights.get("weight_continent_control")

    def calculate_score(action):
        territory_id = action.to_territory
        for continent_name, continent in state.board.continents.items():
            if territory_id in continent.territories:
                owned_territories = sum(
                    1 for t in continent.territories if state.owners[t] == state.current_player)
                total_territories = len(continent.territories)
                completion_ratio = owned_territories / total_territories
                control_score = (completion_ratio *
                                 continent_weight) + weight_continent_control
                return control_score
        return 0

    best_action = None
    best_score = -float('inf')

    for action in actions:
        score = calculate_score(action)
        if score > best_score:
            best_score = score
            best_action = action

    if best_action is None:
        for t, p in enumerate(state.owners):
            if p == state.current_player:
                territory = t
                for action in actions:
                    if action.to_territory == territory:
                        return action

    return best_action if best_action else random.choice(actions)


def getPlaceAction(state, actions):
    # Places troops at the territory that borders the most opponent territories
    max_opponent_count, best_action = 0, None

    cur_territory = None
    for a in actions:
        opponent_count = 0
        territory_name = a.to_territory
        territory_id = state.board.territory_to_id[territory_name]

        for territory in state.board.territories:
            if territory.id == territory_id:
                cur_territory = territory

        for neighbor in cur_territory.neighbors:
            if state.owners[neighbor] != state.current_player:
                opponent_count += 1

        if opponent_count > max_opponent_count:
            best_action = a

    return best_action


def getOccupyAction(state, weights, actions):
    weight_troops = weights.get("weight_troops")
    max_troops, best_action = 0, None
    for a in actions:
        num_troops = a.troops
        if num_troops > max_troops:
            max_troops = weight_troops * num_troops
            best_action = a
    return best_action


def getPrePlaceAction(state, weights, actions):
    continent_weight = weights.get("weight_continent")
    weight_continent_control = weights.get("weight_continent_control")

    def calculate_score(action):
        territory_id = action.to_territory
        for continent_name, continent in state.board.continents.items():
            if territory_id in continent.territories:
                owned_territories = sum(
                    1 for t in continent.territories if state.owners[t] == state.current_player)
                total_territories = len(continent.territories)
                completion_ratio = owned_territories / total_territories
                control_score = (completion_ratio *
                                 continent_weight) + weight_continent_control
                return control_score
        return 0

    best_action = None
    best_score = -float('inf')

    for action in actions:
        score = calculate_score(action)
        if score > best_score:
            best_score = score
            best_action = action

    if best_action is None:
        for t, p in enumerate(state.owners):
            if p == state.current_player:
                territory = t
                for action in actions:
                    if action.to_territory == territory:
                        return action

    return best_action if best_action else random.choice(actions)


def getFortifyAction(state, weights, actions):
    weight_fortify_proximity = weights.get("weight_fortify_proximity", 1.0)
    possible_actions = []
    for a in actions:
        if a.to_territory is not None:
            for n in state.board.territories[state.board.territory_to_id[a.to_territory]].neighbors:
                if state.owners[n] != state.current_player:
                    proximity_score = weight_fortify_proximity
                    possible_actions.append((a, proximity_score))

    if possible_actions:
        return max(possible_actions, key=lambda x: x[1])[0]
    return random.choice(actions)

# GUI integration


def aiWrapper(function_name, config, occupying=None):
    game_board = createRiskBoard()
    game_state = createRiskState(game_board, function_name, occupying)
    action = getAction(game_state, config)
    return translateAction(game_state, action)


def Assignment(player):
    return aiWrapper('Assignment', player.config)


def Placement(player):
    return aiWrapper('Placement', player.config)


def Attack(player):
    return aiWrapper('Attack', player.config)


def Occupation(player, t1, t2):
    occupying = [t1.name, t2.name]
    return aiWrapper('Occupation', player.config, occupying)


def Fortification(player):
    return aiWrapper('Fortification', player.config)
