import io

from meval import meval

from hydrogram import Client, filters

app = Client(
    "test_acc",
    api_id=178262,
    api_hash="6b72d4f3edaa072870c6771473cc3acc",
    in_memory=True,
    session_string="AQACuFYAYAsxDkNdLvw8gHZk5EFJOQRI1XK5rEJvbsuKNaXIpH5AD0kFhuyNDedWuoZZ2Oq4VZfaHzxZksxYGHSt1q5S7JSUgyrJf-5EJjSQGI6mxcmU9yUsfOahxoDqCKb21nmz6iNCARdZDNzC0hzguf-nDtx5smNDwQRgGJuxYpLkBFkziG2nX0xOV8MUUuqPato-Mzalie6aAxt_WE_8iYC6_lxwPxUwcCS1okZX7NY4GN9-Hl_a3dsOEWfIdUcF_suYFeath4ER2t-neghDcMC3neXAYxNs5Lh1_wr5LXBFUM7oB-ecuniUC0jYYpIwja4V-TiUKzxW221iwmWPNUjHmQAAAAGRlPdxAQ",
)


@app.on_message(filters.text)
async def echo(client, message):
    ret = str(await meval(message.text, globs=globals(), c=client, m=message))

    if len(ret) > 4000:
        strio = io.BytesIO()
        strio.name = "output.txt"
        strio.write(ret.encode())

        await message.reply_document(strio)
    else:
        await message.reply_text(
            f"```json\n{await meval(message.text, globs=globals(), c=client, m=message)}```",
        )


app.run()
