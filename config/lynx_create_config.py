#!/usr/bin/python

# IMPORT
#
import argparse
import json
import numpy as np
from operator import itemgetter

# MAIN
#
if __name__ == '__main__':

    # Read the command line
    parser = argparse.ArgumentParser(description = "Create the Json configuration file for Lynx Simulator")
    parser.add_argument("-f", "--filename",  required=True, help="File containing a sequence of file pages Pi read by a program, separated by a comma ',' ")
    parser.add_argument("-t", "--transition",  required=True, type=int, help="The transition maximum number per state in Lynx prediction automate")
    parser.add_argument("-m", "--miss",  required=True, type=int, help="The maximum number of tolerated miss read")
    parser.add_argument("-p", "--prediction",  required=True, type=int, help="The number of read operations to predict using the Lynx prediction mechanism")
    parser.add_argument("-o", "--output",  required=True,  help="The output file")


    args = parser.parse_args()

    # Open the configuration json file
    inputFile      = open(args.filename, "r")
    read_sequence  = inputFile.read().replace('\n', '').split(',')
    map_object     = map(int, read_sequence)
    read_sequence  = list(map_object)

    json_configuration = {}

    json_configuration["lots_of_miss_nb"]     = int(args.miss)
    json_configuration["max_transition_nb"]   = int(args.transition)
    json_configuration["page_predictions_nb"] = int(args.prediction)
    json_configuration["reads"]               = read_sequence
    output_filename = args.output

    json_configuration_data = json.dumps(json_configuration)

    inputFile.close()
    output_file = open(output_filename, "w")
    output_file.write(json_configuration_data)
    output_file.close()
