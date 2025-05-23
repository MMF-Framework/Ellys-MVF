#!/bin/bash
# scripts/quickstart.sh

echo "🚀 Ellys-MVF 빠른 시작 스크립트"
echo "================================"

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "📁 프로젝트 루트: $PROJECT_ROOT"

cd "$PROJECT_ROOT"

echo ""
echo "🔍 시스템 요구사항 확인 중..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3가 설치되어 있지 않습니다."
    echo "   Python 3.8 이상을 설치해주세요."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION 발견"

echo ""
echo "📂 필수 디렉토리 생성 중..."

mkdir -p projects
mkdir -p archive
mkdir -p logs

[ ! -f "projects/.gitkeep" ] && touch projects/.gitkeep
[ ! -f "archive/.gitkeep" ] && touch archive/.gitkeep
[ ! -f "logs/.gitkeep" ] && touch logs/.gitkeep

mkdir -p mvf/{core,modules,utils,cli}
[ ! -f "mvf/__init__.py" ] && touch mvf/__init__.py
[ ! -f "mvf/core/__init__.py" ] && touch mvf/core/__init__.py
[ ! -f "mvf/modules/__init__.py" ] && touch mvf/modules/__init__.py
[ ! -f "mvf/utils/__init__.py" ] && touch mvf/utils/__init__.py
[ ! -f "mvf/cli/__init__.py" ] && touch mvf/cli/__init__.py

echo "✅ 디렉토리 생성 완료"

echo ""
echo "⚙️  초기 설정 확인 중..."

if [ ! -f "system/manifest.yaml" ]; then
    echo "❌ system/manifest.yaml 파일이 없습니다."
    exit 1
fi

if [ ! -f "system/mmf_config.yaml" ]; then
    echo "❌ system/mmf_config.yaml 파일이 없습니다."
    exit 1
fi

echo "✅ 설정 파일 확인 완료"

echo ""
echo "📝 샘플 프로젝트 생성 중..."

SAMPLE_PROJECT_DIR="projects/sample_project_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$SAMPLE_PROJECT_DIR"

cat > "$SAMPLE_PROJECT_DIR/project_info.yaml" << 'EOF'
project:
  metadata:
    name: "샘플 프로젝트"
    description: "Ellys-MVF 테스트용 샘플 프로젝트"
    created_date: "2024-05-23"
    created_by: "quickstart"
    status: "planning"
    priority: "medium"
    
  classification:
    domain: "education"
    complexity: "simple"
    duration_estimate: "1 week"
    team_size: 1
    
  objectives:
    primary_goal: "Ellys-MVF 프레임워크 학습 및 테스트"
    success_criteria: 
      - "8단계 프로세스 완주"
      - "PNE 매트릭스 작성"
      - "자동 보고서 생성"
    key_metrics: 
      - "완료된 단계 수"
      - "획득한 XP"
    deadline: "2024-05-30"
EOF

if [ -f "templates/persona/pne_matrix.md" ]; then
    cp "templates/persona/pne_matrix.md" "$SAMPLE_PROJECT_DIR/"
    echo "✅ PNE 매트릭스 템플릿 복사 완료"
else
    echo "⚠️  PNE 매트릭스 템플릿을 찾을 수 없습니다."
fi

echo "✅ 샘플 프로젝트 생성 완료: $SAMPLE_PROJECT_DIR"

echo ""
echo "🎉 설정 완료!"
echo ""
echo "다음 단계:"
echo "1. 샘플 프로젝트 확인: $SAMPLE_PROJECT_DIR"
echo "2. PNE 매트릭스 작성: $SAMPLE_PROJECT_DIR/pne_matrix.md"
echo "3. 첫 번째 프로젝트 시작하기"
echo ""
echo "테스트:"
echo "  python3 -c \"import sys; sys.path.append('.'); from mvf import *; print('MVF 패키지 로드 성공!')\""
echo ""
echo "도움말:"
echo "  - 문서: docs/quickstart/"
echo "  - 설정 파일: system/"
echo "  - 템플릿: templates/"
echo ""
echo "🚀 Ellys-MVF와 함께 시작하세요!"