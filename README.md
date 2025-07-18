# HEAP-AInalyse
AI powered contract analysis project for HEAP

To host locally:
Run start-all.bat or start-all.sh in root folder of HEAP-AInalyse with docker open in background. This allows all services to start running.
To stop, run stop-all.bat or stop-all.sh to stop the containers

For .sh, use "chmod +x start-all.sh" or "chmod +x stop-all.sh"

To host on cloud:
Copy frontend into the front end ECs, backend to the backend ECs
Set up a nginx server in the frontend ECs to act as a reverse proxy to the backend private ip
For backend just docker compose up 