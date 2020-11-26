import requests
import json
import matplotlib.pyplot as plt
import argparse


def generate_score_histogram_from_json_request(response_data):
    # Generates a histogram that is the distribution of result match scores
    score_list = [int(result_dict['score'])
                  for result_dict in response_data['results']]
    name_list = [result_dict['name']
                 for result_dict in response_data['results']]
    print(json.dumps(response_data['results'], indent=4))
    plt.hist(score_list)
    plt.show()


# Global variables
url = 'https://api.seer.cancer.gov/rest/rx/latest'
api_key = input('enter api key...\n')
drug = input('enter drug name\n')
headers = {'X-SEERAPI-Key': api_key}
params = {'count': '100', 'q': drug}
req = requests.get(url, headers=headers, params=params)
json_response = req.json()

generate_score_histogram_from_json_request(json_response)
