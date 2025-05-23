# mvf/modules/hud.py

from typing import Dict, List, Optional
from datetime import datetime
import json

class HUD:
    def __init__(self):
        self.alerts = []
        self.notifications = []
        self.status_data = {}
        self.last_update = datetime.now()
    
    def add_alert(self, level: str, message: str, source: str = "system"):
        """알림 추가"""
        alert = {
            "level": level,  # info, warning, error, success
            "message": message,
            "source": source,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.alerts.append(alert)
        
        # 최근 10개만 유지
        if len(self.alerts) > 10:
            self.alerts = self.alerts[-10:]
        
        print(f"🔔 [{level.upper()}] {message}")
    
    def update_status(self, key: str, value, description: str = ""):
        """상태 정보 업데이트"""
        self.status_data[key] = {
            "value": value,
            "description": description,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.last_update = datetime.now()
    
    def display_dashboard(self, project=None):
        """대시보드 표시"""
        print("\n" + "="*60)
        print("🎮 Ellys-MVF HUD Dashboard")
        print("="*60)
        
        if project:
            progress = project.get_progress()
            print(f"📋 프로젝트: {progress['project_name']}")
            print(f"📊 진행률: {progress['progress_percentage']:.1f}% ({progress['completed_stages']}/{progress['total_stages']} 단계)")
            print(f"🏆 레벨: {progress['current_level']} (XP: {progress['current_xp']})")
            print(f"📈 매트릭스 완성도: {progress['matrix_completion']:.1f}%")
            print(f"🔄 상태: {progress['status']}")
        
        if self.status_data:
            print("\n📊 시스템 상태:")
            for key, data in self.status_data.items():
                print(f"  • {key}: {data['value']} ({data['description']})")
        
        if self.alerts:
            print("\n🔔 최근 알림:")
            for alert in self.alerts[-5:]:  # 최근 5개만 표시
                icon = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "success": "✅"}.get(alert['level'], "📝")
                print(f"  {icon} {alert['message']} [{alert['timestamp']}]")
        
        print(f"\n🕐 마지막 업데이트: {self.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
    
    def get_dashboard_data(self) -> Dict:
        """대시보드 데이터 반환 (API용)"""
        return {
            "alerts": self.alerts,
            "status_data": self.status_data,
            "last_update": self.last_update.isoformat(),
            "alert_count": len(self.alerts),
            "status_count": len(self.status_data)
        }
    
    def clear_alerts(self):
        """알림 목록 초기화"""
        self.alerts = []
        print("🧹 알림 목록이 초기화되었습니다.")
    
    def export_log(self, file_path: str):
        """로그 내보내기"""
        log_data = {
            "export_date": datetime.now().isoformat(),
            "alerts": self.alerts,
            "status_data": self.status_data
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        print(f"📁 HUD 로그가 저장되었습니다: {file_path}")

# 글로벌 HUD 인스턴스
hud_instance = HUD()

def get_hud() -> HUD:
    """글로벌 HUD 인스턴스 반환"""
    return hud_instance