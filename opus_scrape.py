import os
import pandas as pd
import regex
import yaml

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
        # opening a file
    with open(infile, 'r') as stream:
        try:
            # Converts yaml document to python object
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
path_to_opus = '/mnt/c/dev'
path = os.fsencode(path_to_opus)

for file in os.listdir(path):
    filename = os.fsdecode(file)
    if filename.endswith('.txt'):  # assuming in a directory with only OPUS solutions as .txt files
        data = scrape_opus_solution(filename, search_criteria)
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

# save to CSV
outpath = os.path.join(path_to_opus, 'all_coordinates.csv')
df.to_csv(outpath)
