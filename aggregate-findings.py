## The Aggregation Script

### aggregate_findings.py

#!/usr/bin/env python3
"""
Aggregates findings.json files from all agents into FINDINGS_SUMMARY.md
Run from repository root: python scripts/aggregate_findings.py
"""

import json
import os
from datetime import datetime
from collections import defaultdict, Counter
from pathlib import Path

class FindingsAggregator:
    def __init__(self, repo_root='.'):
        self.repo_root = Path(repo_root)
        self.findings = []
        self.phenomena = ['photosynthesis', 'navigation', 'enzymes', 'olfaction', 'dna']
        
    def collect_findings(self):
        """Recursively find and load all findings.json files"""
        for findings_file in self.repo_root.rglob('findings.json'):
            try:
                with open(findings_file, 'r') as f:
                    data = json.load(f)
                    data['file_path'] = str(findings_file)
                    self.findings.append(data)
            except Exception as e:
                print(f"Error loading {findings_file}: {e}")
                
    def analyze_findings(self):
        """Extract patterns, contradictions, and priorities"""
        analysis = {
            'total_agents': len(set(f['agent_id'] for f in self.findings)),
            'total_findings': len(self.findings),
            'phenomena_activity': Counter(f['phenomenon'] for f in self.findings),
            'high_confidence': [],
            'contradictions': [],
            'emerging_patterns': [],
            'next_priorities': Counter(),
            'surprising_results': []
        }
        
        # Group findings by key findings
        finding_groups = defaultdict(list)
        for f in self.findings:
            for finding in f.get('key_findings', []):
                finding_groups[finding].append(f)
        
        # Identify high-confidence (multiple agents agree)
        for finding, agents in finding_groups.items():
            if len(agents) >= 3:
                avg_confidence = sum(a.get('confidence', 0) for a in agents) / len(agents)
                analysis['high_confidence'].append({
                    'finding': finding,
                    'confidence': avg_confidence,
                    'agent_count': len(agents),
                    'first_agent': agents[0]['agent_id']
                })
        
        # Find contradictions
        for f in self.findings:
            for contradicted_id in f.get('contradicts', []):
                # Find what was contradicted
                for other in self.findings:
                    if contradicted_id in str(other):
                        analysis['contradictions'].append({
                            'agent1': f['agent_id'],
                            'agent2': other.get('agent_id', 'unknown'),
                            'topic': f['phenomenon'],
                            'description': f.get('key_findings', [''])[0]
                        })
        
        # Collect surprising results
        for f in self.findings:
            for surprise in f.get('surprising_results', []):
                analysis['surprising_results'].append({
                    'agent': f['agent_id'],
                    'phenomenon': f['phenomenon'],
                    'finding': surprise
                })
        
        # Aggregate next priorities
        for f in self.findings:
            if 'next_priority' in f:
                analysis['next_priorities'][f['next_priority']] += 1
                
        return analysis
    
    def generate_summary(self, analysis):
        """Create the markdown summary"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        summary = f"""# Quantum Biology Research: Living Findings Summary
*Last updated: {now} | Total agents: {analysis['total_agents']} | Total findings: {analysis['total_findings']}*

## 🔥 Breakthrough Discoveries
<!-- High-confidence findings supported by multiple agents -->

"""
        # Add high confidence findings by phenomenon
        for phenomenon in self.phenomena:
            phenomenon_findings = [f for f in analysis['high_confidence'] 
                                  if any(a['phenomenon'] == phenomenon 
                                       for a in self.findings 
                                       if f['finding'] in a.get('key_findings', []))]
            if phenomenon_findings:
                summary += f"\n### {phenomenon.title()}\n"
                for f in sorted(phenomenon_findings, key=lambda x: x['confidence'], reverse=True)[:3]:
                    summary += f"- **{f['finding']}** - Confidence: {f['confidence']:.2f} ({f['agent_count']} agents agree)\n"
                    summary += f"  - First reported by: {f['first_agent']}\n\n"
        
        # Add contradictions section
        if analysis['contradictions']:
            summary += "\n## 🔄 Active Contradictions\n<!-- Where agents disagree - these are valuable! -->\n\n"
            summary += "### Major Debates\n"
            for i, c in enumerate(analysis['contradictions'][:5], 1):
                summary += f"{i}. **{c['topic'].title()} Finding**\n"
                summary += f"   - Agent {c['agent1']} vs Agent {c['agent2']}\n"
                summary += f"   - Regarding: {c['description'][:100]}...\n\n"
        
        # Add surprising results
        if analysis['surprising_results']:
            summary += "\n## 🚨 Surprising Results\n<!-- The 'wait, what?' moments -->\n\n"
            for s in analysis['surprising_results'][:10]:
                summary += f"1. **{s['agent']}** ({s['phenomenon']}): {s['finding']}\n"
        
        # Add next priorities
        if analysis['next_priorities']:
            summary += "\n## 🎯 Converging Priorities\n<!-- What multiple agents independently suggest as next steps -->\n\n"
            summary += "### Consensus Next Questions\n"
            for priority, count in analysis['next_priorities'].most_common(5):
                summary += f'1. **"{priority}"** ({count} agents)\n'
        
        # Add statistics
        summary += f"\n## 📊 Knowledge Graph Stats\n"
        summary += f"- Total findings: {analysis['total_findings']}\n"
        summary += f"- Active agents: {analysis['total_agents']}\n"
        summary += f"- Phenomena coverage: {dict(analysis['phenomena_activity'])}\n"
        
        summary += "\n---\n*Generated by aggregation script v1.0*"
        
        return summary
    
    def run(self):
        """Main execution"""
        print("Collecting findings...")
        self.collect_findings()
        
        if not self.findings:
            print("No findings.json files found!")
            return
            
        print(f"Found {len(self.findings)} findings from {len(set(f['agent_id'] for f in self.findings))} agents")
        
        print("Analyzing patterns...")
        analysis = self.analyze_findings()
        
        print("Generating summary...")
        summary = self.generate_summary(analysis)
        
        # Write summary
        summary_path = self.repo_root / 'FINDINGS_SUMMARY.md'
        with open(summary_path, 'w') as f:
            f.write(summary)
            
        print(f"Summary written to {summary_path}")
        
        # Also create a JSON version for other tools
        analysis_path = self.repo_root / 'findings_analysis.json'
        with open(analysis_path, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
            
        print(f"Detailed analysis written to {analysis_path}")

if __name__ == "__main__":
    aggregator = FindingsAggregator()
    aggregator.run()