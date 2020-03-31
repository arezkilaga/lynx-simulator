# lynx-simulator

Lynx prefetching mechanism simulator

Usage: In the folder config, run the following script in order to create your custom configuration:

python3 lynx_create_config.py [-h] -f FILENAME -t TRANSITION -m MISS -p PREDICTION -o OUTPUT.json

FILENAME: is a text file containing a sequence of file pages read by a program.

TRANSITION: is the maximum number of transitions allowed for a given page.

MISS: is the maximum number of MISS allowed on a file.

PREDICTION: is the number of pages LYNX should predict and prefetch.

OUTPUT.json: is the configuration file output.

In the main folder, run the following script in order to execute the simulation and obtain the results:

lynx.py [-h] -f FILENAME

FILENAME: is the configuration file created by the previous script.
