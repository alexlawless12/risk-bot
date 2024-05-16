import random
from risktools import *
from gui.aihelper import *
from gui.turbohelper import *


def getAction(state, config, time_left=None):
    weights = config.get("weights", {})

    # Finds all possible actions and stores them in a list
    actions = getAllowedActions(state)

    # Attack logic
    if state.turn_type == "Attack":
        return getAttackAction(state, actions)

    # Place logic
    if state.turn_type == "Place":
        return getPlaceAction(state, actions)

    # Occupy logic
    if state.turn_type == "Occupy":
        return getOccupyAction(state, actions)

    # PrePlace logic
    if state.turn_type == "PrePlace":
        return getPrePlaceAction(state, actions)

    # Fortify logic
    if state.turn_type == "Fortify":
        return getFortifyAction(state, actions)

    # If it is none of these turn types, returns a random action
    return random.choice(actions)


def getAttackAction(state, actions):
    # For each possible attack, calculates the ratio of armies on our territory to armies on enemy territory
    # It attacks the highest ratio first, and it won't attack if the ratio is less than 2 so it doesn't spread too thin
    max_ratio = 0.0
    best_action = actions[0]
    for a in actions:
        cur_ratio = 0.0
        territory_attacked_id, territory_attacked = a.to_territory, None
        territory_attacked_from_id, territory_attacked_from = a.from_territory, None
        for t in state.board.territories:
            if t.name == territory_attacked_id:
                territory_attacked = t
        for t in state.board.territories:
            if t.name == territory_attacked_from_id:
                territory_attacked_from = t
        if territory_attacked is None:
            break
        cur_ratio = state.armies[territory_attacked_from.id] / \
            state.armies[territory_attacked.id]
        if cur_ratio > max_ratio:
            max_ratio = cur_ratio
            best_action = a
        if cur_ratio < 2.0:
            return actions[len(actions)-1]

    return best_action


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


def getOccupyAction(state, actions):
    # Moves the maximum amount of troops from the conquering territory to the conquered territory
    max_troops, num_troops, best_action = 0, 0, None
    for a in actions:
        num_troops = a.troops
        if num_troops > max_troops:
            max_troops = num_troops
            best_action = a
    return best_action


def getPrePlaceAction(state, actions):
    # After all territories have been assigned, we stack troops in one of our territories to prepare for attack
    territory = None
    for t, p in enumerate(state.owners):
        if p == state.current_player:
            territory = t
    for a in actions:
        if a.to_territory == territory:
            return a
    return random.choice(actions)


def getFortifyAction(state, actions):
    # Create a list of all actions that move troops to a territory bordering an opponent
    possible_actions = []
    myaction = random.choice(actions)
    for a in actions:
        if a.to_territory is not None:
            for n in state.board.territories[state.board.territory_to_id[a.to_territory]].neighbors:
                if state.owners[n] != state.current_player:
                    possible_actions.append(a)

    # Randomly select one of these actions, if there were any
    if len(possible_actions) > 0:
        myaction = random.choice(possible_actions)

    return myaction


# Need below code for GUI


def aiWrapper(function_name, config, occupying=None):
    game_board = createRiskBoard()
    game_state = createRiskState(game_board, function_name, occupying)
    action = getAction(game_state, config)
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
