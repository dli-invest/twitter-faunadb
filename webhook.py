import os
import json
import requests
from operator import itemgetter


def format_tweet_for_discord(stream_data: dict):
    try:
        # data, matching_rules
        data, matching_rules, includes = itemgetter("data", "matching_rules", "includes")(stream_data)
        # figure out matching rules in v2
        embeds = []
        id, author_id, text = itemgetter("id", "author_id", "text")(data)
        if text != None:
            text = text[0:2000]

        title = " ,".join([str(rule.get("tag")) for rule in matching_rules])

        user = None
        try:
            users = itemgetter("users")(includes)
            user = itemgetter("username")(users[0])
        except Exception as e:
            print(e)
        # figure out how to output all matching tags somehow
        embed = {
            "title": title,
            "description": text,
            "author": {
                "name": f"{id} - {author_id}",
            },
            "url": f"https://twitter.com/{user}/status/{id}"
        }
        embeds.append(embed)
        return embeds
    except Exception as e:
        print(e)
        print("NO DATA RETURNED")
        return []


def post_webhook_content(content: str = "", embeds: list = None):
    url = os.getenv("DISCORD_WEBHOOK")
    data = {}
    if content == "":
        data["content"] = ""
    else:
        # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
        data["content"] = f"```{content}```"
    if embeds is not None:
        data["embeds"] = embeds

    result = requests.post(
        url, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))