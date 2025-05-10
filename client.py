import asyncio
import logging
from datetime import datetime, timezone
from enum import Enum
from ocpp.routing import on  # Import the 'on' decorator

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running:")
    print("\n $ pip install websockets")
    import sys
    sys.exit(1)

from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result
from ocpp.v201.enums import Action

logging.basicConfig(level=logging.INFO)


class AuthorizationStatus(str, Enum):
    accepted = "Accepted"
    blocked = "Blocked"
    expired = "Expired"
    invalid = "Invalid"
    concurrentTx = "ConcurrentTx"
    rejected = "Rejected"


class ChargePoint(cp):
    @on(Action.boot_notification)
    def on_boot_notification(self, charging_station, reason, **kwargs):
        return call_result.BootNotification(
            current_time=datetime.now(timezone.utc).isoformat(),
            interval=10,
            status="Accepted"
        )

    @on(Action.heartbeat)
    def on_heartbeat(self):
        print("Got a Heartbeat!")
        return call_result.Heartbeat(
            current_time=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        )

    @on(Action.authorize)
    def on_authorize(self, id_token, **kwargs):
        print(f"Received token for authorization: {id_token['id_token']}")
        token = id_token['id_token']
        if token == "VALID123":
            status = AuthorizationStatus.accepted
        else:
            status = AuthorizationStatus.invalid

        return call_result.Authorize(
            id_token_info={
                "status": status
            }
        )


async def on_connect(websocket):
    try:
        requested_protocols = websocket.request.headers["Sec-WebSocket-Protocol"]
    except KeyError:
        logging.error("Client hasn't requested any Subprotocol. Closing Connection")
        return await websocket.close()

    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        logging.warning(
            "Protocols Mismatched | Expected Subprotocols: %s,"
            " but client supports %s | Closing connection",
            websocket.available_subprotocols,
            requested_protocols,
        )
        return await websocket.close()

    charge_point_id = websocket.request.path.strip("/")
    charge_point = ChargePoint(charge_point_id, websocket)
    await charge_point.start()


async def main():
    server = await websockets.serve(
        on_connect, "0.0.0.0", 9000, subprotocols=["ocpp2.0.1"]
    )
    logging.info("Server started. Listening for charge points...")
    await server.wait_closed()


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
