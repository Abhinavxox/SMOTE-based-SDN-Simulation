# Import necessary modules
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str, str_to_dpid
from pox.lib.util import str_to_bool
import time

# Initialize the core logger
log = core.getLogger()

# We don't want to flood immediately when a switch connects.
# Can be overridden on the command line.
_flood_delay = 0

class LearningSwitch(object):
    """
    The learning switch "brain" associated with a single OpenFlow switch.
    """

    def __init__(self, connection, transparent):
        # Switch we'll be adding L2 learning switch capabilities to
        self.connection = connection
        self.transparent = transparent

        # Our table
        self.macToPort = {}

        # We want to hear PacketIn messages, so we listen
        # to the connection
        connection.addListeners(self)

        # We just use this to know when to log a helpful message
        self.hold_down_expired = _flood_delay == 0

        # log.debug("Initializing LearningSwitch, transparent=%s",
        #          str(self.transparent))

    def _handle_PacketIn(self, event):
        """
        Handle packet in messages from the switch to implement the algorithm.
        """

        packet = event.parsed

        self.macToPort[packet.src] = event.port  # 1

    def print_mac_to_port_mapping(self):
        print("MAC to Port Mapping:")
        for mac, port in self.macToPort.items():
            print(f"  MAC: {mac}, Port: {port}")


class l2_learning (object):
    """
    Waits for OpenFlow switches to connect and makes them learning switches.
    """

    def __init__ (self, transparent, ignore = None):
        core.openflow.addListeners(self)
        self.transparent = transparent
        self.ignore = set(ignore) if ignore else ()
        self.learning_switches = []  # Keep track of LearningSwitch instances

    def _handle_ConnectionUp (self, event):
        if event.dpid in self.ignore:
            log.debug("Ignoring connection %s" % (event.connection,))
            return
        log.debug("Connection %s" % (event.connection,))
        learning_switch = LearningSwitch(event.connection, self.transparent)
        self.learning_switches.append(learning_switch)

        # Call the print function for each LearningSwitch instance
        for ls in self.learning_switches:
            ls.print_mac_to_port_mapping()

def launch (transparent=False, hold_down=_flood_delay, ignore = None):
    """
    Starts an L2 learning switch.
    """
    try:
        global _flood_delay
        _flood_delay = int(str(hold_down), 10)
        assert _flood_delay >= 0
    except:
        raise RuntimeError("Expected hold-down to be a number")

    if ignore:
        ignore = ignore.replace(',', ' ').split()
        ignore = set(str_to_dpid(dpid) for dpid in ignore)

    core.registerNew(l2_learning, str_to_bool(transparent), ignore)