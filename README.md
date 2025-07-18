# HEAP-AInalyse
AI powered contract analysis project for HEAP

To host locally:
Run start-all.bat or start-all.sh in root folder of HEAP-AInalyse with docker open in background. This allows all services to start running.
To stop, run stop-all.bat or stop-all.sh to stop the containers

For .sh, use "chmod +x start-all.sh" or "chmod +x stop-all.sh"

To host on cloud:
Distribute Application Components:
Deploy the frontend application to the designated frontend EC2 instances.
Deploy the backend application to the designated backend EC2 instances.

Configure Reverse Proxy:
On frontend EC2 instance, install and configure Nginx to serve the frontend application and act as a reverse proxy.
The Nginx server should forward API requests to the backend service using the private IP address of the backend EC2 instances.

Start Backend Services:
On backend EC2 instance, navigate to the backend project directory and execute:
docker compose up --build -d

Ensure Docker and Docker Compose are properly installed and configured on the backend instances.