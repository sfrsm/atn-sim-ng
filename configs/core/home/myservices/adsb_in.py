#
# CORE
# Copyright (c)2010-2012 the Boeing Company.
# See the LICENSE file included in this distribution.
#
''' Sample user-defined service.
'''
import os

from core.service import CoreService, addservice
from core.misc.ipaddr import IPv4Prefix, IPv6Prefix

class AdsbIn(CoreService):
    ''' This is a sample user-defined service.
    '''
    # a unique name is required, without spaces
    _name = "AdsbIn"
    # you can create your own group here
    _group = "Aviation"
    # list of other services this service depends on
    _depends = ()
    # per-node directories
    _dirs = ()
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    _configs = ('adsb_in.cfg', 'adsb_in.sh')
    # this controls the starting order vs other enabled services
    _startindex = 50
    # list of startup commands, also may be generated during startup
    _startup = ('sh adsb_in.sh',)
    # list of shutdown commands
    _shutdown = ()

    @classmethod
    def generateconfig(cls, node, filename, services):
        ''' Return a string that will be written to filename, or sent to the
            GUI for user customization.
        '''
        if filename == "adsb_in.sh":
            # get lat/lng position
            l_lat, l_lng, l_alt = node.session.location.getgeo(node.position.x, node.position.y, node.position.z)

            cfg = "#!/bin/sh\n"
            cfg += "# auto-generated by AdsbIn (adsb_in.py)\n"
            cfg += "sleep 10\n"
            cfg += "echo \"x/y/z: {} {} {}\"\n".format(node.position.x, node.position.y, node.position.z)
            cfg += "echo \"Lat/Lng/Alt: {}\"\n".format(node.session.location.getgeo(node.position.x, node.position.y, node.position.z))
            cfg += "python -m atn.surveillance.adsb.adsb_in {} {} {} {} 2> adsb_in.log\n".format(int(node.objid), l_lat, l_lng, l_alt)

        elif filename == "adsb_in.cfg":
            cfg = "[glb]\n"
            cfg += "destinations = dump1090 buster\n\n"
            cfg += "[dump1090]\n"
            cfg += "type = dump1090\n"
            cfg += "server = localhost\n"
            cfg += "port = 30001\n"
            cfg += "\n"
            cfg += "[buster]\n"
            cfg += "type = buster\n"
            cfg += "addr = 10.0.1.10\n"
            cfg += "port = 12270\n\n"

        return cfg

    @staticmethod
    def subnetentry(x):
        ''' Generate a subnet declaration block given an IPv4 prefix string
            for inclusion in the config file.
        '''
        if x.find(":") >= 0:
            # this is an IPv6 address
            return ""
        else:
            net = IPv4Prefix(x)
            return 'echo "  network %s"' % (net)

# this line is required to add the above class to the list of available services
addservice(AdsbIn)
