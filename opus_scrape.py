import os
import pandas as pd
import regex
import yaml

# ---Input and output info; user edit here---
path_to_solutions = '/mnt/c/project_01/opus'
path_to_output = '/mnt/c/project_01/opus/output'
output_name = 'project_01.csv'


def scrape_opus_solution(infile, search_crit):
    """
    Scrape the text of the human-readable ASCII version of an NGS OPUS solution for any search criteria specified.
    """

    with open(infile, 'r') as f:
        # read all lines
        lines = f.readlines()

    temp_list_of_lists = []

    # results appended to list (cheaper than append/concat to dataframe)
    data_list = [None] * len(search_crit)

    # search lines until criterion met
    for line in lines:
        for index, (column_name, search_info) in enumerate(search_crit.items()):
            if search_info['search_for'] in line:
                # perform designated search
                value = regex.findall(search_info['regex_str'], line)[search_info['group_number']]

                # assign results to temp_list
                data_list[index] = value

    # after going through a single file, retuen list
    return data_list


def open_yaml(infile):
    """Bring in contents of a YAML as a dictionary."""

    with open(infile, 'r') as stream:
        try:
            # Converts YAML document to Python object
            d = yaml.safe_load(stream)
            return d
        except yaml.YAMLError as e:
            return e


# bring in YAML
path_to_yaml = 'search_criteria.yaml'
search_criteria = open_yaml(path_to_yaml)

# initialize a list for all returned data; will become list of lists
all_data = []

# open each OPUS solution
path = os.fsencode(path_to_solutions)

for file in os.listdir(path):
    filename = os.fsdecode(file)
    if filename.endswith('.txt'):  # assuming in a directory with only OPUS solutions as .txt files
        path_to_file = os.path.join(path_to_solutions, filename)
        data = scrape_opus_solution(path_to_file, search_criteria)
        all_data.append(data)
    else:
        continue

# grab column names from dict
column_names = []
for key in search_criteria:
    column_names.append(key)

# after all files searched, create dataframe for data scraped
df = pd.DataFrame(all_data, columns=column_names)

# print results in terminal
print(df)

# save output
if not os.path.exists(path_to_output):
    os.makedirs(path_to_output)

df.to_csv(os.path.join(path_to_output, output_name))
