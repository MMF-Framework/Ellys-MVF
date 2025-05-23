# mvf/cli/main.py

import click
from pathlib import Path
from ..core.project import Project
from ..core.pne_matrix import PNEMatrix
from ..modules.hud import get_hud
from ..modules.xp_manager import get_xp_manager

@click.group()
def cli():
    """Ellys-MVF CLI - 30분 내 실전 적용 가능한 전략 프레임워크"""
    pass

@cli.command()
@click.argument('name')
def create_project(name):
    """새 프로젝트 생성"""
    try:
        project = Project(name)
        hud = get_hud()
        hud.add_alert('success', f'프로젝트 "{name}"이 생성되었습니다')
        
        click.echo(f"✅ 프로젝트 '{name}'이 생성되었습니다!")
        click.echo(f"📁 경로: {project.project_dir}")
        click.echo(f"🎮 상태: {project.status}")
        
        # 첫 XP 지급
        project.add_xp(25, '첫 프로젝트 생성')
        click.echo(f"🎉 첫 프로젝트 생성 보너스: +25 XP!")
        
    except Exception as e:
        click.echo(f"❌ 프로젝트 생성 실패: {str(e)}")

@cli.command()
@click.argument('project_name')
def dashboard(project_name):
    """프로젝트 대시보드 표시"""
    try:
        project_dir = Path(f"projects/{project_name.replace(' ', '_').lower()}")
        if not project_dir.exists():
            click.echo(f"❌ 프로젝트 '{project_name}'을 찾을 수 없습니다.")
            return
        
        project = Project(project_name, project_dir)
        hud = get_hud()
        hud.display_dashboard(project)
        
    except Exception as e:
        click.echo(f"❌ 대시보드 표시 실패: {str(e)}")

@cli.command()
def list_projects():
    """프로젝트 목록 표시"""
    projects_dir = Path("projects")
    if not projects_dir.exists():
        click.echo("📂 프로젝트 폴더가 없습니다.")
        return
    
    projects = [d for d in projects_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    if not projects:
        click.echo("📂 생성된 프로젝트가 없습니다.")
        click.echo("💡 'python3 scripts/ellys-mvf.py create-project <이름>' 명령어로 프로젝트를 생성하세요.")
        return
    
    click.echo("📋 프로젝트 목록:")
    for project_dir in projects:
        try:
            project = Project(project_dir.name, project_dir)
            progress = project.get_progress()
            click.echo(f"  • {project.name} - {progress['progress_percentage']:.1f}% - 레벨 {progress['current_level']} - XP: {progress['current_xp']}")
        except:
            click.echo(f"  • {project_dir.name} - (상태 불명)")

@cli.command()
@click.argument('project_name')
@click.argument('stage_name')
def complete_stage(project_name, stage_name):
    """프로젝트 단계 완료"""
    try:
        project_dir = Path(f"projects/{project_name.replace(' ', '_').lower()}")
        if not project_dir.exists():
            click.echo(f"❌ 프로젝트 '{project_name}'을 찾을 수 없습니다.")
            return
        
        project = Project(project_name, project_dir)
        project.complete_stage(stage_name)
        
        click.echo(f"✅ {stage_name} 단계가 완료되었습니다!")
        
    except Exception as e:
        click.echo(f"❌ 단계 완료 실패: {str(e)}")

@cli.command()
def version():
    """버전 정보 표시"""
    click.echo("Ellys-MVF v1.0.0")
    click.echo("MMF Framework - Minimum Viable Framework")
    click.echo("30분 내 실전 적용 가능한 전략 프레임워크")

if __name__ == '__main__':
    cli()