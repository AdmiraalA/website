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
        key_str = str(key)  # Convert key to a hashable type
        if key_str not in unique_results:
            unique_results[key_str] = result
        else:
            unique_results[key_str]['occurrences'].append(result['locations'][0]['physicalLocation']['artifactLocation']['uri'])

    combined_results = []
    for result in unique_results.values():
        combined_results.append(combine_occurrences(result))

    return combined_results

# Read SARIF file
with open('results.sarif', 'r') as file:
    sarif_data = json.load(file)

# Filter and combine duplicate entries
combined_results = filter_and_combine_duplicates(sarif_data)

# Add tool information from the action under the 'runs' array
tool_info = {
    'name': 'zaproxy-to-ghas',
    'version': '2.1.0'
}
sarif_data['runs'][0]['tool'] = {'driver': tool_info}

# Remove attempt to add tool information at the top level

# Write combined results to a new SARIF file
with open('combined_results.sarif', 'w') as file:
    json.dump(sarif_data, file, indent=2)
