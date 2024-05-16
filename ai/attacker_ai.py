import random
from risktools import *
# For interacting with interactive GUI
from gui.aihelper import *
from gui.turbohelper import *


### ATTACKER AI ####
#
#  This AI always chooses to attack if it is possible
#  Complete description for all turn types:
#    - PreAssign - Chooses territories randomly
#    - PrePlace, Place - Places troops on random territory that is bordering an opponent territory (a front)
#    - Occupy - Chooses random action
#    - Fortify - Chooses random action that moves troops to front
#    - TurnInCards - Chooses random action
#
#  This results in an AI that is very aggressive and fairly successful.  Not trivial to beat this agent a significant portion of the time


def getAction(state, config, time_left=None):
    """Main AI function.  It should return a valid AI action for this state."""

    # Get the possible actions in this state
    actions = getAllowedActions(state)

    # Select a Random Action (to use for unspecified turn types)
    myaction = random.choice(actions)

    if state.turn_type == 'Attack':
        # The final action in the list will be the "stop attacking" action, so this will always choose to attack if possible
        myaction = actions[0]

    # Return the chosen action
    return myaction


# Code below this is the interface with Risk.pyw GUI version
# DO NOT MODIFY


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
