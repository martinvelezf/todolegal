from json import dumps

from httplib2 import Http


def main():
    """Hangouts Chat incoming webhook quickstart."""
    url = 'https://webhook.site/4cb7980d-edf2-4ebc-b19f-92e34aeb7719'
    bot_message = {
        'text' : 'Hello from a Python script!',
        'value':'Nuevo valor'
        }

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

    print(response)

if __name__ == '__main__':
    main()