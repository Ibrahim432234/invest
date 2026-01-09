@echo off
echo Updating from Git...
git pull

echo.
echo Cleaning up old Docker containers...
docker-compose down -v
docker system prune -f

echo.
echo Building and starting containers...
docker-compose up --build -d

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak > nul

echo.
echo ====================================
echo Services are starting!
echo ====================================
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo ====================================
echo.
echo Press Ctrl+C to stop viewing logs
echo.

docker-compose logs -f
