from plugins import *
from sqlalchemy import create_engine
from env import logger
from HPotterDB import Base
import types
import socket
import signal

servers = []

def signal_handler(signal, frame):
    logger.info("shutting down")
    for server in servers:
        server.shutdown()

# make sure you add all non-plugins imports here
imported = ['__builtins__', 'types', 'socket', 'sqlalchemy', 'logging', \
    'signal', 'env', 'HPotterDP']

if "__main__" == __name__:

    # note sqlite:///:memory: can't be used, even for testing, as it
    # doesn't work with threads.
    engine = create_engine('sqlite:///main.db', echo=True)
    Base.metadata.create_all(engine)

    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            if name in imported:
                continue
            for address in val.get_addresses():
                mysocket = socket.socket(address[0])
                mysocket.bind((address[1], address[2]))

                servers.append(val.start_server(mysocket, engine))

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()