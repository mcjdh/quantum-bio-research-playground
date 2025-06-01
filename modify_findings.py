import json

# Content from read_files output
original_findings_json_str = """
{
  "agent_id": "20250531-173500-BoundarySim",
  "phenomenon": "integration",
  "task_type": "synthesis",
  "key_findings": [],
  "phase_diagrams": [
    {
      "name": "Temperature vs. Coherence Time",
      "parameters": {},
      "cliff_edge_description": "",
      "plot_file": ""
    },
    {
      "name": "System Size vs. Quantum Advantage",
      "parameters": {},
      "cliff_edge_description": "",
      "plot_file": ""
    },
    {
      "name": "Noise Level vs. Efficiency",
      "parameters": {},
      "cliff_edge_description": "",
      "plot_file": ""
    }
  ],
  "confidence": 0.0,
  "surprising_results": [],
  "contradicts": [],
  "supports": [],
  "next_priority": ""
}
"""

findings_data = json.loads(original_findings_json_str)

# Parameters from the subtask description
PLOT_FILENAME="plot_temp_vs_coherence_water_None.png"
FIXED_MOLECULAR_SIZE=100
FIXED_ENV_NAME="water"
FIXED_ENV_COUPLING=1.0
FIXED_PROTECTION_STRATEGY="None"
CLIFF_THRESHOLD_S=1e-12

CLIFF_DESCRIPTION=f"Coherence time drops below {CLIFF_THRESHOLD_S:.1e} s. The simulation identifies the approximate temperature for this drop under the specified conditions."

# Update the first phase diagram entry
findings_data["phase_diagrams"][0]["parameters"] = {
    "molecular_size": FIXED_MOLECULAR_SIZE,
    "environment_name": FIXED_ENV_NAME,
    "environment_coupling": FIXED_ENV_COUPLING,
    "protection_strategy": FIXED_PROTECTION_STRATEGY,
    "temperature_range_K": "270-370 (50 points)" # As specified in the python script for phase 1
}
findings_data["phase_diagrams"][0]["cliff_edge_description"] = CLIFF_DESCRIPTION
findings_data["phase_diagrams"][0]["plot_file"] = f"analysis/{PLOT_FILENAME}"

# Update overall confidence
findings_data["confidence"] = 0.5

# Print the modified JSON
print(json.dumps(findings_data, indent=2))
