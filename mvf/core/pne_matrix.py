# mvf/core/pne_matrix.py

from typing import Dict, List, Optional, Tuple
import yaml
from pathlib import Path
from datetime import datetime

class PNEMatrix:
    def __init__(self):
        self.matrix = {
            'positive': {'qualitative': [], 'quantitative': [], 'contextual': []},
            'negative': {'qualitative': [], 'quantitative': [], 'contextual': []},
            'external': {'qualitative': [], 'quantitative': [], 'contextual': []}
        }
        self.gaps = []
        self.insights = []
    
    def add_item(self, pne_type: str, data_type: str, content: str) -> bool:
        """PNE 매트릭스에 항목 추가"""
        if pne_type not in self.matrix:
            return False
        if data_type not in self.matrix[pne_type]:
            return False
        
        self.matrix[pne_type][data_type].append({
            'content': content,
            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return True
    
    def add_positive(self, data_type: str, content: str) -> bool:
        """긍정적 요인 추가"""
        return self.add_item('positive', data_type, content)
    
    def add_negative(self, data_type: str, content: str) -> bool:
        """부정적 요인 추가"""
        return self.add_item('negative', data_type, content)
    
    def add_external(self, data_type: str, content: str) -> bool:
        """외부 요인 추가"""
        return self.add_item('external', data_type, content)
    
    def identify_gaps(self) -> List[str]:
        """빈 셀 및 Gap 식별"""
        gaps = []
        
        for pne_type, categories in self.matrix.items():
            for data_type, items in categories.items():
                if not items:
                    gaps.append(f"{pne_type.upper()}-{data_type.capitalize()} 셀이 비어있음")
        
        total_counts = {}
        for pne_type, categories in self.matrix.items():
            total_counts[pne_type] = sum(len(items) for items in categories.values())
        
        if total_counts.values():
            max_count = max(total_counts.values())
            min_count = min(total_counts.values())
            
            if max_count - min_count > 2:
                gaps.append(f"분석 불균형: 가장 많은 항목({max_count})과 적은 항목({min_count}) 차이가 큼")
        
        self.gaps = gaps
        return gaps
    
    def get_completion_rate(self) -> float:
        """완성도 계산 (9셀 중 몇 셀이 채워졌는지)"""
        filled_cells = 0
        total_cells = 9
        
        for pne_type, categories in self.matrix.items():
            for data_type, items in categories.items():
                if items:
                    filled_cells += 1
        
        return (filled_cells / total_cells) * 100
    
    def generate_insights(self) -> List[str]:
        """자동 인사이트 생성"""
        insights = []
        completion = self.get_completion_rate()
        
        if completion < 50:
            insights.append("⚠️ 분석이 불충분합니다. 더 많은 요인을 고려해보세요.")
        
        quant_count = sum(len(self.matrix[pne]['quantitative']) for pne in self.matrix)
        total_count = sum(len(items) for pne in self.matrix.values() for items in pne.values())
        
        if total_count > 0 and (quant_count / total_count) < 0.3:
            insights.append("📊 정량적 데이터가 부족합니다. 수치로 뒷받침할 수 있는 근거를 추가하세요.")
        
        external_count = sum(len(items) for items in self.matrix['external'].values())
        if external_count < 2:
            insights.append("🌍 외부 환경 분석이 부족합니다. 시장, 경쟁, 규제 등을 고려하세요.")
        
        self.insights = insights
        return insights
    
    def export_to_markdown(self, file_path: Optional[Path] = None) -> str:
        """마크다운 형식으로 내보내기"""
        markdown = "# PNE 매트릭스 분석 결과\n\n"
        markdown += f"**완성도:** {self.get_completion_rate():.1f}%\n\n"
        
        markdown += "## 📊 매트릭스\n\n"
        markdown += "| 구분 | Qualitative | Quantitative | Contextual |\n"
        markdown += "|------|-------------|--------------|------------|\n"
        
        for pne_type in ['positive', 'negative', 'external']:
            row = f"| **{pne_type.upper()}** |"
            for data_type in ['qualitative', 'quantitative', 'contextual']:
                items = self.matrix[pne_type][data_type]
                cell_content = "<br>".join([item['content'] for item in items]) if items else "-"
                row += f" {cell_content} |"
            markdown += row + "\n"
        
        if self.gaps:
            markdown += "\n## 🔍 식별된 Gap\n\n"
            for gap in self.gaps:
                markdown += f"- {gap}\n"
        
        if self.insights:
            markdown += "\n## 💡 인사이트\n\n"
            for insight in self.insights:
                markdown += f"- {insight}\n"
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
        
        return markdown
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'matrix': self.matrix,
            'gaps': self.gaps,
            'insights': self.insights,
            'completion_rate': self.get_completion_rate()
        }
    
    def save_to_yaml(self, file_path: Path):
        """YAML 파일로 저장"""
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, allow_unicode=True)
    
    def load_from_yaml(self, file_path: Path):
        """YAML 파일에서 로드"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            self.matrix = data.get('matrix', self.matrix)
            self.gaps = data.get('gaps', [])
            self.insights = data.get('insights', [])