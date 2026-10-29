@echo off
title Bullet Matrix Server Launcher
cd /d %~dp0

echo ===================================================
echo  Starting Bullet Matrix Host Server
echo ===================================================

:: 1. AI_agent/extraction_target_project 폴더가 하위에 있는 경우 이동
if exist "AI_agent\extraction_target_project" (
    cd AI_agent\extraction_target_project
) else if exist "extraction_target_project" (
    cd extraction_target_project
) else if exist "..\server.js" (
    cd ..
)

echo [Current Directory] %cd%

:: 2. 필수 Node.js 모듈(express, ws) 존재 여부 체크 및 설치
if not exist "node_modules" (
    echo 📦 [Auto Setup] node_modules를 찾을 수 없어 모듈을 설치합니다...
    call npm install express ws
)

:: 3. server.js 실행
if exist "server.js" (
    echo 🚀 [Server Start] server.js를 실행합니다...
    node server.js
) else (
    echo ❌ [Error] 현재 경로에서 server.js 파일을 찾을 수 없습니다.
    echo 현재 위치: %cd%
    pause
)