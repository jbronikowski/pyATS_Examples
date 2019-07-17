#!/usr/bin/env python
###################################################################
# basic_example.py : A very simple test script example which include:
#     common_setup
#     Tescases
#     common_cleanup
# The purpose of this sample test script is to show the "hello world"
# of aetest.
###################################################################

# To get a logger for the script
from ats.log.utils import banner
from genie.conf import Genie
import logging
from pyats import aetest

from genie.utils.config import Config

# Get your logger for your script
log = logging.getLogger(__name__)

###################################################################
###                  COMMON SETUP SECTION                       ###
###################################################################

# This is how to create a CommonSetup
# You can have one of no CommonSetup
# CommonSetup can be named whatever you want

class device_setup(aetest.CommonSetup):
    """ Common Setup section """

    # Connect to each device in the testbed'
    @aetest.subsection
    def connect(self, testbed, steps):
        genie_testbed = Genie.init(testbed)
        device_list = []
        device_name = []

        for device in genie_testbed.devices.values():
            with steps.start("Connecting to device '{d}'".format(d=device.name)):
                log.info(banner(
                    "Connecting to device '{d}'".format(d=device.name)))
                try:
                    device.connect()
                except Exception as e:
                    self.failed("Failed to establish connection to '{}'".format(
                        device.name))

                device_list.append(device)
                device_name.append(device.name)
        log.info((device_list))
        aetest.loop.mark(device_commands, devices=device_list, uids=device_name)


###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

# This is how to create a testcase
# You can have 0 to as many testcase as wanted

# Testcase name : tc_one
class device_commands(aetest.Testcase):
    """ This is user Testcases section """

    @ aetest.test
    def parse_running_config(self, devices):
        """ Parsing running config """

        output = devices.execute('show running-config')
        config = Config(output)
        config.tree()

        #  Storing running configuration to use later
        self.config_output = config.config

    @aetest.test
    def disable_source_routing(self, devices):
        """ Disabling ip source-route on device """

        if 'no ip source-route' in self.config_output.keys():
            self.skipped('Device is already configured properly')
        #  Executing 'no ip source-route' on device
        devices.configure("no ip source-route")


if __name__ == '__main__': # pragma: no cover
    aetest.main()
