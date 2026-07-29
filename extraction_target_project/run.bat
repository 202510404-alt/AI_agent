@echo off
setlocal

set MODE=%1

if "%MODE%"=="" set MODE=all

if "%MODE%"=="all" (
    echo [RUN] Running client and server simultaneously...
    npm run dev:all
    goto end
)

if "%MODE%"=="server" (
    echo [RUN] Running server only...
    npm run dev
    goto end
)

if "%MODE%"=="client" (
    echo [RUN] Running client only...
    npm run dev:client
    goto end
)

if "%MODE%"=="install" (
    echo [RUN] Installing all dependencies...
    npm run install:all
    goto end
)

echo [ERROR] Unknown mode: %MODE%
echo Usage: .\run.bat [all ^| server ^| client ^| install]

:end
endlocal