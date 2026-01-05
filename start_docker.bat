@echo off
echo Building Docker image...
docker build -t sign-translator-app .
if %errorlevel% neq 0 (
    echo Docker build failed. Please ensure Docker Desktop is running.
    pause
    exit /b %errorlevel%
)

echo Starting application...
echo Access the app at http://localhost:8501
docker run -p 8501:8501 sign-translator-app
pause
