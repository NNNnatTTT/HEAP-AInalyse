#!/bin/bash

# Vue Frontend Rebuild and Deploy Script
# Usage: ./rebuild_deploy_vue.sh

echo "Starting Vue frontend rebuild and deployment..."

# Navigate to your Vue project directory
cd /home/frontend

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "Error: package.json not found. Make sure you're in the correct Vue project directory."
    exit 1
fi

# Install/update dependencies (optional, uncomment if needed)
# echo "Installing dependencies..."
# npm install

# Build the Vue project for production
echo "Building Vue project for production..."
npm run build

# Check if build was successful
if [ $? -ne 0 ]; then
    echo "Error: Build failed. Please check your code for errors."
    exit 1
fi

# Check if dist directory exists
if [ ! -d "dist" ]; then
    echo "Error: dist directory not found. Build may have failed."
    exit 1
fi

# Backup current deployment (optional)
echo "Creating backup of current deployment..."
if [ -d "/var/www/vue-frontend" ]; then
    cp -r /var/www/vue-frontend /var/www/vue-frontend.backup.$(date +%Y%m%d_%H%M%S)
fi

# Copy the built files to the Nginx directory
echo "Deploying new build to Nginx directory..."
cp -r dist/* /var/www/vue-frontend/

# Set proper permissions
echo "Setting proper permissions..."
chown -R nginx:nginx /var/www/vue-frontend
chmod -R 755 /var/www/vue-frontend

# Test Nginx configuration
echo "Testing Nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    # Reload Nginx to apply changes
    echo "Reloading Nginx..."
    systemctl reload nginx
    
    # Verify Nginx is running
    if systemctl is-active --quiet nginx; then
        echo "✅ Vue frontend rebuilt and deployed successfully!"
        echo "🌐 Your application is now live at: http://your-server-ip"
    else
        echo "❌ Error: Nginx failed to start. Check configuration."
        exit 1
    fi
else
    echo "❌ Error: Nginx configuration test failed. Deployment aborted."
    exit 1
fi

# Optional: Clear old backups (keep only last 5)
echo "Cleaning up old backups..."
ls -t /var/www/vue-frontend.backup.* 2>/dev/null | tail -n +6 | xargs -r rm -rf

echo "Deployment completed successfully!"
