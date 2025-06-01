# Quantum Biology Multi-Agent Research Orchestration

## 🎯 Mission Brief
Explore quantum mechanics in biological systems across 5 phenomena. Each agent works independently in parallel branches. This system scales to any number of agents without coordination overhead.

## 🏗️ Architecture for Parallel Agents

### File Structure (CRITICAL - Prevents Merge Conflicts)
```
quantum-biology/
├── photosynthesis/
│   ├── literature/
│   │   └── [YYYYMMDD-HHMMSS-AgentID]/
│   ├── theory/
│   │   └── [YYYYMMDD-HHMMSS-AgentID]/
│   ├── experiments/
│   │   └── [YYYYMMDD-HHMMSS-AgentID]/
│   └── synthesis/
│       └── [YYYYMMDD-HHMMSS-AgentID]/
├── navigation/
│   └── [same structure]
├── enzymes/
│   └── [same structure]
├── olfaction/
│   └── [same structure]
├── dna/
│   └── [same structure]
└── integration/
    └── [cross-phenomenon work]
```

### Agent Workflow (No Coordination Needed)
1. **Generate unique ID**: `YYYYMMDD-HHMMSS-AgentName` (e.g., `20250531-143022-Alpha7`)
2. **Pick any task**: No claiming needed - just start working
3. **Create your folder**: Always use your unique timestamp folder
4. **Work freely**: You'll never conflict with other agents
5. **Submit PR**: Title: `[Phenomenon-Type] Brief description - AgentID`

## 📦 Task Packages (Self-Contained Work Units)

### Each agent should produce:
```
[YourTimestampFolder]/
├── README.md          # What you did and found
├── findings.json      # Structured data for later aggregation
├── sources.bib        # Papers/resources you used
├── analysis/          # Your computations/visualizations
├── raw_data/          # Original materials
└── next_questions.md  # What to investigate next
```

### 📋 Format Requirements (CRITICAL for Auto-Aggregation)

#### ✅ Required File Structure
Every agent folder MUST contain these files for successful aggregation:

```
[YourTimestampFolder]/
├── README.md          # ✅ REQUIRED: Overview of your work
├── findings.json      # ✅ REQUIRED: Machine-readable results  
├── sources.bib        # ✅ REQUIRED: References (even if empty)
├── next_questions.md  # ✅ REQUIRED: Future research directions
├── analysis/          # ✅ REQUIRED: Code, calculations, plots
│   └── [your analysis files]
└── raw_data/          # ✅ REQUIRED: Source materials, datasets
    └── [your data files]
```

**⚠️ Common Mistakes to Avoid:**
- Missing `analysis/` or `raw_data/` directories (create them even if empty)
- `findings.json` wrapped in markdown code blocks (use plain JSON)
- Invalid timestamp format (must be `YYYYMMDD-HHMMSS-AgentName`)

#### 🎯 findings.json Template (Copy & Modify)
```json
{
  "agent_id": "YYYYMMDD-HHMMSS-YourAgentName",
  "phenomenon": "photosynthesis",
  "task_type": "theory", 
  "key_findings": [
    "First major finding - be specific and actionable",
    "Second finding - quantify when possible", 
    "Third finding - highlight unexpected results"
  ],
  "confidence": 0.8,
  "surprising_results": [
    "The most unexpected discovery was...",
    "Contrary to expectations, we found..."
  ],
  "contradicts": [],
  "supports": [
    "Previous work by Agent-XYZ showing similar patterns"
  ],
  "next_priority": "Investigate the specific mechanism behind finding #1 using method X"
}
```

**Field Validation:**
- `phenomenon`: Must be exactly one of: `photosynthesis`, `navigation`, `enzymes`, `olfaction`, `dna`, `integration`
- `task_type`: Must be exactly one of: `literature`, `theory`, `experiments`, `synthesis`  
- `confidence`: Float between 0.0 and 1.0 (0.7+ recommended for solid findings)
- `key_findings`: Array of 2-5 specific, actionable findings
- `next_priority`: Single, specific next research question

#### 📝 README.md Template
```markdown
# [Phenomenon] [Task Type] - Agent [YourTimestamp]

## Mission
Brief description of what you investigated and why.

## Key Findings
1. **Finding 1**: Detailed explanation with evidence
2. **Finding 2**: Quantitative results when possible  
3. **Finding 3**: Unexpected discoveries highlighted

## Methodology
How you approached the problem (literature search, calculations, etc.)

## Limitations
What you couldn't investigate and why

## Files in this Package
- `README.md`: This overview
- `findings.json`: Structured results for aggregation
- `sources.bib`: References used
- `analysis/`: [Describe your analysis files]
- `raw_data/`: [Describe your data sources]
- `next_questions.md`: Future research directions

## Connection to Other Work
How your findings relate to other agents' work (if known)
```

---

## 🔬 Research Domains & Key Questions

### 1️⃣ PHOTOSYNTHESIS - Quantum Coherence
**Core Mystery**: How do plants achieve 95% energy transfer efficiency?

**Literature Mining Focus**:
- FMO complex structure and dynamics
- Coherence timescales vs temperature
- Which organisms show strongest effects
- Energy transfer pathways
- Protection mechanisms against decoherence

**Theory Development Focus**:
- Förster theory limitations
- Quantum walk models
- Environment-assisted quantum transport
- Coherence vs entanglement roles
- Optimal transport networks

**Experimental Proposals**:
- 2D spectroscopy improvements
- Artificial light-harvesting designs
- Temperature/pressure dependencies
- Isotope substitution effects
- Biomimetic quantum wires

**Synthesis Goals**:
- Universal efficiency principles
- Evolutionary optimization paths
- Engineering design rules
- Quantum computer architectures inspired by photosynthesis

---

### 2️⃣ NAVIGATION - Radical Pair Mechanism
**Core Mystery**: How do birds sense magnetic fields with quantum entanglement?

**Literature Mining Focus**:
- Cryptochrome structures and variants
- Behavioral evidence across species
- RF disruption experiments
- Magnetic field sensitivities
- Evolution of magnetoreception

**Theory Development Focus**:
- Spin chemistry in proteins
- Decoherence protection in warm systems
- Signal amplification mechanisms
- Entanglement measures
- Classical vs quantum compass models

**Experimental Proposals**:
- In vivo quantum state detection
- Genetic modifications to test theory
- Artificial quantum compasses
- Isotope effects on navigation
- Time-resolved spin measurements

**Synthesis Goals**:
- Quantum sensor design principles
- Biological quantum information processing
- Evolution of quantum traits
- Medical applications of spin chemistry

---

### 3️⃣ ENZYMES - Quantum Tunneling
**Core Mystery**: How do enzymes break the speed limit of classical chemistry?

**Literature Mining Focus**:
- Kinetic isotope effects
- Temperature-independent catalysis
- Enzyme families with tunneling
- Reaction rate enhancements
- Computational tunneling studies

**Theory Development Focus**:
- Beyond transition state theory
- Coupled tunneling mechanisms
- Protein dynamics role
- Marcus theory extensions
- Quantum rate theories

**Experimental Proposals**:
- Ultrafast catalysis measurements
- Heavy atom substitutions
- Pressure effects on tunneling
- Single molecule enzymology
- Quantum control of reactions

**Synthesis Goals**:
- Industrial catalyst design
- Drug development implications
- Metabolic efficiency principles
- Quantum effects in aging

---

### 4️⃣ OLFACTION - Quantum Vibration Sensing
**Core Mystery**: Does the nose use quantum mechanics to smell?

**Literature Mining Focus**:
- Turin's theory evidence
- Isotope discrimination tests
- Odorant-receptor interactions
- Behavioral studies
- Competing theories

**Theory Development Focus**:
- Inelastic electron tunneling
- Vibration-to-perception mapping
- Shape vs vibration reconciliation
- Quantum sensor mechanisms
- Prediction accuracy comparisons

**Experimental Proposals**:
- Deuterated molecule libraries
- Receptor mutation studies
- Artificial quantum noses
- Time-resolved olfaction
- Critical test designs

**Synthesis Goals**:
- Quantum sensor technology
- Disease detection methods
- Flavor/fragrance industry applications
- Evolution of chemical sensing

---

### 5️⃣ DNA - Quantum Mutations
**Core Mystery**: Do quantum effects drive genetic variation?

**Literature Mining Focus**:
- Proton tunneling evidence
- Tautomer stability
- UV-induced quantum processes
- Mutation rate anomalies
- Quantum effects in replication

**Theory Development Focus**:
- Tunneling in base pairs
- Decoherence in DNA
- Quantum error correction analogs
- Superposition in genetics
- Evolution rate implications

**Experimental Proposals**:
- Single DNA molecule quantum states
- Isotope effects on mutations
- Quantum control of genetics
- Time-resolved base pair dynamics
- Environmental quantum effects

**Synthesis Goals**:
- Cancer mechanism insights
- Directed evolution tools
- Origin of life theories
- Quantum biology of aging

---

## 🌐 Integration Opportunities

### Cross-Phenomenon Patterns
Work in `integration/` folder to find:
- Common quantum protection mechanisms
- Temperature thresholds across systems
- Evolutionary convergence on quantum solutions
- Universal mathematical frameworks
- Biomimetic design principles

### Meta-Analysis Tasks
- Build quantum biology ontology
- Create mechanism comparison matrix
- Identify contradictions between domains
- Find unexpected connections
- Propose unified theories

---

## 🚀 Agent Instructions

### Starting Your Mission
1. **Choose based on your strengths** (physics background → theory, biology → literature, CS → synthesis)
2. **Dive deep or go broad** (single phenomenon expert vs integration generalist)
3. **Work independently** (assume you're the only agent in the universe)
4. **Be thorough** (better to complete one task well than many poorly)
5. **Document surprises** (the "wait, what?" moments are gold)

### Quality Markers
- **Literature**: 20+ sources minimum, focus on 2020-2025
- **Theory**: Mathematical frameworks, testable predictions
- **Experiments**: Feasible with current or near-term technology
- **Synthesis**: Connect to applications and bigger pictures

### Remember
- You're building a piece of a larger puzzle
- Other agents are working in parallel on other pieces
- Your timestamp folder ensures zero conflicts
- The findings.json enables automatic knowledge aggregation
- Focus on finding what doesn't fit current understanding

---

## 📊 Scalability Features

This orchestration system handles:
- **1 agent**: Deep dive into one area
- **10 agents**: Parallel exploration of all phenomena
- **100 agents**: Multiple perspectives per task
- **1000+ agents**: Exhaustive parameter space exploration

The timestamp-based folders and structured JSON outputs mean infinite agents can work without coordination, conflicts, or communication overhead. The human merge process becomes simple: accept all PRs (no conflicts possible) and run aggregation scripts on the JSON files.

## 🎯 Success Metrics

Each agent contribution is valuable if it:
1. Adds new knowledge (literature)
2. Clarifies mechanisms (theory)
3. Suggests validations (experiments)
4. Finds connections (synthesis)
5. Identifies contradictions (critical analysis)

The "best" contributions will likely be those that find contradictions between accepted theory and experimental data, or unexpected connections between phenomena.