# mvf/__init__.py

__version__ = "1.0.0"
__author__ = "MMF-Framework"
__email__ = "contact@mmf-framework.org"

try:
    from .core.project import Project
    from .core.pne_matrix import PNEMatrix
    from .modules.hud import HUD
    from .modules.xp_manager import XPManager
    
    __all__ = [
        "Project",
        "PNEMatrix", 
        "HUD",
        "XPManager"
    ]
except ImportError:
    # 모듈이 아직 구현되지 않은 경우
    __all__ = []
    
print("📦 Ellys-MVF 패키지 로드됨")