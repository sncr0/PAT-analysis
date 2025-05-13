# receiver.py
import trio
import json
import multiaddr
from libp2p import new_host
from libp2p.crypto.secp256k1 import create_new_key_pair
from libp2p.network.stream.net_stream import INetStream

from p2p.constants import PROTOCOL_ID, FIXED_SECRET, LISTEN_PORT


async def blockchain_handler(stream: INetStream):
    data = await stream.read()
    message = json.loads(data.decode())
    print("✅ Received:", message)

    # Here you'd insert a call to Web3.py, foundry/cast, etc.
    print("🪙 Simulating blockchain log...")

    await stream.close()


class ReceiverNode:
    def __init__(self):
        FIXED_SECRET = bytes.fromhex("d68630d25322e75e1f664d1647db23310bea0297f6c35b99c1d024a766294351")
        self.key_pair = create_new_key_pair(FIXED_SECRET)


    async def start(self):
        self.host = new_host(key_pair=self.key_pair)
        listen_addr = multiaddr.Multiaddr(f"/ip4/0.0.0.0/tcp/{LISTEN_PORT}")
        async with self.host.run(listen_addrs=[listen_addr]):
            self.host.set_stream_handler(PROTOCOL_ID, blockchain_handler)
            print("🟢 Receiver running")
            print(f"Peer ID: {self.host.get_id().to_string()}")
            print("Waiting for incoming data...")
            await trio.sleep_forever()


if __name__ == "__main__":
    trio.run(ReceiverNode().start)
