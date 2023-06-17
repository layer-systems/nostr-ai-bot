import requests
import time
import ssl
import os
import json
import uuid
from pynostr.event import Event, EventKind
from pynostr.relay_manager import RelayManager
from pynostr.message_type import ClientMessageType
from pynostr.key import PrivateKey
from pynostr.filters import FiltersList, Filters
from pynostr.encrypted_dm import EncryptedDirectMessage
from gpt4all import GPT4All


relay_manager = RelayManager(timeout=2)

messages_done = []

try:
    env_private_key = os.environ.get("PRIVATE_KEY")
    if not env_private_key:
        print('The environment variable "PRIVATE_KEY" is not set.')
        exit(1)

    private_key = PrivateKey(bytes.fromhex(env_private_key))
    # Read env variable and add relays
    env_relays = os.getenv('RELAYS') # None
    if env_relays is None:
        env_relays = "wss://relay.layer.systems"
    for relay in env_relays.split(","):
        print("Adding relay: " + relay)
        relay_manager.add_relay(relay)

    print("Pubkey: " + private_key.public_key.bech32())
    print("Pubkey (hex): " + private_key.public_key.hex())

    while(True):
        filters = FiltersList([Filters(pubkey_refs=[private_key.public_key.hex()], kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE])])
        subscription_id = uuid.uuid1().hex
        relay_manager.add_subscription_on_all_relays(subscription_id, filters)
        relay_manager.run_sync()
        while relay_manager.message_pool.has_notices():
            notice_msg = relay_manager.message_pool.get_notice()
            print("Notice: " + notice_msg.content)
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()
            msg_decrypted = EncryptedDirectMessage()
            msg_decrypted.decrypt(private_key_hex=private_key.hex(), encrypted_message=event_msg.event.content, public_key_hex=event_msg.event.pubkey)
            # print (event_msg.event.pubkey + " send " + msg_decrypted.cleartext_content)
            currentTime = time.time()
            if(currentTime - 60 < event_msg.event.created_at):
                if(event_msg.event.id in messages_done):
                    continue
                gptj = GPT4All("ggml-gpt4all-j-v1.3-groovy")
                response = gptj.generate(msg_decrypted.cleartext_content, False)
                print(response)
                continue
        time.sleep(10)
        relay_manager.close_all_relay_connections()


except Exception as e:
    print(e)
    relay_manager.close_all_relay_connections()
    exit(1)