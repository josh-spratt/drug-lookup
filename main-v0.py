import requests
import json
import matplotlib.pyplot as plt
import argparse


def get_list_of_potential_drug_matches(key, drug):
    # Sends a drug param to rest rx api and returns a json response body
    url = 'https://api.seer.cancer.gov/rest/rx/latest'
    headers = {'X-SEERAPI-Key': key}
    params = {'count': '100', 'q': drug}
    req = requests.get(url, headers=headers, params=params)
    json_response = req.json()
    return json_response


def generate_score_histogram_from_json_request(response_data):
    # Generates a histogram that is the distribution of result match scores
    score_list = [int(result_dict['score'])
                  for result_dict in response_data['results']]
    name_list = [result_dict['name']
                 for result_dict in response_data['results']]
    print(json.dumps(response_data['results'], indent=4))
    plt.hist(score_list)
    plt.show()


def find_max_match_scores(dict_of_matches):
    max_score = 0

    for match in dict_of_matches['results']:
        if match["score"] > max_score:
            max_score = match["score"]

    max_score_list = []
    for match in dict_of_matches['results']:
        if match["score"] == max_score:
            max_score_list.append(match)

    return max_score_list




parser = argparse.ArgumentParser()
parser.add_argument("--key")
parser.add_argument("--drug")
args = parser.parse_args()

if args.key and args.drug:
    matches = get_list_of_potential_drug_matches(args.key, args.drug)
elif args.key:
    print("Please enter '--key API KEY' and '--drug DRUG NAME' in the command line interface when executing this script")
elif args.drug:
    print("Please enter '--key API KEY' and '--drug DRUG NAME' in the command line interface when executing this script")
else:
    print("Please enter '--key API KEY' and '--drug DRUG NAME' in the command line interface when executing this script")

best_match = find_max_match_scores(matches)

