# To run the job:
# pyats run job $VIRTUAL_ENV/examples/basic/job/basic_example_job.py
# Description: This example shows the basic functionality of pyats
#              with few passing tests

import os
from pyats.easypy import run
import logging

# All run() must be inside a main function
def main(runtime):
    # Find the location of the script in relation to the job file
    test_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    testscript = os.path.join(test_path, 'source_route_script.py')
    # Execute the testscript
    run(testscript=testscript)
