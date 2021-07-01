# Как запустить тесты
### 1) Установить Docker на ubuntu:18.04: 
`sudo apt-get update`  
`sudo apt-get —no-install-recommends install -y \`  
`apt-transport-https \`  
`ca-certificates \`  
`curl \`  
`gnupg-agent \`  
`software-properties-common`  
`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`   
`sudo add-apt-repository \`  
`"deb [arch=amd64] https://download.docker.com/linux/ubuntu \`  
`$(lsb_release -cs) \`  
`stable"`  
`sudo apt-get update`   
`sudo apt-get —no-install-recommends install -y docker-ce docker-ce-cli containerd.io`  
### 2) Выдать права доступа Docker:
`sudo groupadd docker`  
`sudo usermod -aG docker $USER`  
`newgrp docker`  
### 3) Создать образ с помощью Dockerfile с названием "tests" из текущей директории (там, где лежит Dockerfile):  
`sudo docker build -t tests .`
### 4) Создать контейнер из образа "tests" и запустить его:  
`sudo docker run -p 443:443 tests`
