import logging

# disable INFO level logging for transitions library since it will break the communication protocol based on stdout
logging.getLogger("transitions").setLevel(logging.CRITICAL)
