#!/bin/bash

echo "Backend"
cd backend
docker-compose up --build -d
echo "Backend-ed"

echo "Frontend"
cd ../Frontend
npm install
npm run dev
cd ..
echo "Frontend-ed"
