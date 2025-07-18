@echo off
echo Stopping backend
cd backend
docker compose down
cd ..
echo Stopped backend

