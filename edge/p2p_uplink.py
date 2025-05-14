import os
import logging
import asyncio
import json
import trio
import multiaddr
from eth_hash.auto import keccak


from libp2p.peer.peerinfo import info_from_p2p_addr
from libp2p import new_host
from libp2p.crypto.secp256k1 import create_new_key_pair
from libp2p.peer.peerinfo import info_from_p2p_addr
from p2p.constants import PROTOCOL_ID, FIXED_SECRET, RECEIVER_MULTIADDR

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def hash_object_keccak256(obj) -> str:
    serialized = json.dumps(obj, sort_keys=True, separators=(',', ':'))
    return keccak(serialized.encode('utf-8')).hex()


async def publish_measurement_p2p(payload: dict):
    FIXED_SECRET = bytes.fromhex("d68630d25322e75e1f664d1647db23310bea0297f6c35b99c1d024a766294351")
    key_pair = create_new_key_pair(FIXED_SECRET)
    host = new_host(key_pair=key_pair)
    listen_addr = multiaddr.Multiaddr("/ip4/0.0.0.0/tcp/0")  # ephemeral port

    async with host.run(listen_addrs=[listen_addr]):
        info = info_from_p2p_addr(multiaddr.Multiaddr(RECEIVER_MULTIADDR))
        await host.connect(info)
        print('c')
        stream = await host.new_stream(info.peer_id, [PROTOCOL_ID])
        # await stream.write(json.dumps(payload).encode())
        hashed_payload = {"hashed_spectrum": hash_object_keccak256(payload),
                   "timestamp": payload["timestamp"]}
        print(json.dumps(hashed_payload).encode())
        print(hashed_payload)
        print('b')
        await stream.write(json.dumps(hashed_payload).encode())
        # await stream.write_eof()  # <-- this is essential to signal EOF to the receiver
        await trio.sleep(0.1)     # small delay to allow receiver to process
        await stream.close()
        print("📤 Sent measurement via P2P")

