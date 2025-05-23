# mvf/modules/xp_manager.py

from typing import Dict, List, Optional
from datetime import datetime
import json

class XPManager:
    def __init__(self):
        self.xp_history = []
        self.achievements = []
        self.level_thresholds = {
            1: 0, 2: 100, 3: 250, 4: 450, 5: 700,
            6: 1000, 7: 1350, 8: 1750, 9: 2200, 10: 2700
        }
        self.xp_rewards = {
            "stage_completion": 20,
            "matrix_cell_filled": 5,
            "insight_generated": 15,
            "report_generated": 25,
            "gap_identified": 10,
            "project_completed": 100
        }
    
    def award_xp(self, amount: int, reason: str, recipient: str = "user") -> Dict:
        """XP 지급"""
        xp_record = {
            "amount": amount,
            "reason": reason,
            "recipient": recipient,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.xp_history.append(xp_record)
        
        # 최근 100개 기록만 유지
        if len(self.xp_history) > 100:
            self.xp_history = self.xp_history[-100:]
        
        return xp_record
    
    def calculate_level(self, total_xp: int) -> int:
        """총 XP를 바탕으로 레벨 계산"""
        for level in reversed(range(1, 11)):
            if total_xp >= self.level_thresholds[level]:
                return level
        return 1
    
    def get_xp_to_next_level(self, current_xp: int) -> Optional[int]:
        """다음 레벨까지 필요한 XP"""
        current_level = self.calculate_level(current_xp)
        if current_level >= 10:
            return None  # 최대 레벨
        
        next_level_threshold = self.level_thresholds[current_level + 1]
        return next_level_threshold - current_xp
    
    def check_achievements(self, project) -> List[str]:
        """업적 확인"""
        new_achievements = []
        
        # 첫 프로젝트 생성
        if not any(a['type'] == 'first_project' for a in self.achievements):
            new_achievements.append({
                'type': 'first_project',
                'title': '🌟 첫 걸음',
                'description': '첫 번째 프로젝트를 생성했습니다!',
                'earned_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # PNE 매트릭스 마스터
        if project.pne_matrix.get_completion_rate() >= 100:
            if not any(a['type'] == 'matrix_master' for a in self.achievements):
                new_achievements.append({
                    'type': 'matrix_master',
                    'title': '🧩 매트릭스 마스터',
                    'description': 'PNE 매트릭스를 완전히 채웠습니다!',
                    'earned_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # 레벨업 관련 업적
        current_level = self.calculate_level(project.xp)
        level_achievements = {
            5: ('🏆 베테랑', '레벨 5에 도달했습니다!'),
            10: ('👑 마스터', '최고 레벨에 도달했습니다!')
        }
        
        if current_level in level_achievements:
            achievement_type = f'level_{current_level}'
            if not any(a['type'] == achievement_type for a in self.achievements):
                title, description = level_achievements[current_level]
                new_achievements.append({
                    'type': achievement_type,
                    'title': title,
                    'description': description,
                    'earned_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # 새 업적 추가
        self.achievements.extend(new_achievements)
        
        return [a['title'] + ': ' + a['description'] for a in new_achievements]
    
    def get_xp_summary(self, project) -> Dict:
        """XP 요약 정보"""
        current_level = self.calculate_level(project.xp)
        xp_to_next = self.get_xp_to_next_level(project.xp)
        
        return {
            "total_xp": project.xp,
            "current_level": current_level,
            "xp_to_next_level": xp_to_next,
            "total_achievements": len(self.achievements),
            "recent_xp_gains": self.xp_history[-5:] if self.xp_history else [],
            "level_progress": f"{current_level}/10"
        }
    
    def display_xp_status(self, project):
        """XP 상태 표시"""
        summary = self.get_xp_summary(project)
        
        print("\n" + "="*50)
        print("🏆 XP & 성장 현황")
        print("="*50)
        print(f"총 XP: {summary['total_xp']}")
        print(f"현재 레벨: {summary['current_level']}/10")
        
        if summary['xp_to_next_level']:
            print(f"다음 레벨까지: {summary['xp_to_next_level']} XP")
        else:
            print("🎉 최고 레벨 달성!")
        
        print(f"획득 업적: {summary['total_achievements']}개")
        
        if summary['recent_xp_gains']:
            print("\n📈 최근 XP 획득:")
            for gain in summary['recent_xp_gains']:
                print(f"  • +{gain['amount']} XP - {gain['reason']} [{gain['timestamp']}]")
        
        if self.achievements:
            print("\n🏅 업적:")
            for achievement in self.achievements[-3:]:  # 최근 3개만 표시
                print(f"  • {achievement['title']}: {achievement['description']}")
        
        print("="*50)

# 글로벌 XP Manager 인스턴스
xp_manager_instance = XPManager()

def get_xp_manager() -> XPManager:
    """글로벌 XP Manager 인스턴스 반환"""
    return xp_manager_instance