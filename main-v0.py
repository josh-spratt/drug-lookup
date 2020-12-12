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
    if json_response['total'] == 0:
        print('I did not find that drug. Please check spelling and try again.')
        quit()
    if json_response['total'] >= 1:
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


def user_verifies_max_score_correctness(list_of_max_scores):
    if len(list_of_max_scores) == 1:
        for score in list_of_max_scores:
            if score['type'] == 'DRUG':
                print('I found 1 DRUG matching your search criteria.')
            if score['type'] == 'REGIMEN':
                print('I found 1 REGIMEN matching your search criteria.')
        return list_of_max_scores
    if len(list_of_max_scores) > 1:
        print('I found multiple matches for your query which I can not distinguish from one another. Please try again with a more descriptive name.')
        quit()


def get_rx_entry_from_id(key, list_of_max_scores):
    for score in list_of_max_scores:
        id = score['id']
    url = 'https://api.seer.cancer.gov/rest/rx/latest/id/{}'.format(id)
    headers = {'X-SEERAPI-Key': key}
    req = requests.get(url, headers=headers)
    json_response = req.json()
    return json_response


def parse_desired_drug_data_from_json_response(resultant_dict):
    user_content_depth_selection = (input('What data are you looking for?\n1.) Very detailed drug information\n2.)'
                                          ' A broad overview of this drug\n3.) Alternate names for this drug\n4.) '
                                          'Primary site & histology information\n5.) Remarks, including recent FDA '
                                          'approvals, news, and history\n6.) Drug categorization'))
    if (user_content_depth_selection == 1 or user_content_depth_selection == '1.' or user_content_depth_selection
            == '1.)'or user_content_depth_selection == '1)' or user_content_depth_selection.lower() == 'one'):
        name = resultant_dict['name']
        print(name)
        alternate_name = resultant_dict['alternate_name']
        print(alternate_name)
        category = resultant_dict['category']
        print(category)
        subcategory = resultant_dict['subcategory']
        print(subcategory)
        primary_site = resultant_dict['primary_site']
        print(primary_site)
        remarks = resultant_dict['remarks']
        print(remarks)


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
user_verifies_max_score_correctness(best_match)
dict_of_specific_drug_result = get_rx_entry_from_id(args.key, best_match)
#print(json.dumps(dict_of_specific_drug_result, indent=2))
parse_desired_drug_data_from_json_response(dict_of_specific_drug_result)
