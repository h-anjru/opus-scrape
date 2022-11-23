# opus-scrape
Scrape the human-readable, ASCII solutions from NGS' OPUS from multiple solutions into a single CSV.

## How it works
This script searches for certain key phrases in the OPUS solution that indicate where a value of interest may be. It then performs a regex search to pull the value from that line of the OPUS solution, eventually placing all found values into a Pandas dataframe that is printed into a CSV.

The key phrases and how to find the value of interest are stored in an easy-to-read, easy-to-edit YAML.

## Example
From the `search_criteria.yaml` file, you see that one of the items searched for is `Northing [m]`, accompanied by the following items:
```yaml
Northing [m]:
  search_for: 'Northing (Y) [meters]'
  regex_str: '[0-9]+\.[0-9]+'
  group_number: 1
```
To find the Northing coordinate (state plane) from the solution, the script searches line by line through the solution, stopping at the line containing the `search_for` term. From the OPUS solution:
```
Northing (Y) [meters]     4934835.846           103778.178
```
 The script then performs a regular expression search using the `regex_str` and the `group_number`:
```py
value = regex.findall(search_info['regex_str'], line)[search_info['group_number']]
```
The `group_number` will grab the second coordinate `[1]` and skip the first `[0]`. 

This process repeated for every item in the YAML.

## Work in progress
This script has only been tested so far on OPUS-RS (rapid static) solutions.