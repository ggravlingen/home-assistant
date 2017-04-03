"""
192.168.0.129 -sU -p 5684
https://bitsex.net/software/2017/coap-endpoints-on-ikea-tradfri/
"""


import logging
import asyncio

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    """
    Example class which performs single PUT request to localhost
    port 5683 (official IANA assigned CoAP port), URI "/other/block".
    Request is sent 2 seconds after initialization.

    Payload is bigger than 1kB, and thus is sent as several blocks.
    """

    context = await Context.create_client_context()

    await asyncio.sleep(2)

    payload = b"The quick brown fox jumps over the lazy dog.\n" * 30
    request = Message(code=PUT, payload=payload)
    request.opt.uri_host = '127.0.0.1'
    request.opt.uri_path = ("other", "block")

    response = await context.request(request).response

    print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
