'''
This file contains the code for the AI control algorithms.

Created on Oct 11, 2016
View the full repository here https://github.com/car-chase/amoebots
'''

from multiprocessing import Process, Queue, Array

def ai_level_main(TO_MAIN, AI_INPUT_QUEUE, TO_MOVEMENT):
