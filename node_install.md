sudo apt install -y nodejs

sudo npm install -g pm2
pm2 start "python3 -m http.server 8000" --name my-server
