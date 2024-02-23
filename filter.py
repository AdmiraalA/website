import json

def combine_duplicates(sarif_data):
    unique_results = {}
    
    for result in sarif_data.get('runs', [])[0].get('results', []):
        key = (result.get('ruleId', ''), result.get('message', ''), result.get('level', ''))
        if key not in unique_results:
            unique_results[key] = {
                'result': result,
                'occurrences': [result['locations'][0]['physicalLocation']['artifactLocation']['uri']]
            }
        else:
            unique_results[key]['occurrences'].append(result['locations'][0]['physicalLocation']['artifactLocation']['uri'])
    
    combined_results = []
    
    for key, value in unique_results.items():
        combined_result = value['result']
        combined_result['locations'] = [{
            'physicalLocation': {
                'artifactLocation': {
                    'uri': ', '.join(value['occurrences'])
                }
            }
        }]
        combined_results.append(combined_result)
    
    return combined_results

# Read SARIF file
with open('temp_results.sarif', 'r') as file:
    sarif_data = json.load(file)

# Combine duplicate entries
combined_results = combine_duplicates(sarif_data)

# Write combined results to a new SARIF file
with open('combined_results.sarif', 'w') as file:
    json.dump({"runs": [{"results": combined_results}]}, file, indent=2)
