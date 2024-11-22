import json

# Paths to the input JSON file and output NGINX config file
json_file_path = "backend_ips.json"
nginx_conf_path = "ansible/roles/load_balancer/templates/nginx.conf.j2"

# Load the backend IPs from the JSON file
with open(json_file_path, "r") as json_file:
    backend_ips = json.load(json_file)

# Generate the upstream backend block dynamically
upstream_backend = "\n".join([f"        server {ip}:80;" for ip in backend_ips])

# Template for the NGINX configuration file
nginx_template = f"""
events {{
    worker_connections 1024;  # Number of simultaneous connections per worker
}}

http {{
    upstream backend {{
{upstream_backend}
    }}

    server {{
        listen 80;

        location / {{
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}
    }}
}}
"""

# Write the generated NGINX configuration to the output file
with open(nginx_conf_path, "w") as nginx_file:
    nginx_file.write(nginx_template)

print(f"NGINX configuration has been generated and saved to {nginx_conf_path}.")