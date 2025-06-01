#!/usr/bin/env python3
"""
Focused compliance checker for quantum biology research agents
Only checks actual agent timestamped folders, ignores subdirectories
"""

import json
import os
from pathlib import Path
import re
from collections import defaultdict

class AgentComplianceChecker:
    def __init__(self, repo_root='.'):
        self.repo_root = Path(repo_root)
        self.required_files = ['README.md', 'findings.json', 'sources.bib', 'next_questions.md']
        self.required_json_fields = ['agent_id', 'phenomenon', 'task_type', 'key_findings', 'confidence']
        
    def is_agent_folder(self, folder_path):
        """Check if a folder is an agent folder based on timestamp format"""
        pattern = r'^\d{8}-\d{6}-.+$'
        return bool(re.match(pattern, folder_path.name))
        
    def find_agent_folders(self):
        """Find all actual agent folders in the repository"""
        agent_folders = []
        
        # Search in all subdirectories, but only include timestamped folders
        for root, dirs, files in os.walk(self.repo_root):
            # Filter dirs to only include timestamp-formatted folders
            for dir_name in dirs:
                full_path = Path(root) / dir_name
                if self.is_agent_folder(full_path):
                    agent_folders.append(full_path)
                    
        return sorted(agent_folders)
        
    def check_agent_compliance(self, agent_path):
        """Check compliance for a single agent"""
        results = {
            'path': str(agent_path.relative_to(self.repo_root)),
            'name': agent_path.name,
            'files_present': 0,
            'total_files': len(self.required_files),
            'findings_valid': False,
            'findings_complete': False,
            'issues': []
        }
        
        # Check required files
        for file_name in self.required_files:
            if (agent_path / file_name).exists():
                results['files_present'] += 1
            else:
                results['issues'].append(f"Missing {file_name}")
                
        # Check findings.json specifically
        findings_path = agent_path / 'findings.json'
        if findings_path.exists():
            try:
                with open(findings_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                # Check for markdown code blocks
                if content.startswith('```') or content.startswith('````'):
                    results['issues'].append("findings.json has markdown code blocks")
                else:
                    data = json.loads(content)
                    results['findings_valid'] = True
                    
                    # Check required fields
                    missing_fields = [f for f in self.required_json_fields if f not in data]
                    if not missing_fields:
                        results['findings_complete'] = True
                    else:
                        results['issues'].append(f"Missing JSON fields: {missing_fields}")
                        
            except json.JSONDecodeError:
                results['issues'].append("findings.json is not valid JSON")
            except Exception as e:
                results['issues'].append(f"Error reading findings.json: {e}")
                
        # Check directories
        if not (agent_path / 'analysis').exists():
            results['issues'].append("Missing analysis/ directory")
        if not (agent_path / 'raw_data').exists():
            results['issues'].append("Missing raw_data/ directory")
            
        return results
        
    def generate_summary(self):
        """Generate a compliance summary"""
        agent_folders = self.find_agent_folders()
        
        print("🔍 Quantum Biology Agent Compliance Report")
        print("=" * 50)
        print(f"Found {len(agent_folders)} agent folders\n")
        
        # Stats
        fully_compliant = 0
        mostly_compliant = 0
        needs_work = 0
        
        # Group by phenomenon
        by_phenomenon = defaultdict(list)
        
        for folder in agent_folders:
            results = self.check_agent_compliance(folder)
            
            # Determine phenomenon
            path_parts = folder.parts
            phenomenon = "unknown"
            if 'integration' in path_parts:
                phenomenon = 'integration'
            else:
                phenomena = ['photosynthesis', 'navigation', 'enzymes', 'olfaction', 'dna']
                for part in path_parts:
                    if part in phenomena:
                        phenomenon = part
                        break
                        
            by_phenomenon[phenomenon].append(results)
            
            # Calculate compliance score
            file_score = results['files_present'] / results['total_files']
            json_score = (int(results['findings_valid']) + int(results['findings_complete'])) / 2
            total_score = (file_score + json_score) / 2
            
            issue_count = len(results['issues'])
            
            if issue_count == 0:
                status = "✅ FULLY COMPLIANT"
                fully_compliant += 1
            elif issue_count <= 2:
                status = "⚠️  MOSTLY COMPLIANT"
                mostly_compliant += 1
            else:
                status = "❌ NEEDS WORK"
                needs_work += 1
                
            print(f"{status}: {results['name']}")
            if results['issues']:
                for issue in results['issues']:
                    print(f"  • {issue}")
                print()
                
        print(f"\n📊 Overall Summary:")
        print(f"• Fully compliant: {fully_compliant} ({fully_compliant/len(agent_folders)*100:.1f}%)")
        print(f"• Mostly compliant: {mostly_compliant} ({mostly_compliant/len(agent_folders)*100:.1f}%)")
        print(f"• Needs work: {needs_work} ({needs_work/len(agent_folders)*100:.1f}%)")
        
        print(f"\n📈 By Phenomenon:")
        for phenomenon, results_list in sorted(by_phenomenon.items()):
            fully = sum(1 for r in results_list if len(r['issues']) == 0)
            mostly = sum(1 for r in results_list if 1 <= len(r['issues']) <= 2)
            total = len(results_list)
            compliant_rate = (fully + mostly) / total * 100
            print(f"• {phenomenon}: {total} agents, {compliant_rate:.1f}% compliant (fully: {fully}, mostly: {mostly})")
            
        print(f"\n🎯 Key Insights:")
        
        # Most common issues
        all_issues = []
        for folder in agent_folders:
            results = self.check_agent_compliance(folder)
            all_issues.extend(results['issues'])
            
        issue_counts = defaultdict(int)
        for issue in all_issues:
            # Normalize similar issues
            if "Missing" in issue and "directory" in issue:
                issue_counts["Missing required directories"] += 1
            elif "Missing" in issue and ".md" in issue:
                issue_counts["Missing documentation files"] += 1
            elif "JSON" in issue:
                issue_counts["findings.json format issues"] += 1
            else:
                issue_counts[issue] += 1
                
        print("• Most common issues:")
        for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - {issue}: {count} agents")
            
        if fully_compliant + mostly_compliant >= len(agent_folders) * 0.8:
            print(f"\n🎉 Excellent! {(fully_compliant + mostly_compliant)/len(agent_folders)*100:.1f}% of agents are following the ORCHESTRATION.md format well.")
        else:
            print(f"\n⚠️  {needs_work} agents need attention to meet ORCHESTRATION.md requirements.")

if __name__ == "__main__":
    checker = AgentComplianceChecker()
    checker.generate_summary()
