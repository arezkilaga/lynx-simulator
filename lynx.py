#!/usr/bin/python

# IMPORT
#
import subprocess
import argparse
import json
import numpy as np
from collections import defaultdict
from operator import itemgetter

# MAIN
#
if __name__ == '__main__':

    # Read the command line
    parser = argparse.ArgumentParser(description = "Simulate Lynx prefetching mechanism")
    parser.add_argument("-f", "--filename",  required=True, help="json Lynx simulator json configuration file name")

    args = parser.parse_args()

    # Open the configuration json file
    jsonFile = open(args.filename)

    # Parse the configuration json file
    lynx_config = json.load(jsonFile)
    max_nb_transition = lynx_config["max_transition_nb"]
    max_nb_miss       = lynx_config["lots_of_miss_nb"]
    read_sequence     = lynx_config["reads"]
    current_read      = 0
    nb_predictions    = 2
    nb_page_cached    = 0

    nb_pages_in_the_simulation = 1+read_sequence[np.argmax(read_sequence)]
    state_machine = np.zeros((nb_pages_in_the_simulation, max_nb_transition, 2))
    prediction    = np.zeros(nb_predictions)
    cache         = {0}

    cache_hit           = 0
    cache_miss          = 0
    total_hit           = 0
    total_miss          = 0
    current_miss        = 0
    state_machine_reset = 0

    for page in read_sequence:

        # Is the prediction method accurate ? 
        if page in prediction:
            total_hit +=1
        else: 
            total_miss   +=1
            current_miss +=1

        #Is the page already cached ?
        if page in cache:
            cache_hit +=1
        else:
            cache_miss +=1
            cache.add(page)

        #Prediction
        transitions = state_machine[page]
        sorted_transition = sorted(transitions, key=itemgetter(1), reverse=True)
        for i in range(nb_predictions):
            if (sorted_transition[i][1] > 0):
                prediction[i] = sorted_transition[i][0]
                cache.add(prediction[i])

        #Learning
        page_idx = (page % (max_nb_transition))

        if (state_machine[current_read][page_idx][0] == page):
            state_machine[current_read][page_idx][1] +=1
        elif (state_machine[current_read][page_idx][0] == 0):
            state_machine[current_read][page_idx][0] = page
            state_machine[current_read][page_idx][1] = 1
        else:
            state_machine[current_read][page_idx][1] = -1
        
        current_read = page

        if (current_miss > max_nb_miss):
            current_miss  = 0
            curent_read   = 0
            state_machine = np.zeros((nb_pages_in_the_simulation, max_nb_transition, 2))
            prediction    = np.zeros(nb_predictions)
            state_machine_reset += 1

    print("Total reads %s"%len(read_sequence))
    print("Total cache miss %s"%cache_miss)
    print("Total cache hit %s"%cache_hit)
    print("Total prediction miss %s"%total_miss)
    print("Total prediction hit  %s"%total_hit)
    print("Prediction state machine has been reset %s times"%state_machine_reset)

    # Close the configuration json file
    jsonFile.close()
