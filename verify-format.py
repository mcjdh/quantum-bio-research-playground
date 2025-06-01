#!/usr/bin/env python3
"""
Format verification script for quantum biology research agents
Checks compliance with ORCHESTRATION.md requirements
"""

import json
import os
from pathlib import Path
import re
from collections import defaultdict

class FormatVerifier:
    def __init__(self, repo_root='.'):
        self.repo_root = Path(repo_root)
        self.required_files = ['README.md', 'findings.json', 'sources.bib', 'next_questions.md']
        self.required_dirs = ['analysis', 'raw_data']
        self.required_json_fields = ['agent_id', 'phenomenon', 'task_type', 'key_findings', 'confidence']
        self.valid_phenomena = ['photosynthesis', 'navigation', 'enzymes', 'olfaction', 'dna', 'integration']
        self.valid_task_types = ['literature', 'theory', 'experiments', 'synthesis']
        
    def check_timestamp_format(self, folder_name):
        """Check if folder follows YYYYMMDD-HHMMSS-AgentID format"""
        pattern = r'^\d{8}-\d{6}-.+$'
        return bool(re.match(pattern, folder_name))
        
    def verify_agent_folder(self, agent_path):
        """Verify a single agent folder for compliance"""
        results = {
            'path': str(agent_path),
            'timestamp_format': self.check_timestamp_format(agent_path.name),
            'required_files_present': {},
            'required_dirs_present': {},
            'findings_json_valid': False,
            'findings_json_complete': False,
            'findings_json_errors': []
        }
        
        # Check required files
        for file_name in self.required_files:
            file_path = agent_path / file_name
            results['required_files_present'][file_name] = file_path.exists()
            
        # Check required directories
        for dir_name in self.required_dirs:
            dir_path = agent_path / dir_name
            results['required_dirs_present'][dir_name] = dir_path.exists()
            
        # Check findings.json specifically
        findings_path = agent_path / 'findings.json'
        if findings_path.exists():
            try:
                with open(findings_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Check for markdown code blocks
                    if content.strip().startswith('```') or content.strip().startswith('````'):
                        results['findings_json_errors'].append("Contains markdown code blocks")
                    else:
                        data = json.loads(content)
                        results['findings_json_valid'] = True
                        
                        # Check required fields
                        missing_fields = []
                        for field in self.required_json_fields:
                            if field not in data:
                                missing_fields.append(field)
                                
                        if not missing_fields:
                            results['findings_json_complete'] = True
                            
                            # Validate field values
                            if 'phenomenon' in data and data['phenomenon'] not in self.valid_phenomena:
                                results['findings_json_errors'].append(f"Invalid phenomenon: {data['phenomenon']}")
                                
                            if 'task_type' in data and data['task_type'] not in self.valid_task_types:
                                results['findings_json_errors'].append(f"Invalid task_type: {data['task_type']}")
                                
                            if 'confidence' in data:
                                try:
                                    conf = float(data['confidence'])
                                    if not (0.0 <= conf <= 1.0):
                                        results['findings_json_errors'].append(f"Confidence out of range: {conf}")
                                except (ValueError, TypeError):
                                    results['findings_json_errors'].append("Confidence not a valid number")
                        else:
                            results['findings_json_errors'].append(f"Missing required fields: {missing_fields}")
                            
            except json.JSONDecodeError as e:
                results['findings_json_errors'].append(f"JSON decode error: {e}")
            except Exception as e:
                results['findings_json_errors'].append(f"Error reading file: {e}")
                
        return results
        
    def scan_all_agents(self):
        """Scan entire repository for agent folders"""
        agent_folders = []
        
        # Look for timestamped folders in all phenomenon directories
        for phenomenon_dir in self.repo_root.iterdir():
            if phenomenon_dir.is_dir() and phenomenon_dir.name in self.valid_phenomena:
                # Look in subdirectories (literature, theory, experiments, synthesis)
                for task_type_dir in phenomenon_dir.iterdir():
                    if task_type_dir.is_dir():
                        for potential_agent in task_type_dir.iterdir():
                            if potential_agent.is_dir():
                                agent_folders.append(potential_agent)
                                
        # Also check integration folder directly
        integration_dir = self.repo_root / 'integration'
        if integration_dir.exists():
            for potential_agent in integration_dir.iterdir():
                if potential_agent.is_dir():
                    agent_folders.append(potential_agent)
                    
        return agent_folders
        
    def generate_report(self):
        """Generate comprehensive compliance report"""
        agent_folders = self.scan_all_agents()
        
        print(f"🔍 Quantum Biology Format Verification Report")
        print(f"=" * 50)
        print(f"Total agent folders found: {len(agent_folders)}")
        print()
        
        all_results = []
        compliant_count = 0
        
        for folder in agent_folders:
            results = self.verify_agent_folder(folder)
            all_results.append(results)
            
            # Calculate compliance score
            compliance_score = 0
            total_checks = 0
            
            # Timestamp format (1 point)
            total_checks += 1
            if results['timestamp_format']:
                compliance_score += 1
                
            # Required files (4 points)
            for file_present in results['required_files_present'].values():
                total_checks += 1
                if file_present:
                    compliance_score += 1
                    
            # Required dirs (2 points)
            for dir_present in results['required_dirs_present'].values():
                total_checks += 1
                if dir_present:
                    compliance_score += 1
                    
            # Findings.json valid and complete (2 points)
            total_checks += 2
            if results['findings_json_valid']:
                compliance_score += 1
            if results['findings_json_complete']:
                compliance_score += 1
                
            compliance_percentage = (compliance_score / total_checks) * 100
            
            if compliance_percentage >= 80:
                compliant_count += 1
                status = "✅ COMPLIANT"
            elif compliance_percentage >= 60:
                status = "⚠️  MOSTLY COMPLIANT"
            else:
                status = "❌ NON-COMPLIANT"
                
            print(f"{status} ({compliance_percentage:.0f}%): {folder.name}")
            
            if compliance_percentage < 100:
                # Show issues
                if not results['timestamp_format']:
                    print(f"  - Invalid timestamp format")
                for file_name, present in results['required_files_present'].items():
                    if not present:
                        print(f"  - Missing: {file_name}")
                for dir_name, present in results['required_dirs_present'].items():
                    if not present:
                        print(f"  - Missing directory: {dir_name}")
                if not results['findings_json_valid']:
                    print(f"  - findings.json invalid")
                if results['findings_json_errors']:
                    for error in results['findings_json_errors']:
                        print(f"  - {error}")
                print()
        
        print(f"\n📊 Summary:")
        print(f"- Compliant agents: {compliant_count}/{len(agent_folders)} ({compliant_count/len(agent_folders)*100:.1f}%)")
        
        # Count by phenomenon
        phenomenon_stats = defaultdict(list)
        for result in all_results:
            # Extract phenomenon from path
            path_parts = Path(result['path']).parts
            if 'integration' in path_parts:
                phenomenon = 'integration'
            else:
                for part in path_parts:
                    if part in self.valid_phenomena:
                        phenomenon = part
                        break
                else:
                    phenomenon = 'unknown'
            phenomenon_stats[phenomenon].append(result)
            
        print(f"\n📈 By Phenomenon:")
        for phenomenon, results in phenomenon_stats.items():
            compliant = sum(1 for r in results if self.calculate_compliance_score(r) >= 80)
            print(f"- {phenomenon}: {compliant}/{len(results)} compliant")
            
    def calculate_compliance_score(self, results):
        """Calculate compliance percentage for a single agent"""
        compliance_score = 0
        total_checks = 0
        
        total_checks += 1
        if results['timestamp_format']:
            compliance_score += 1
            
        for file_present in results['required_files_present'].values():
            total_checks += 1
            if file_present:
                compliance_score += 1
                
        for dir_present in results['required_dirs_present'].values():
            total_checks += 1
            if dir_present:
                compliance_score += 1
                
        total_checks += 2
        if results['findings_json_valid']:
            compliance_score += 1
        if results['findings_json_complete']:
            compliance_score += 1
            
        return (compliance_score / total_checks) * 100

if __name__ == "__main__":
    verifier = FormatVerifier()
    verifier.generate_report()
