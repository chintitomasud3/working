worker_processes 1;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Frontend (React / Vue / etc.)
    upstream frontend_server {
        server 192.168.20.10:5000;
    }

    # Backend (Node / FastAPI)
    upstream backend_server {
        server 192.168.20.20:9000;
    }

    server {
        listen 80;
        server_name _;

        # -------------------------
        # Frontend route
        # -------------------------
        location / {
            proxy_pass http://frontend_server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # -------------------------
        # Backend API route
        # -------------------------
        location /api/ {
            proxy_pass http://backend_server/;
            
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            # Important for POST / large payloads
            client_max_body_size 20M;
        }
    }
}
