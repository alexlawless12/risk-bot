import random
from risktools import *
# For interacting with interactive GUI
from gui.aihelper import *
from gui.turbohelper import *

### RANDOM AI ####
#
#  This AI always will choose a random action
#  It does not necessarily attempt to win or end the game.


def getAction(state, config, time_left=None):
    """Main AI function.  It should return a valid AI action for this state."""

    # Get the possible actions in this state
    actions = getAllowedActions(state)

    # Select random action (to use for non-attack turn types)
    return random.choice(actions)

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
