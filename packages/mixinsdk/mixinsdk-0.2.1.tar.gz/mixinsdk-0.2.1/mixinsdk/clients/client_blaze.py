import asyncio
import gzip
import json
import logging
import signal
import sys
import time
import uuid
from collections import deque
from concurrent.futures import ThreadPoolExecutor

import websockets
import websockets.client
from cryptography.hazmat.primitives.asymmetric import ed25519

from mixinsdk.clients._message import encrypt_message_data
from mixinsdk.types.user import UserProfile

from ..constants import API_BASE_URLS
from ..utils import get_conversation_id_of_two_users
from ._message import parse_message_data
from ._sign import sign_authentication_token
from .config import AppConfig


class BlazeClient:
    """WebSocket client with keystore"""

    def __init__(
        self,
        config: AppConfig,
        profile: UserProfile = None,
        on_message: callable = None,
        on_error: callable = None,
        api_base: str = API_BASE_URLS.BLAZE_DEFAULT,
        auto_start_list_pending_message=True,
    ):
        """
        - on_message, function, 2 arguments: blaze_client, message:dict
        - on_error, function, 2 arguments: blaze_client, error:Exception
        """
        self.config = config
        self.profile = profile

        self.on_message = on_message
        self.on_error = on_error
        self.logger = logging.getLogger("blaze-client")
        self.api_base = api_base
        self.auto_start_list_pending_message = auto_start_list_pending_message

        self.ws = None
        self._stoping = False
        self._sending_deque = deque()
        self._msg_processors: ThreadPoolExecutor = None
        self._msg_sender: ThreadPoolExecutor = None

    def _get_auth_token(self, method: str, uri: str, bodystring: str):
        return sign_authentication_token(
            self.config.client_id,
            self.config.session_id,
            self.config.private_key,
            self.config.key_algorithm,
            method,
            uri,
            bodystring,
        )

    def get_conversation_id_with_user(self, user_id: str):
        return get_conversation_id_of_two_users(self.config.client_id, user_id)

    def echo(self, received_msg_id):
        """
        when receive a message, must reply to server
        ACKNOWLEDGE_MESSAGE_RECEIPT ack server received message
        """
        params = {"message_id": received_msg_id, "status": "READ"}
        msg = {
            "id": str(uuid.uuid4()),
            "action": "ACKNOWLEDGE_MESSAGE_RECEIPT",
            "params": params,
        }
        return self._send(msg)

    def send_message(self, message: dict):
        """
        - message, use types.message.pack_message() to make it
        """

        # TODO : depends on switch of encryption
        # message["data"]=

        msg = {
            "id": str(uuid.uuid4()),
            "action": "CREATE_MESSAGE",
            "params": message,
        }
        return self._send(msg)

    def run_forever(self, max_workers):
        """
        run websocket server forever
        """

        # ----- For handle KeyboardInterrupt
        def kbdint_handler(sig, frame):
            self.logger.debug(" ⌨ Keyboard Interrupt =====")
            self.close(keyboard_interrupt=True)
            # TODO a better way to exit gracefully
            #   websockets wait next message will block the main thread,
            #   so use sys.exit() to force exit
            sys.exit(0)

        signal.signal(signal.SIGINT, kbdint_handler)

        # Multiple threads to handle messages
        self._msg_processors = ThreadPoolExecutor(max_workers=max_workers)
        # One thread to send message. Websockets not support concurrent
        self._msg_sender = ThreadPoolExecutor(max_workers=1)

        def sender():
            self.logger.debug("sender started")
            while True:
                if self._stoping:
                    break
                if not self._sending_deque:
                    time.sleep(0.1)
                    continue
                if not self.ws:
                    time.sleep(0.1)
                    continue
                msg_obj = self._sending_deque.popleft()
                raw_msg = gzip.compress(json.dumps(msg_obj).encode())
                try:
                    asyncio.run(self.ws.send(raw_msg))
                except Exception as e:
                    self.logger.error("Exception occurred", exc_info=True)
                    self._callback(self.on_error, e)
            self.logger.debug("sender ended")

        self._msg_sender.submit(sender)

        msg = f"Blaze client ID: {self.config.client_id}"
        self.logger.info(msg)

        # Run websocket forever
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._running_loop())
        self.logger.debug("loop end")

        # close websocket connection
        try:
            self.loop.run_until_complete(self.ws.wait_closed())
        except Exception:
            pass

        self.logger.debug("Shutting down the threads ...")
        self._msg_processors.shutdown(wait=True)
        self._msg_sender.shutdown(wait=True)

        self.logger.info("Blaze client stopped")

    async def _running_loop(self):
        def _handle_message(raw_msg):
            message = json.loads(gzip.decompress(raw_msg).decode())
            self._callback(self.on_message, message)

        def _handle_message_done(future: asyncio.Future):
            error = future.exception()
            if error:
                self._callback(self.on_error, error)

        while True:  # -- Run websocket server forever
            auth_token = self._get_auth_token("GET", "/", "")
            async for websocket in websockets.connect(
                self.api_base,
                subprotocols=["Mixin-Blaze-1"],
                extra_headers={"Authorization": f"Bearer {auth_token}"},
            ):
                self.logger.info("Websocket connected")
                self.ws: websockets.client.WebSocketClientProtocol = websocket
                try:
                    if self.auto_start_list_pending_message:
                        self.start_to_list_pending_message()

                    async for raw_msg in self.ws:  # if no message, will be blocking
                        if self._stoping:
                            break
                        f = self._msg_processors.submit(_handle_message, raw_msg)
                        f.add_done_callback(_handle_message_done)

                    if self._stoping:
                        break

                except websockets.ConnectionClosed:
                    self.logger.warn("websockets.ConnectionClosed")
                    time.sleep(2)
                    break  # to recreate websocket connection of new token, else invalid token
                    # if self._stoping:
                    #     break
                except Exception as e:
                    self.logger.error("Exception occurred", exc_info=True)
                    self._callback(self.on_error, e)
                    time.sleep(2)
                    break  # to recreate websocket connection of new token, else invalid token
                    # if self._stoping:
                    #     break
            # exited the websocket context, will closed the connection automatically
            self.logger.debug("exited the websocket context")

            if self._stoping:
                break  # exit the while loop

    def parse_message_data(self, data: str, category: str):
        return parse_message_data(
            data, category, self.config.session_id, self.config.private_key
        )

    def encrypt_message_data(self, data_b64_str: str):
        pass
        # # data = base64.b64encode(b"hello world").decode("utf-8")
        # private = ed25519.Ed25519PrivateKey().from_private_bytes(
        #     self.config..private_key
        # )
        # public = private.public_key()
        # user_session = UserSession(
        #     self.config..client_id, self.config..session_id, public
        # )
        # data_encrypted = encrypt_message_data(
        #     data, [user_session], self.config..private_key
        # )
        # data_b64_str = base64.b64encode(data_encrypted).decode("utf-8")

    def start_to_list_pending_message(self):
        if not self.ws:
            print("✗ Failed to listen, websocket is not connected")
            return
        msg = {"id": str(uuid.uuid4()), "action": "LIST_PENDING_MESSAGES"}
        self._send(msg)

    def close(self, keyboard_interrupt=False):
        self.logger.debug("stoping")
        self._stoping = True
        if not keyboard_interrupt:
            try:
                asyncio.run(self.ws.close_connection())
            except Exception:
                pass

    def _send(self, msg_obj) -> None:
        """Add message to sending deque"""
        if self._stoping:
            return
        self._sending_deque.append(msg_obj)

    def _callback(self, callback, *args):
        if callback:
            try:
                callback(self, *args)
            except Exception as e:
                self.logger.error(f"error from callback {callback}: {e}")
                if self.on_error:
                    self.on_error(self, e)
