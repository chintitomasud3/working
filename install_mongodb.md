sudo apt-get update

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

na hole :  sudo rm -f /usr/share/keyrings/mongodb-server-7.0.gpg
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg

sudo apt update
sudo apt-get upgrade
## Install 
sudo apt install -y mongodb-org


## MongoDB start & enable
sudo systemctl start mongod
sudo systemctl enable mongod

## mongodb status check
sudo systemctl status mongod


##mongo mongoose shell check

mongosh

## change the bind ip
sudo nano /etc/mongod.conf

bindIp: 127.0.0.1 er jaigay  bindIp: 0.0.0.0

