@echo off
chcp 65001 > nul
title Realtime Whiteboard Server
color 0A

echo ========================================================
echo   실시간 협업 화이트보드 시스템 자동 빌드 및 실행
echo ========================================================
echo.

echo [1/3] 루트 백엔드 패키지 설치 확인 중...
call npm install

echo.
echo [2/3] 리액트 클라이언트 빌드 중... (잠시만 기다려주세요)
call npm run build

echo.
echo [3/3] 통합 서버를 시작합니다...
echo 아래 콘솔에 표시되는 '다른 사람 접속 주소'를 공유하세요!
echo ========================================================
echo.

npm start
pause