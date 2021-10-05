import requests
import json
import sys

BEARER_TOKEN = 'XXX'
output_path = 'output.txt'
username_count = 300

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers, stream=True)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    else:
        output_file = open(output_path, 'a')
        count = 0
        for response_line in response.iter_lines():
          if count >= username_count :
            output_file.close()
            sys.exit("Done")
          if response_line:
              json_response = json.loads(response_line)
              if json_response['data']['lang'] == 'en' and not json_response['data']['text'].startswith(('RT', '@')):
                  output_file.write(json_response['includes']['users'][0]['username']+"\n")
                  print(json_response['includes']['users'][0]['username'])
                  count += 1
        output_file.close()

def main():
  headers = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}
  url = "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=lang&expansions=author_id"
  timeout = 0

  while True:
    connect_to_endpoint(url, headers)
    timeout += 1

if __name__ == "__main__":
  main()
