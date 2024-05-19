sudo docker build -t njs .
sudo docker stop $1
sudo docker run -d -p 1026:1024 njs
