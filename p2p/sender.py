# sender.py
import trio
import json
import multiaddr
from libp2p import new_host
from libp2p.crypto.secp256k1 import create_new_key_pair
from libp2p.peer.peerinfo import info_from_p2p_addr

from p2p.constants import PROTOCOL_ID, FIXED_SECRET, RECEIVER_MULTIADDR


class SenderNode:
    def __init__(self):
        FIXED_SECRET = bytes.fromhex("d68630d25322e75e1f664d1647db23310bea0297f6c35b99c1d024a766294351")
        self.key_pair = create_new_key_pair(FIXED_SECRET)

    async def send(self, payload: dict):
        self.host = new_host(key_pair=self.key_pair)
        listen_addr = multiaddr.Multiaddr("/ip4/0.0.0.0/tcp/0")  # OS picks an available port
        async with self.host.run(listen_addrs=[listen_addr]):
            info = info_from_p2p_addr(multiaddr.Multiaddr(RECEIVER_MULTIADDR))
            await self.host.connect(info)
            stream = await self.host.new_stream(info.peer_id, [PROTOCOL_ID])

            await stream.write(json.dumps(payload).encode())
            await stream.close()
            print("📤 Data sent!")


if __name__ == "__main__":
    sample_data = {
        "type": "SPECTRO_DATA",
        "hash": "QmABC123...",
        "timestamp": "2025-05-13T16:42:00Z",
    }
    trio.run(SenderNode().send, sample_data)
