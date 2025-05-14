import os
import json
import math
import numpy as np
import trio
from datetime import datetime, timezone

from core.data_readers.infrared_reader import InfraredReader
from core.data_formats.infrared_measurement import InfraredMeasurement
from edge.utils import build_spectrum

from edge.config import SIMULATION, SIMULATION_SINE
from edge.mqtt_uplink import publish_measurement
from edge.p2p_uplink import publish_measurement_p2p





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




def hash_object_keccak256(obj) -> str:
    serialized = json.dumps(obj, sort_keys=True, separators=(',', ':'))
    return keccak(serialized.encode('utf-8')).hex()


async def publish_measurement_p2p(payload: dict):
    FIXED_SECRET = bytes.fromhex("d68630d25322e75e1f664d1647db23310bea0297f6c35b99c1d024a766294351")
    key_pair = create_new_key_pair(FIXED_SECRET)
    host = new_host(key_pair=key_pair)
    listen_addr = multiaddr.Multiaddr("/ip4/0.0.0.0/tcp/0")  # ephemeral port
    print(payload["spectrum"].data["x"])
    spectrum = list(payload["spectrum"].data["x"])
    hashed_spectrum = hash_object_keccak256(spectrum)
    print(hashed_spectrum)

    async with host.run(listen_addrs=[listen_addr]):
        info = info_from_p2p_addr(multiaddr.Multiaddr(RECEIVER_MULTIADDR))
        await host.connect(info)
        print('c')
        # print(payload)
        # print(payload["spectrum"]["X"])
        stream = await host.new_stream(info.peer_id, [PROTOCOL_ID])
        # await stream.write(json.dumps(payload).encode())
        hashed_payload = {"hashed_spectrum": hashed_spectrum,
                          "timestamp": payload["timestamp"]}
        # print(json.dumps(hashed_payload).encode())
        # print(hashed_payload)
        # print('b')
        await stream.write(json.dumps(hashed_payload).encode())
        # await stream.write_eof()  # <-- this is essential to signal EOF to the receiver
        await trio.sleep(0.1)     # small delay to allow receiver to process
        await stream.close()
        print("📤 Sent measurement via P2P")


# --- Simulation mode using real data file ---
async def run_simulation_mode():
    reader = InfraredReader()

    while True:
        try:
            measurement = reader.read_file('data/acetonitrile-acetone/67-64-1-IR.jdx')
            # publish_measurement(measurement)

            # Try P2P if enabled
            await publish_measurement_p2p(measurement.to_dict())

            await trio.sleep(3)
        except Exception as e:
            print("⚠️ Error in simulation loop:", e)


# --- Simulation mode using sine wave synthetic spectrum ---
async def run_simulation_mode_sine():
    print("🔁 Running SIMULATION_SINE mode")
    i = 0.0
    while True:
        try:
            concentration = 0.5 + 0.45 * math.sin(i)
            print(f"🧪 Sine concentration: {concentration:.2f}")
            spectrum = build_spectrum(concentration=concentration)
            timestamp = datetime.now(timezone.utc).isoformat()
            # publish_measurement(spectrum)
            data = {
                "spectrum": spectrum,
                "timestamp": timestamp,
            }
            await publish_measurement_p2p(data)

            i += 0.1
            await trio.sleep(3)
        except Exception as e:
            print("⚠️ Error in sine simulation loop:", e)


# --- Entry point ---
async def main():
    if SIMULATION:
        await run_simulation_mode_sine()
    elif SIMULATION_SINE:
        await run_simulation_mode_sine()
    else:
        print("No simulation mode enabled.")


if __name__ == "__main__":
    trio.run(main)
