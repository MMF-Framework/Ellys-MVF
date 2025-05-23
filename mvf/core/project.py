# mvf/core/project.py

import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from .pne_matrix import PNEMatrix

class Project:
    def __init__(self, name: str, project_dir: Optional[Path] = None):
        self.name = name
        self.created_date = datetime.now()
        self.status = "planning"
        self.project_dir = project_dir or Path(f"projects/{name.replace(' ', '_').lower()}")
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata = {
            "name": name,
            "created_date": self.created_date.strftime("%Y-%m-%d"),
            "status": self.status,
            "priority": "medium"
        }
        
        self.pne_matrix = PNEMatrix()
        self.stages = {}
        self.xp = 0
        self.level = 1
        
        self._load_or_create_project_file()
    
    def _load_or_create_project_file(self):
        """프로젝트 파일 로드 또는 생성"""
        project_file = self.project_dir / "project_info.yaml"
        
        if project_file.exists():
            with open(project_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data and 'project' in data:
                    self.metadata.update(data.get('project', {}).get('metadata', {}))
                    self.xp = data.get('project', {}).get('xp', 0)
                    self.level = data.get('project', {}).get('level', 1)
                    self.stages = data.get('project', {}).get('stages', {})
        else:
            self._save_project_file()
    
    def _save_project_file(self):
        """프로젝트 파일 저장"""
        project_file = self.project_dir / "project_info.yaml"
        
        project_data = {
            "project": {
                "metadata": self.metadata,
                "stages": self.stages,
                "xp": self.xp,
                "level": self.level
            }
        }
        
        with open(project_file, 'w', encoding='utf-8') as f:
            yaml.dump(project_data, f, default_flow_style=False, allow_unicode=True)
    
    def set_matrix(self, matrix: PNEMatrix):
        """PNE 매트릭스 설정"""
        self.pne_matrix = matrix
        matrix_file = self.project_dir / "pne_matrix.yaml"
        matrix.save_to_yaml(matrix_file)
        print(f"PNE 매트릭스가 저장되었습니다: {matrix_file}")
    
    def add_xp(self, points: int, reason: str = ""):
        """XP 추가"""
        self.xp += points
        new_level = (self.xp // 100) + 1
        if new_level > self.level:
            self.level = new_level
            print(f"🎉 레벨업! 새로운 레벨: {self.level}")
        
        self._save_project_file()
        return self.xp, self.level
    
    def complete_stage(self, stage_name: str):
        """단계 완료"""
        self.stages[stage_name] = {
            "completed": True,
            "completed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        xp_gained = 20
        self.add_xp(xp_gained, f"Stage {stage_name} completed")
        
        self._save_project_file()
        print(f"✅ {stage_name} 단계 완료! (+{xp_gained} XP)")
    
    def update_status(self, status: str):
        """상태 업데이트"""
        self.status = status
        self.metadata["status"] = status
        self._save_project_file()
        print(f"📋 프로젝트 상태가 '{status}'로 변경되었습니다.")
    
    def get_progress(self) -> Dict:
        """진행 상황 반환"""
        total_stages = 8
        completed_stages = len([s for s in self.stages.values() if s.get('completed', False)])
        progress_percentage = (completed_stages / total_stages) * 100
        
        return {
            "project_name": self.name,
            "status": self.status,
            "completed_stages": completed_stages,
            "total_stages": total_stages,
            "progress_percentage": progress_percentage,
            "current_xp": self.xp,
            "current_level": self.level,
            "matrix_completion": self.pne_matrix.get_completion_rate()
        }
    
    def generate_report(self) -> str:
        """보고서 생성"""
        template_path = Path("templates/report/report_template.md")
        if not template_path.exists():
            return "❌ 보고서 템플릿을 찾을 수 없습니다."
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            
            progress = self.get_progress()
            
            report_content = template.format(
                project_name=self.name,
                generated_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                start_date=self.metadata.get("created_date", ""),
                end_date="진행중",
                author=self.metadata.get("created_by", "Unknown"),
                status=self.status,
                total_xp=self.xp,
                current_level=self.level,
                **{f"stage{i}_progress": "100%" if f"stage{i}" in self.stages else "0%" for i in range(8)}
            )
            
            report_file = self.project_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"📄 보고서 생성 완료: {report_file}")
            return str(report_file)
            
        except Exception as e:
            return f"❌ 보고서 생성 중 오류: {str(e)}"
    
    def __str__(self):
        return f"Project(name='{self.name}', status='{self.status}', level={self.level}, xp={self.xp})"