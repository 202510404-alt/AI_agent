@echo off
title Bullet Matrix Multi-Server
cd /d %~dp0
echo Starting Bullet Matrix Host Server...

:: AI_agent/extraction_target_project 경로 내 server.js 자동 찾기 후 실행
if exist "server.js" (
    node server.js
) else if exist "extraction_target_project\server.js" (
    node extraction_target_project\server.js
) else if exist "AI_agent\extraction_target_project\server.js" (
    node AI_agent\extraction_target_project\server.js
) else (
    echo [Error] server.js 파일을 찾을 수 없습니다.
    pause
)