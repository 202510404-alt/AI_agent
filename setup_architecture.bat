import os

def create_directory_structure():
    bat_content = """@echo off
echo ==========================================================================
echo [CoreDefense Architecture Setup] extraction_target_project 내 신규 트리 세팅 시작
echo ==========================================================================

rem 1. 루트 경로 변수 지정 및 기존 레거시 구조 제거
set ROOT_DIR=extraction_target_project
if exist %ROOT_DIR%\\src\\main\\java\\com\\desertcore rmdir /s /q %ROOT_DIR%\\src\\main\\java\\com\\desertcore
if exist %ROOT_DIR%\\src\\main\\resources\\editor_objects.json del /f /q %ROOT_DIR%\\src\\main\\resources\\editor_objects.json

rem 2. 리소스 디렉터리 구조 신설 (4장 개정안 반영)
mkdir %ROOT_DIR%\\src\\main\\resources\\config\\waves
mkdir %ROOT_DIR%\\src\\main\\resources\\config\\weapons
mkdir %ROOT_DIR%\\src\\main\\resources\\config\\player_classes
mkdir %ROOT_DIR%\\src\\main\\resources\\config\\npc
mkdir %ROOT_DIR%\\src\\main\\resources\\config\\mining
mkdir %ROOT_DIR%\\src\\main\\resources\\config\\structures
mkdir %ROOT_DIR%\\src\\main\\resources\\config\\progression
mkdir %ROOT_DIR%\\src\\main\\resources\\lang
mkdir %ROOT_DIR%\\src\\main\\resources\\schematics

rem 3. Java 패키지 디렉터리 구조 신설 (5장 개정안 반영)
set BASE_PATH=%ROOT_DIR%\\src\\main\\java\\com\\yourstudio\\coredefense
mkdir %BASE_PATH%\\bootstrap
mkdir %BASE_PATH%\\api\\event
mkdir %BASE_PATH%\\api\\service
mkdir %BASE_PATH%\\common\\event
mkdir %BASE_PATH%\\common\\registry
mkdir %BASE_PATH%\\common\\config
mkdir %BASE_PATH%\\common\\contract
mkdir %BASE_PATH%\\common\\util
mkdir %BASE_PATH%\\common\\scheduling
mkdir %BASE_PATH%\\common\\perf
mkdir %BASE_PATH%\\common\\result
mkdir %BASE_PATH%\\session\\event
mkdir %BASE_PATH%\\core\\event
mkdir %BASE_PATH%\\wave\\spawn
mkdir %BASE_PATH%\\wave\\condition
mkdir %BASE_PATH%\\wave\\state
mkdir %BASE_PATH%\\wave\\boss
mkdir %BASE_PATH%\\wave\\event
mkdir %BASE_PATH%\\combat\\weapon\\strategy
mkdir %BASE_PATH%\\combat\\weapon\\projectile
mkdir %BASE_PATH%\\combat\\weapon\\ammo
mkdir %BASE_PATH%\\combat\\melee
mkdir %BASE_PATH%\\combat\\damage
mkdir %BASE_PATH%\\combat\\vfx
mkdir %BASE_PATH%\\combat\\event
mkdir %BASE_PATH%\\mob\\ai
mkdir %BASE_PATH%\\mob\\event
mkdir %BASE_PATH%\\npc\\safezone\\event
mkdir %BASE_PATH%\\npc\\trait
mkdir %BASE_PATH%\\npc\\vocation
mkdir %BASE_PATH%\\npc\\recruit
mkdir %BASE_PATH%\\npc\\death
mkdir %BASE_PATH%\\npc\\event
mkdir %BASE_PATH%\\mining\\event
mkdir %BASE_PATH%\\structure\\wall
mkdir %BASE_PATH%\\structure\\turret\\targeting
mkdir %BASE_PATH%\\structure\\turret\\types
mkdir %BASE_PATH%\\structure\\event
mkdir %BASE_PATH%\\drone
mkdir %BASE_PATH%\\playerclass\\specialization
mkdir %BASE_PATH%\\playerclass\\skill
mkdir %BASE_PATH%\\playerclass\\heal
mkdir %BASE_PATH%\\playerclass\\builder\\event
mkdir %BASE_PATH%\\playerclass\\event
mkdir %BASE_PATH%\\progression
mkdir %BASE_PATH%\\persistence\\file
mkdir %BASE_PATH%\\persistence\\sql
mkdir %BASE_PATH%\\gui\\menus
mkdir %BASE_PATH%\\command\\sub

echo [CoreDefense Architecture Setup] 폴더 트리 생성 완료. 스켈레톤 마스터 파일 생성 진행...

rem 4. 리소스 및 설정 파일 더미 생성
echo # Core Configuration > %ROOT_DIR%\\src\\main\\resources\\config\\core.yml
echo # Visual Stages > %ROOT_DIR%\\src\\main\\resources\\config\\core_visual_stages.yml
echo # Wave Definitions > %ROOT_DIR%\\src\\main\\resources\\config\\waves\\wave_definitions.yml
echo # Boss Waves > %ROOT_DIR%\\src\\main\\resources\\config\\waves\\boss_waves.yml
echo # Player Classes > %ROOT_DIR%\\src\\main\\resources\\config\\player_classes\\classes.yml
echo # Specializations > %ROOT_DIR%\\src\\main\\resources\\config\\player_classes\\specializations.yml
echo # NPC Job Promotions > %ROOT_DIR%\\src\\main\\resources\\config\\npc\\npc_job_promotions.yml
echo # Resonance Thresholds > %ROOT_DIR%\\src\\main\\resources\\config\\npc\\resonance_thresholds.yml
echo # Editor Objects Specs > %ROOT_DIR%\\src\\main\\resources\\editor_objects.json

rem 5. 핵심 스켈레톤 소스 생성
echo package com.yourstudio.coredefense; > %BASE_PATH%\\CoreDefensePlugin.java
echo public class CoreDefensePlugin extends org.bukkit.plugin.java.JavaPlugin {} >> %BASE_PATH%\\CoreDefensePlugin.java

echo package com.yourstudio.coredefense.bootstrap; > %BASE_PATH%\\bootstrap\\ModuleInitializer.java
echo public class ModuleInitializer { public static boolean DEBUG = false; } >> %BASE_PATH%\\bootstrap\\ModuleInitializer.java

echo ==========================================================================
echo [CoreDefense Architecture Setup] 모든 파일 구조 초기화 및 매핑 성공.
echo ==========================================================================
"""
    with open("setup_architecture.bat", "w", encoding="cp949") as f:
        f.write(bat_content)

create_directory_structure()