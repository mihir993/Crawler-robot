'''
____________________________________________________________________________
This is main program that calls every other programs depending on switch logic
There are three Algorithms which are  used here namely:
1) Valueiteration   2) Q(λ)-Learning  3) Q-Learning
______________________________________________________________________________
'''


# ___________ impoering dependencies ___________ #

import Q_learning_V3_1 as qLearning
import qLamda_V1_2 as qLamda
import valueiteratingpolicy
import pinSetup
import GoToHome


# ___________ setting up GPIO pins ___________ #
#      for better idea go to pinSetup.py

pinVar = pinSetup.pinSetup()  # pinSetup method returns list
p = pinVar[0]  # pin to control first servo motor (movemet of first arm)
p1 = pinVar[1]  # pin to control second servo motor (movement of second arm)
encoder = pinVar[2]  # class object for encoder reading
ENClast = pinVar[3]  # variable to  store last encoder values
p.start(3.0)  # start first servo motor
p1.start(3.0)  # start second servo motor
GoToHome.GoToHome(p, p1)  # bring both motors to default position (home position)

val1 = pinSetup.valueRead_ON()  # ON/OFF switch value
val2 = pinSetup.valueRead_alg()  # Algorithm select switch
print (val1, val2)
while True:
    if val1 == 0:  # if switch is at ON position
        if val2 == "Value iteration":  # selecting algorithm
            print "Value Iteration"
            # calling valueiteration algorithm
            # here 3 suggests that there are 3 nos of raws and cols i.e 9 states
            valueiteratingpolicy.valueiteratingpolicy(3, p, p1, encoder, ENClast)
        elif val2 == "Q Learning":
            print "QLearning"
            # calling Q-Learning algorithm
            # here 3 suggests that there are 3 nos of raws and cols i.e 9 states
            trial = qLearning.qLearning(3, p, p1, encoder, ENClast)
            print(trial[0])
            print("\n")
            print(trial[1])
            print("\n")
            print(trial[2])
        else:  # qLamda learning
            print "qLamda"
            # calling Q(λ)-Learning algorithm
            # here 3 suggests that there are 3 nos of raws and cols i.e 9 states
            trial = qLamda.qLamda(3, p, p1, encoder, ENClast)
            print(trial[0])
            print("\n")
            print(trial[1])
            print("\n")
            print(trial[2])
    else:  # if switch is at OFF position
        print "stopped"
    val1 = pinSetup.valueRead_ON()  # updating switch position On/OFF
    val2 = pinSetup.valueRead_alg()  # updating switch position for algorithm
