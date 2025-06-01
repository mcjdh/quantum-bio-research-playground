import json

# Content from read_files output (current findings.json)
original_findings_json_str = """
{
  "agent_id": "20250531-173500-BoundarySim",
  "phenomenon": "integration",
  "task_type": "synthesis",
  "key_findings": [],
  "phase_diagrams": [
    {
      "name": "Temperature vs. Coherence Time",
      "parameters": {
        "molecular_size": 100,
        "environment_name": "water",
        "environment_coupling": 1.0,
        "protection_strategy": "None",
        "temperature_range_K": "270-370 (50 points)"
      },
      "cliff_edge_description": "Coherence time drops below 1.0e-12 s. The simulation identifies the approximate temperature for this drop under the specified conditions.",
      "plot_file": "analysis/plot_temp_vs_coherence_water_None.png"
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
  "confidence": 0.5,
  "surprising_results": [],
  "contradicts": [],
  "supports": [],
  "next_priority": ""
}
"""

findings_data = json.loads(original_findings_json_str)

# Parameters from the Phase 2 simulation
PLOT_FILENAME="plot_system_size_vs_quantum_advantage_T310K.png"
FIXED_TEMPERATURE_K=310.0
L_BARRIER_A_MIN=0.1
L_BARRIER_A_MAX=1.0
L_BARRIER_A_STEPS=50
V0_EV=0.3
PROTON_WELL_WIDTH_A=0.5
CLIFF_THRESHOLD_ADVANTAGE=10.0

CLIFF_DESCRIPTION_PHASE2=f"Quantum Advantage (P_tunnel / P_classical) drops below {CLIFF_THRESHOLD_ADVANTAGE:.1f} as barrier width (system size proxy) increases. The simulation identifies the approximate barrier width for this drop at T={FIXED_TEMPERATURE_K}K."

# Update the second phase diagram entry
findings_data["phase_diagrams"][1]["parameters"] = {
    "system_size_proxy": "Barrier Width (Angstroms) for proton tunneling in DNA",
    "system_size_range": f"{L_BARRIER_A_MIN:.1f}-{L_BARRIER_A_MAX:.1f} A ({L_BARRIER_A_STEPS} steps)",
    "quantum_advantage_metric": "Ratio P_tunneling / P_classical",
    "fixed_temperature_K": FIXED_TEMPERATURE_K,
    "barrier_height_eV": V0_EV,
    "proton_well_width_A": PROTON_WELL_WIDTH_A
}
findings_data["phase_diagrams"][1]["cliff_edge_description"] = CLIFF_DESCRIPTION_PHASE2
findings_data["phase_diagrams"][1]["plot_file"] = f"analysis/{PLOT_FILENAME}"

# Update overall confidence
findings_data["confidence"] = 0.66

# Print the modified JSON
print(json.dumps(findings_data, indent=2))
