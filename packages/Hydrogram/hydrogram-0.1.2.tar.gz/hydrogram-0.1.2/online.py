# create a simple Python Telegram userbot using Pyrogram, which should make the account stay online forever

import asyncio
import os

from pyrogram import Client, idle


@client.on_message()
async def handler(client, message):
    await message.reply_text("Hello, World!")


async def main():
    client = Client(
        "my_account",
        api_id=123456,
        api_hash="0123456789abcdef0123456789abcdef",
        workdir=os.getcwd(),
    )

    async with client:
        await idle()


if __name__ == "__main__":
    asyncio.run(main())
