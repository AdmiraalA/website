import json

def filter_duplicates(sarif_data):
    unique_results = {}
    filtered_results = []

    for result in sarif_data.get('runs', [])[0].get('results', []):
        key = (result.get('ruleId', ''), result.get('message', ''), result.get('level', ''))
        if key not in unique_results:
            unique_results[key] = result

    for key, value in unique_results.items():
        filtered_results.append(value)

    return filtered_results

# Read SARIF file
with open('temp_results.sarif', 'r') as file:
    sarif_data = json.load(file)

# Filter duplicate entries
filtered_results = filter_duplicates(sarif_data)

# Write filtered results to a new SARIF file
with open('filtered_results.sarif', 'w') as file:
    json.dump({"runs": [{"results": filtered_results}]}, file, indent=2)
