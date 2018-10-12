# Implementation  of Q-learning
# again for 3x3 matrix is the starting point
# version 3.1 is to use exploration and exploitation technique with Q-learning
import numpy as np
#import ipdb
import time
from Error import qError
import random
from Dummy import generateDummy
from copy import deepcopy
import pinSetup
import GoToHome
import action_22 as act
import generate_rewardmatrix
import gotopos
import initvalact
import qinitial
epsilon = 0.7
bita = 1/2
lamda = 1/2
gama = 0.7  # discount factor assuming to be 0.9
# 0 = up / 1 = down / 2 = left / 3= right
# Here Q function is also function of state and actions

pinVar = pinSetup.pinSetup()
p = pinVar[0]
p1 = pinVar[1]
encoder = pinVar[2]
ENClast = pinVar[3]
p.start(3.0)
p1.start(3.0)
GoToHome.GoToHome(p, p1)


def epsilon_greedy_policy(Q, actions, epsilon):
    '''
    Create a policy in which epsilon dictates how likely it will
    take a random action.

    :param q: Q values of the perticular state
    :param nA: number of actions (int)
    :param epsilon: chance it will take a random move (float)
    :return: probability of each action to be taken (list)
    '''
    q = []
    maxind = []
    temp = 0
    for action in actions:
        q.append(Q[action])
    nA = len(actions)
    maxval = max(q)
    for temp in range(len(q)):
        if maxval == q[temp]:
            maxind.append(temp)
    if len(maxind) == 1:
        probs = np.ones(nA) * epsilon / nA
        best_action = np.argmax(q)
        probs[best_action] += 1.0 - epsilon
    else:
        probs = np.ones(nA) * epsilon / nA
        for temp in range(len(q)):
            if temp in maxind:
                probs[temp] += (1.0 - epsilon)/len(maxind)
    return probs


def action_select(raw, col, n):
    # action selection according to selction of state
    if raw == 0 and col == 0:
        return [1, 3]
    elif raw == 0 and (col == -1 or col == n-1):
        return [1, 2]
    elif raw == 0:
        return [1, 2, 3]

    elif raw == n-1 and col == 0:
        return [0, 3]
    elif raw == n-1 and (col == -1 or col == n-1):
        return [0, 2]
    elif raw == n-1:
        return [0, 2, 3]

    elif col == 0:
        return [0, 1, 3]
    elif (col == -1 or col == n-1):
        return [0, 1, 2]

    else:
        return [0, 1, 2, 3]  # cells where all four actions are possible


def qLearning(n, p, p1, encoder, ENClast):
    epsilon = 0.7
    v = initvalact.initvalact(n)
    Q = qinitial.qinitial(n)
    '''Q = [[[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],  # State1,State2, Stete3
         [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],  # State4, State5, State6
         [[1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0]]]  # State7, State8, State9'''
    kMatrix = qinitial.qinitial(n)
    Tr = qinitial.qinitial(n)
    a = v[1]
    size = np.shape(Q)  # storing size of Q-matrix
    n = size[0]
    Qlast = generateDummy(Q)  # generating dummy of same sizq as Q to enter the while loop
    iteration = 0  # initializing the iteration
    reward = generate_rewardmatrix.generate_rewardmatrix(n)
    state = random.randint(1, size[0] * size[1])
    while qError(Q, Qlast) > 1.5 or Q == Qlast or iteration <= 100:
        iteration += 1  # incresing iteration value
	if iteration > 60:
	    epsilon = 0.1
        Qlast = deepcopy(Q)  # copying Q to Qlast
        # state =  selecting state randomly 1every time depending on the Q size
        # temp = to retrive raw and column from Nos of state generated by random selector
        # state / Nos.of column will give us information about the raw number...
        # for 3x4 (raw x column) state 1 to 4 are raw in 1 and state 5 to 8 are raw in 2
        # for raw1(state 1 to 4)/4 (total columns) will be 0 < temp <= 1
        # for raw1(state 5 to 8)/4 (total columns) will be 1 < temp <= 2
        if iteration == 1:
            temp = state / (size[1] * 1.0)  # defining a temporary variable
            if ((temp).is_integer()):
                raw = int(temp) - 1
            else:
                raw = int(temp)
            # temp = modulo of state and Total column
            # for column1(state 1,5,9) % 4 (total columns) will be 1 [i.e colum = 1-1 = 0]
            # for column1(state 2,6,10) % 4 (total columns) will be 2 [i.e colum = 2-1 = 1]
            temp = state % size[1]
            col = temp - 1
            if col < 0:
                col = size[1] - 1
            else:
                pass
            gotopos.gotopos(raw, col, p, p1, n)  # to go to state that is selected randomly
            time.sleep(0.3)

        possibleActions = action_select(raw, col, n)
        probablity = epsilon_greedy_policy(Q[raw][col], possibleActions, epsilon)
        actionIndex = np.random.choice(len(probablity), p=probablity)
        action = possibleActions[actionIndex]
        # action selection according to selction of state
        '''
        -------------------------------------------------------------
        ***************REPLACED BY EPSILON GREDDY POLICY*************
        -------------------------------------------------------------
        if i < NumOfSelAct:
            possibleActions = action_select(raw, col, n)
            tempList = []
            for i in possibleActions:
                tempList.append(Q[raw][col][i])
            action = possibleActions[tempList.index(max(tempList))]
        else:
            possibleActions = action_select(raw, col, n)
            action = random.choice(possibleActions)
        -------------------------------------------------------------
        ***************REPLACED BY EPSILON GREDDY POLICY*************
        -------------------------------------------------------------
        '''

        # defining nextstate according to choosen action
        if action == 0:  # Up movement
            nextstate = Q[raw-1][col]
            rawtemp = raw - 1  # raw of nextstep
            coltemp = col  # col of nextstep
        elif action == 1:  # Down movememt
            nextstate = Q[raw+1][col]
            rawtemp = raw + 1  # raw of nextstep
            coltemp = col  # col of nextstep
        elif action == 2:  # Left movement
            nextstate = Q[raw][col-1]
            rawtemp = raw  # raw of nextstep
            coltemp = col - 1  # col of nextstep
        else:  # Right movement
            nextstate = Q[raw][col+1]
            rawtemp = raw  # raw of nextstep
            coltemp = col + 1  # col of nextstep
        # try executing the Q-iteration formula with no errors..
        '''
        _____ADD HERE____
        ACTION_PERFORMANCE FUNCTION
        UPDATE_REWARD FUNCTION
	'''
        ENClast= encoder.getData()
        act.playAction(action, raw, col, size[0], p, p1)
        time.sleep(0.1)
        if action == 0 or action == 1:
            ENClast= encoder.getData()
        ENC= encoder.getData()
        diff = ENC - ENClast
	oldreward = reward[raw][col][action]
        if (oldreward != 0 and diff == 0) or (np.sign(oldreward) != np.sign(diff) and oldreward != 0):
            #		restriCount[raw][col][action] += 1
            #		if restriCount[raw][col][action] < 3:
            print ("!! restriction applied !!")
            gotopos.gotopos(raw, col, p, p1, n)
            time.sleep(0.3)
            ENClast = encoder.getData()
            act.playAction(action, raw, col, size[0], p, p1)
            time.sleep(0.1)
            if action == 0 or action == 1:
                ENClast = encoder.getData()
            ENC = encoder.getData()
            diff = ENC - ENClast
        reward[raw][col][action] = diff
        # update_reward.update_reward(reward, raw, col, action, diff)

        kMatrix[raw][col][action] = kMatrix[raw][col][action] + 1

        try:
            alpha = 1/((kMatrix[raw][col][action])**bita)
            eComplement = reward[raw][col][action] + gama * max(nextstate) - Q[raw][col][action]
            e = reward[raw][col][action] + gama * max(nextstate) - max(Q[raw][col])
            for r in range(size[0]):
                for c in range(size[1]):
                    for actn in action_select(raw, col, n):
                        Tr[r][c][actn] = gama * lamda * Tr[r][c][actn]
                        Q[r][c][actn] = Q[r][c][actn] + alpha * Tr[r][c][actn] * e

            Q[raw][col][action] = Q[raw][col][action] + alpha * eComplement
            Tr[raw][col][action] += 1
        # tracking if there is a type error (i.e. datatype missmatch) or not in above equation
        except TypeError as e:
            print("TypeError")
        print possibleActions
        print probablity
        print "raw= ", raw, "col = ", col, "action = ", action
        raw = rawtemp
        col = coltemp
        print "qerror is", qError(Q, Qlast)
        print "reward is", reward
        print "iteration = ", iteration
    # getting the appropriate action back from the given calculated values of Q matrix
    print Tr
    print Q
    for r in range(0, size[0]):
        for c in range(0, size[1]):
            possibleActions = action_select(r, c, n)
            tempList = []
            for i in possibleActions:
                tempList.append(Q[r][c][i])
            a[r][c] = possibleActions[tempList.index(max(tempList))]
    # ipdb.set_trace()
    # function returns Q matrix, action matrix and nos of iteration
    return Q, a, iteration


# trial run of the function
trial = qLearning(3,p,p1,encoder,ENClast)
print(trial[0])
print("\n")
print(trial[1])
print("\n")
print(trial[2])
