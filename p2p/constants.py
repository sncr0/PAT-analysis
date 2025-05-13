# constants.py
from libp2p.custom_types import TProtocol

PROTOCOL_ID = TProtocol("/pat/qc-log/1.0.0")

FIXED_SECRET = b"my-hardcoded-peer-secret-must-be-32bytes!"  # 32 bytes = 256 bits

LISTEN_PORT = 9000
RECEIVER_MULTIADDR = f"/ip4/127.0.0.1/tcp/{LISTEN_PORT}/p2p/16Uiu2HAmAA4ZRKeKaw4MbrwoaMCDBYV3vq8ZQkECjGYUkyScReQJ"  # fill after running receiver
