import json

def combine_occurrences(result):
    occurrences = set()
    for location in result.get('locations', []):
        uri = location.get('physicalLocation', {}).get('artifactLocation', {}).get('uri')
        if uri:
            occurrences.add(uri)
    result['locations'] = [{'physicalLocation': {'artifactLocation': {'uri': ', '.join(occurrences)}}}]
    return result

def filter_and_combine_duplicates(sarif_data):
    unique_results = {}
    for result in sarif_data.get('runs', [])[0].get('results', []):
        key = (result.get('ruleId', ''), result.get('message', ''), result.get('level', ''))
        if key not in unique_results:
            unique_results[key] = result
        else:
            unique_results[key]['occurrences'].append(result['locations'][0]['physicalLocation']['artifactLocation']['uri'])

    combined_results = []
    for result in unique_results.values():
        combined_results.append(combine_occurrences(result))

    return combined_results

# Read SARIF file
with open('results.sarif', 'r') as file:
    sarif_data = json.load(file)

# Filter and combine duplicate entries
combined_results = filter_and_combine_duplicates(sarif_data)

# Write combined results to a new SARIF file
with open('combined_results.sarif', 'w') as file:
    json.dump({"runs": [{"results": combined_results}]}, file, indent=2)
