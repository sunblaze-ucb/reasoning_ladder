import os
import json
import pandas as pd
from collections import defaultdict


def is_valid_file(name):
    return not name.startswith('.') and name != '.DS_Store'


# Initialize a dictionary to store results
results = defaultdict(dict)

# Root results folder
root_dir = 'results'

# Traverse through each model directory
for model_name in os.listdir(root_dir):
    # if not "openr1_lg_2k" in model_name:
    #     continue
    if not is_valid_file(model_name):
        continue
    model_dir = os.path.join(root_dir, model_name)
    if not os.path.isdir(model_dir):
        continue

    # Each model has only one checkpoint folder
    ckpt_dirs = [d for d in os.listdir(model_dir) if is_valid_file(d)]
    if not ckpt_dirs:
        continue
    for ckpt_dir in ckpt_dirs:
        ckpt_path = os.path.join(model_dir, ckpt_dir)

        for file_name in os.listdir(ckpt_path):
            if file_name.endswith('.jsonl') and is_valid_file(file_name) and "aime24_nofigures_agg8" in file_name:
                file_path = os.path.join(ckpt_path, file_name)
                with open(file_path, 'r') as f:
                    for line in f:
                        data = json.loads(line)
                        problem_id = data['doc']['id']

                        if 'exact_matches' in data:
                            correctness = data['exact_matches']
                            results[problem_id][model_name] = sum(correctness) / len(correctness)
                        else:
                            correctness = data['exact_match']
                            results[problem_id][model_name] = correctness


# Convert to DataFrame
df = pd.DataFrame.from_dict(results, orient='index').sort_index()

# Define difficulty tiers
easy = [69, 60, 67, 72]
medium = [84, 71, 68, 75, 86, 66, 83, 78, 79, 82]
hard = [70, 74, 76, 77, 87, 85, 64, 65, 80, 61, 88, 73]
exhard = [89, 62, 81, 63]

# Create a new DataFrame to store tier averages
tier_results = pd.DataFrame(index=['easy', 'medium', 'hard', 'exhard'])

# Sort the columns alphabetically
sorted_columns = sorted(df.columns)

# Calculate average performance for each tier and model
for model in sorted_columns:
    # Calculate mean for each tier, handling potential missing values
    tier_results.loc['easy', model] = df.loc[easy, model].mean()
    tier_results.loc['medium', model] = df.loc[medium, model].mean()
    tier_results.loc['hard', model] = df.loc[hard, model].mean()
    tier_results.loc['exhard', model] = df.loc[exhard, model].mean()

# Print results with tab separation
formatted_tier_results = tier_results.applymap(lambda x: f"{x:.2%}")
print(formatted_tier_results.to_csv(sep="\t"))
