import datetime
import os

timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
new_dir = f'integration/{timestamp}-JulesParadox'
print(f'New directory: {new_dir}')

os.makedirs(f'{new_dir}/analysis', exist_ok=True)
os.makedirs(f'{new_dir}/raw_data', exist_ok=True)

open(f'{new_dir}/README.md', 'w').close()
open(f'{new_dir}/findings.json', 'w').close()
open(f'{new_dir}/sources.bib', 'w').close()
open(f'{new_dir}/next_questions.md', 'w').close()

print(f'Created directory and files for {new_dir}')
