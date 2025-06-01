#!/usr/bin/env python3
"""
Improved aggregation script for findings.json files
Handles encoding issues and validates data before processing
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
        self.phenomena = ['photosynthesis', 'navigation', 'enzymes', 'olfaction', 'dna', 'integration']
        
    def collect_findings(self):
        """Recursively find and load all findings.json files"""
        for findings_file in self.repo_root.rglob('findings.json'):
            try:
                with open(findings_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                    # Handle markdown-wrapped JSON
                    if content.startswith('```'):
                        lines = content.split('\n')
                        # Find the actual JSON start and end
                        json_start = None
                        json_end = None
                        for i, line in enumerate(lines):
                            if line.strip() == '{' and json_start is None:
                                json_start = i
                            if line.strip() == '}':
                                json_end = i
                        
                        if json_start is not None and json_end is not None:
                            content = '\n'.join(lines[json_start:json_end+1])
                    
                    data = json.loads(content)
                    data['file_path'] = str(findings_file.relative_to(self.repo_root))
                    
                    # Validate required fields
                    required_fields = ['agent_id', 'phenomenon']
                    if all(field in data for field in required_fields):
                        self.findings.append(data)
                    else:
                        missing = [f for f in required_fields if f not in data]
                        print(f"Skipping {findings_file.name}: missing {missing}")
                        
            except json.JSONDecodeError as e:
                print(f"JSON error in {findings_file.name}: {e}")
            except Exception as e:
                print(f"Error loading {findings_file.name}: {e}")
                
    def analyze_findings(self):
        """Extract patterns, contradictions, and priorities"""
        analysis = {
            'total_agents': len(set(f.get('agent_id', 'unknown') for f in self.findings)),
            'total_findings': len(self.findings),
            'phenomena_activity': Counter(f.get('phenomenon', 'unknown') for f in self.findings),
            'high_confidence': [],
            'contradictions': [],
            'emerging_patterns': [],
            'next_priorities': Counter(),
            'surprising_results': []
        }
        
        # Group findings by key findings text
        finding_groups = defaultdict(list)
        for f in self.findings:
            for finding in f.get('key_findings', []):
                finding_groups[finding].append(f)
        
        # Identify high-confidence findings (multiple agents agree)
        for finding, agents in finding_groups.items():
            if len(agents) >= 2:  # Lowered threshold since we have fewer total findings
                confidences = [a.get('confidence', 0.5) for a in agents]
                avg_confidence = sum(confidences) / len(confidences)
                analysis['high_confidence'].append({
                    'finding': finding,
                    'confidence': avg_confidence,
                    'agent_count': len(agents),
                    'first_agent': agents[0].get('agent_id', 'unknown')
                })
        
        # Find contradictions
        for f in self.findings:
            contradicts = f.get('contradicts', [])
            if contradicts:
                for contradicted_id in contradicts:
                    analysis['contradictions'].append({
                        'agent': f.get('agent_id', 'unknown'),
                        'phenomenon': f.get('phenomenon', 'unknown'),
                        'contradicts': contradicted_id
                    })
        
        # Collect surprising results
        for f in self.findings:
            for surprise in f.get('surprising_results', []):
                analysis['surprising_results'].append({
                    'agent': f.get('agent_id', 'unknown'),
                    'phenomenon': f.get('phenomenon', 'unknown'),
                    'finding': surprise
                })
        
        # Aggregate next priorities
        for f in self.findings:
            next_priority = f.get('next_priority')
            if next_priority:
                analysis['next_priorities'][next_priority] += 1
                
        return analysis
        
    def generate_summary(self, analysis):
        """Create the markdown summary"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        summary = f"""# Quantum Biology Research: Findings Summary
*Generated: {now} | Agents: {analysis['total_agents']} | Findings: {analysis['total_findings']}*

## 🔥 High-Confidence Discoveries
*Findings supported by multiple agents*

"""
        # Add high confidence findings
        if analysis['high_confidence']:
            for finding in sorted(analysis['high_confidence'], key=lambda x: x['confidence'], reverse=True)[:10]:
                summary += f"- **{finding['finding'][:100]}{'...' if len(finding['finding']) > 100 else ''}**\n"
                summary += f"  - Confidence: {finding['confidence']:.2f} | Agents: {finding['agent_count']} | First: {finding['first_agent']}\n\n"
        else:
            summary += "*No multi-agent consensus findings found yet.*\n\n"
        
        # Add phenomena activity
        summary += "## 📊 Research Activity by Phenomenon\n\n"
        for phenomenon, count in analysis['phenomena_activity'].most_common():
            summary += f"- **{phenomenon.title()}**: {count} findings\n"
        
        # Add surprising results
        if analysis['surprising_results']:
            summary += "\n## 🚨 Surprising Results\n*The 'wait, what?' moments*\n\n"
            for surprise in analysis['surprising_results'][:10]:
                summary += f"- **{surprise['agent']}** ({surprise['phenomenon']}): {surprise['finding'][:150]}{'...' if len(surprise['finding']) > 150 else ''}\n"
        
        # Add next priorities
        if analysis['next_priorities']:
            summary += "\n## 🎯 Converging Research Priorities\n*What multiple agents suggest as next steps*\n\n"
            for priority, count in analysis['next_priorities'].most_common(10):
                summary += f"- **{priority[:100]}{'...' if len(priority) > 100 else ''}** ({count} agents)\n"
        
        # Add contradictions
        if analysis['contradictions']:
            summary += "\n## 🔄 Active Contradictions\n*Where agents disagree - valuable for future research*\n\n"
            for contradiction in analysis['contradictions'][:5]:
                summary += f"- **{contradiction['agent']}** ({contradiction['phenomenon']}) contradicts: {contradiction['contradicts']}\n"
        
        summary += f"\n---\n*This summary automatically aggregates findings from all agent folders following the ORCHESTRATION.md format.*"
        
        return summary
        
    def run(self):
        """Main execution"""
        print("🔍 Collecting findings from agent folders...")
        self.collect_findings()
        
        if not self.findings:
            print("❌ No valid findings.json files found!")
            return
            
        print(f"✅ Found {len(self.findings)} valid findings from {len(set(f.get('agent_id', 'unknown') for f in self.findings))} agents")
        
        print("📊 Analyzing patterns and connections...")
        analysis = self.analyze_findings()
        
        print("📝 Generating summary...")
        summary = self.generate_summary(analysis)
        
        # Write summary
        summary_path = self.repo_root / 'findings-summary.md'
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
            
        print(f"✅ Summary written to {summary_path}")
        
        # Also create a JSON version for other tools
        analysis_path = self.repo_root / 'findings-analysis.json'
        # Convert Counter objects to regular dicts for JSON serialization
        json_analysis = {}
        for key, value in analysis.items():
            if isinstance(value, Counter):
                json_analysis[key] = dict(value)
            else:
                json_analysis[key] = value
                
        with open(analysis_path, 'w', encoding='utf-8') as f:
            json.dump(json_analysis, f, indent=2, default=str)
            
        print(f"📊 Analysis data written to {analysis_path}")
        
        # Print quick stats
        print(f"\n📈 Quick Stats:")
        print(f"- Total phenomena covered: {len(analysis['phenomena_activity'])}")
        print(f"- High-confidence findings: {len(analysis['high_confidence'])}")
        print(f"- Surprising results: {len(analysis['surprising_results'])}")
        print(f"- Convergent priorities: {len(analysis['next_priorities'])}")

if __name__ == "__main__":
    aggregator = FindingsAggregator()
    aggregator.run()
