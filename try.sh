#!/bin/bash
# Bash Menu Script Example
pull_up_down=GPIO.PUD_DOWN
echo  "21" > /sys/class/gpio/export
echo "in" > /sys/class/gpio/gpio21/direction
echo "19" > /sys/class/gpio/export
echo "in" > /sys/class/gpio/gpio19/direction
cat /sys/class/gpio/gpio21/value
cat /sys/class/gpio/gpio19/value
val=$( cat /sys/class/gpio/gpio21/value)
val1=$(cat /sys/class/gpio/gpio19/value)
#echo val
#PS3='Please enter your choice: '
#options=("Qlearning 1" "ValueIteration 2" "Quit")
#select opt in "${options[@]}"
#do
#    case $opt in
#        "Qlearning 1")
#            python Q-learning_V3.1.py
#            ;;
#        "ValueIteration 2")
#            python valueiteratingpolicy.py
#            ;;
#
#        "Quit")
#            break
#            ;;
#        *) echo "invalid option $REPLY";;
#    esac
#done
a=1
echo "value of\"a\"is $a"
echo "val is $val"

if [ $val == $a ]
then
  echo "Qlearning"
  python /home/pi/Crawler-robot/Q-learning_V3.1.py
else
  echo "value iteration"
  python /home/pi/Crawler-robot/valueiteratingpolicy.py
fi
if [ $val1 == $a ]
then
  echo "shutdown" 
  shutdown now
fi