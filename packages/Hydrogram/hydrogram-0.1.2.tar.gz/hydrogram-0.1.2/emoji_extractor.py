import re

import httpx

EMOJI_RE = re.compile(r"([0-9A-F ]+)\t(.+)", re.IGNORECASE)

EMOJI_LIST_URL = "https://www.unicode.org/emoji/charts/emoji-list.txt"


def screaming_snake_case(string):
    return (
        "_".join(re.findall(r"[a-z0-9]+", string, re.IGNORECASE))
        .upper()
        .replace("1ST", "FIRST")
        .replace("2ND", "SECOND")
        .replace("3RD", "THIRD")
    )


def main():
    emoji_list = httpx.get(EMOJI_LIST_URL).text
    for emoji_match in EMOJI_RE.finditer(emoji_list):
        emoji_code = emoji_match.group(1)
        emoji_name = emoji_match.group(2)

        emoji_code = "".join([rf"\U{code.zfill(8)}" for code in emoji_code.split(" ")])
        emoji_name = screaming_snake_case(emoji_name)

        print(f'{emoji_name} = "{emoji_code}"')


if __name__ == "__main__":
    main()
