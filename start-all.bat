@echo off
echo Backend
cd backend
docker compose up --build -d
echo Backend-ed

echo Frontend
cd ..\Frontend
call npm install
call npm run dev
cd ..
echo Frontend-ed

