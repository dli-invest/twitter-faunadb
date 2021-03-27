import requests
import os
import json
from webhook import post_webhook_content, format_tweet_for_discord
# from fauna_driver import FaunaWrapper

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token):
    # You can adjust the rules if needed
    # dollar signs do not work at the moment
    sample_rules = [
        {"value": "@ThreeDCap", "tag": "IDK - 3D Capital"},
        {"value": "@sheldonstash OR @PEAK_fintech", "tag": "investment firms"},
        {
            "value": "GET RICH FAST TESTING TWITTER STREAM OR @pikainvestor",
            "tag": "Test Tag",
        },
        {
            "value": "pikainvestor",
            "tag": "Test Tag",
        }
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(headers, set, bearer_token):
    # db_client = FaunaWrapper()
    tweet_fields = "tweet.fields=lang,author_id,in_reply_to_user_id"
    expansions = "expansions=author_id"
    url = "https://api.twitter.com/2/tweets/search/stream?{}&{}".format(
        tweet_fields, expansions
    )
    with requests.get(
        url,
        headers=headers,
        stream=True,
        timeout=480,
    ) as response:
        print(response.status_code)
        try:
            if response.status_code != 200:
                raise Exception(
                    "Cannot get stream (HTTP {}): {}".format(
                        response.status_code, response.text
                    )
                )
            print(response)
            for response_line in response.iter_lines():
                if response_line:
                    json_response = json.loads(response_line)
                    data = json.dumps(json_response, indent=4, sort_keys=True)
                    print(data)

                    # Send both versions until I finish updating the script
                    # and cashtags actually work $
                    post_webhook_content(data)
                    embeds = format_tweet_for_discord(json_response)
                    post_webhook_content(embeds=embeds)
                    # Add data faunadb
                    # db_client.create_document_in_collection(json_response)

        except Exception as e:
            print(e)
            post_webhook_content(str(e))


def main():
    bearer_token = os.environ.get("BEARER_TOKEN")
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token)
    get_stream(headers, set, bearer_token)


if __name__ == "__main__":
    main()