from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from pynostr.key import PrivateKey
from pynostr.encrypted_dm import EncryptedDirectMessage
import time
import uuid
from ollamaApi import OllamaApi
import os

env_private_key = os.environ.get("PRIVATE_KEY")
if not env_private_key:
    print('The environment variable "PRIVATE_KEY" is not set.')
    exit(1)

private_key = PrivateKey(bytes.fromhex(env_private_key))
public_key = private_key.public_key.hex()

relay_manager = RelayManager(timeout=2)
relay_manager.add_relay("wss://relay.damus.io")
filters = FiltersList([Filters(pubkey_refs=[public_key], kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE], limit=1)])
subscription_id = uuid.uuid1().hex
relay_manager.add_subscription_on_all_relays(subscription_id, filters)
relay_manager.run_sync()
while relay_manager.message_pool.has_notices():
    notice_msg = relay_manager.message_pool.get_notice()
    print(notice_msg.content)
while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    # print(event_msg.event.content)
    msg_decrypted = EncryptedDirectMessage()
    msg_decrypted.decrypt(private_key_hex=private_key.hex(), encrypted_message=event_msg.event.content, public_key_hex=event_msg.event.pubkey)
    message = msg_decrypted.cleartext_content
    print("Message: " + message)
    print("=======")
    ollama = OllamaApi("http://host.docker.internal:11434/api/generate")
    response = ollama.call_api(message)
    print("Response: " + response['response'])
    # TODO: Send message back as DM to user

relay_manager.close_all_relay_connections()