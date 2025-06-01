import json

findings_filepath = 'integration/20250601-035443-JulesParadox/findings.json'
readme_filepath = 'integration/20250601-035443-JulesParadox/README.md'

# Load existing findings
try:
    with open(findings_filepath, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: Findings file not found at {findings_filepath}")
    # Initialize with a basic structure if not found, though it should exist from previous steps
    data = {
        "agent_id": "20250601-035443-JulesParadox",
        "phenomenon": "integration",
        "task_type": "synthesis",
        "key_findings": [],
        "confidence": 0.5,
        "surprising_results": [],
        "contradicts": [],
        "supports": [],
        "next_priority": ""
    }

# New paradoxes to add
paradoxes = [
    {
        "summary": "Sustained quantum coherence, essential for many proposed quantum biological effects, seems improbable in warm, wet, and noisy cellular environments.",
        "sources": ["NavCritic/20250531-161500", "General literature"],
        "implicated_phenomena": ["All quantum biology"],
        "details": "Quantum coherence is exceedingly fragile and typically requires cryogenic temperatures and extreme isolation. Biological systems are the antithesis of this—warm, aqueous, and bustling with molecular motion. How life manages to protect, sustain, or even regenerate quantum coherence long enough for functional effects (e.g., in photosynthesis, navigation) is a profound mystery. It challenges our understanding of both quantum mechanics in complex systems and the limits of biological adaptation.",
        "agent_source_ids": ["20250531-161500-NavCritic"]
    },
    {
        "summary": "The vibration theory of olfaction (quantum tunneling based) challenges the classical shape-based theory, with conflicting experimental evidence.",
        "sources": ["SmellFirst/20250531-162500"],
        "implicated_phenomena": ["Olfaction"],
        "details": "The dominant paradigm for smell (olfaction) is 'odorant shape theory' (lock-and-key). However, the 'vibration theory of olfaction' posits that olfactory receptors detect molecular vibrations via inelastic electron tunneling. This quantum mechanism could explain phenomena shape theory cannot (e.g., why isotopes can smell different). However, experimental evidence is contested, and the biological machinery for such quantum detection is not fully understood, creating a paradox between competing theories and ambiguous data.",
        "agent_source_ids": ["20250531-162500-SmellFirst"]
    },
    {
        "summary": "Enzymes achieve reaction rates far exceeding classical predictions, strongly implicating quantum tunneling, but the precise mechanisms of how enzymes promote tunneling are still debated.",
        "sources": ["EnzMech/20240315-100000", "ORCHESTRATION.md"],
        "implicated_phenomena": ["Enzymes", "DNA mutations"],
        "details": "Many enzymes accelerate reactions by factors that classical transition state theory cannot explain. Quantum tunneling, where particles (often protons or electrons) pass through energy barriers rather than over them, is a key explanation. The paradox lies in understanding how enzyme structures and dynamics are so exquisitely 'tuned' to facilitate and control tunneling pathways, effectively manipulating quantum phenomena for biological catalysis.",
        "agent_source_ids": ["20240315-100000-20250531-162000-EnzMech"]
    },
    {
        "summary": "Research agents tasked with identifying scientific paradoxes face an operational paradox due to limitations in accessing primary scientific literature directly.",
        "sources": ["NavCritic/20250531-161500", "PhotoTheory/20250531-161000"],
        "implicated_phenomena": ["Research Methodology"],
        "details": "This is a meta-paradox concerning the operational capabilities of the research agents themselves. Agents NavCritic and PhotoTheory reported difficulties accessing scientific literature due to web restrictions (robots.txt, etc.). This creates a paradox where agents designed for knowledge discovery are limited in their ability to consult primary sources, potentially hindering the depth and breadth of their analysis.",
        "agent_source_ids": ["20250531-161500-NavCritic", "20250531-161000-PhotoTheory"]
    }
]

# Ensure "key_findings" and "supports" are lists
if "key_findings" not in data or not isinstance(data["key_findings"], list):
    data["key_findings"] = []
if "supports" not in data or not isinstance(data["supports"], list):
    data["supports"] = []

# Update findings.json
for p_info in paradoxes:
    key_finding_str = f"Paradox: {p_info['summary']} (Sources: {', '.join(p_info['sources'])}. Implicated: {', '.join(p_info['implicated_phenomena'])}. Details: {p_info['details']})"
    if key_finding_str not in data["key_findings"]:
        data["key_findings"].append(key_finding_str)
    for agent_id in p_info.get("agent_source_ids", []):
        if agent_id not in data["supports"]:
            data["supports"].append(agent_id)

data["confidence"] = 0.8
data["next_priority"] = "Seek experimental proposals or theoretical models aiming to resolve these identified paradoxes. Investigate contradictions between different phenomena if new findings emerge."

with open(findings_filepath, 'w') as f:
    json.dump(data, f, indent=2)
print(f"Updated {findings_filepath} with new paradoxes.")

# Update README.md
readme_content = []
try:
    with open(readme_filepath, 'r') as f:
        readme_content = f.readlines()
except FileNotFoundError:
    print(f"Warning: README file not found at {readme_filepath}. Will create a new one.")
    readme_content.append(f"# Paradox Identification in Quantum Biology - Agent JulesParadox\n\n") # Basic header if missing

# Remove trailing newlines to prevent excessive spacing
readme_content = [line.rstrip('\n') for line in readme_content]
# Add back newlines uniformly
readme_content = [line + '\n' for line in readme_content]


# Ensure "Identified Paradoxes" section exists, and it's correctly named
# The original task used "Identified Paradoxes"
# The user script uses "Identified Paradoxes and Contradictions"
# I will stick to "Identified Paradoxes" as used in previous steps for consistency with current README
section_header_text = "Identified Paradoxes"
# Find if header exists, case insensitive, allowing for "## " prefix
header_found = False
header_index = -1
for i, line in enumerate(readme_content):
    if section_header_text.lower() in line.lower() and line.strip().startswith("##"):
        header_found = True
        header_index = i
        break

if not header_found:
    readme_content.append("\n## " + section_header_text + "\n") # Add section header if not found
else:
    # Ensure there's a newline after the header if content follows directly
    if header_index + 1 < len(readme_content) and readme_content[header_index+1].strip() != "":
         readme_content.insert(header_index + 1, "\n")


# Append new paradoxes to README
# We need to make sure we don't re-add existing paradoxes to the README.
# The simplest way is to check if the summary is already present.
# The first paradox (Constructive Role of Noise) is already in the README from previous steps.

existing_readme_text = "".join(readme_content)
paradox_section_start_index = -1
for i, line in enumerate(readme_content):
    if "## Identified Paradoxes" in line: # Use the title I've been using
        paradox_section_start_index = i
        break

# The first paradox from the previous steps should already be in readme_content.
# The new `paradoxes` list contains different items.
# Let's re-evaluate how to best merge. The provided script appends all from `paradoxes` list.
# The first paradox ("Environmental noise...") is NOT in the `paradoxes` list in the user's prompt.
# So, the script will just append the new ones.

# The previous README content for "Identified Paradoxes" was:
# ## Identified Paradoxes
#
# ### 1. The Constructive Role of Noise in Quantum Biological Systems
# ...
#
# We should add the new paradoxes starting from "### 2." or just "###"
# The user script just uses "### Paradox: {summary}" which is fine.

readme_update_text = []
for p_info in paradoxes:
    # Check if this paradox summary is already in the README to avoid duplication
    if p_info['summary'] not in existing_readme_text:
        readme_update_text.append(f"\n### Paradox: {p_info['summary']}\n") # Add a leading newline for spacing from previous entry
        readme_update_text.append(f"- **Sources:** {', '.join(p_info['sources'])}\n")
        readme_update_text.append(f"- **Implicated Phenomena:** {', '.join(p_info['implicated_phenomena'])}\n")
        readme_update_text.append(f"- **Description:** {p_info['details']}\n")
        readme_update_text.append(f"- **Relevant Agent Findings:** {', '.join(p_info.get('agent_source_ids', ['N/A']))}\n\n")

if paradox_section_start_index != -1:
    # Insert new paradoxes at the end of the identified paradoxes section
    # This is simplified: just append to the whole content, assuming the section is last or structure is simple.
    readme_content.extend(readme_update_text)
else: # Should not happen given previous steps, but as a fallback
    readme_content.extend(readme_update_text)

with open(readme_filepath, 'w') as f:
    f.writelines(readme_content)
print(f"Updated {readme_filepath} with detailed descriptions of new paradoxes.")
