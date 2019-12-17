## WillCode - PetsCarentesPlatform

TODO

### Tecnologias

Foram utilizadas as seguintes tecnologias:

* Backend: Python3 com framework Django 3.*
* Banco de dados mongodb 4.*

### Requisitos

1. Sistema operacional Linux, Windows ou MacOS.
2. Docker-CE instalado e corretamente configurado. - https://docs.docker.com/install/ 
3. Docker compose instalado e corretamente configurado. - https://docs.docker.com/compose/install/
4. Acesso aos repositorios do GitLab.
5. Acesso a internet.

### Instalação

TODO

1. Efetuar o clone do projeto, com a flag **--recurse-submodules** do GitHub: `git clone --recurse-submodules https://gitlab.com/willcode/petsCarentesPlatform.git`
2. Acessar o diretório do projeto: `cd petsCarentesPlatform`
3. Configurar as portas de acesso dos containers no arquivo **.env_setup**, em seguinda, criar uma cópia com o nome **.env**: `cp .env_setup .env` 
4. Copiar os arquivos de configuração, alterando os parâmetros que se façam necessários. Maiores detalhes na etapa **Configuração de instalação**
5. Rodar o arquivo docker-compose: `docker-compose --project-name {USUÁRIO} up -d`
6. Por ultimo certifique que o certificado seja instalado, maiores detalhes na seção **Certificado**.

#### Novas pastas:

1. Pasta **log** do Nginx: `sudo mkdir ./log`
2. Pasta **log** do Django: `sudo mkdir ./appApi/log`
3. Pasta **log** do Django: `sudo mkdir ./appWeb/log`

#### Permissões:

1. `sudo chmod -R 777 ./log`
2. `sudo chmod -R 777 ./appApi/log`
3. `sudo chmod -R 777 ./appWeb/log`

#### Configurações da instalação

##### Etapa 3

Na etapa **3**, você pode consultar as portas que estão em uso pelo comando `sudo docker ps -a`, preferivelmente utilize portas próximas as que já existem.

##### Etapa 4

Copiar o arquivo de configuração yml para dentro da pasta **app**.

Exemplo: `cp config_setup.yml app/config.yml`

Antes de copiar o arquivo, revise os parâmetros de configuração.

Um dos parâmetros importantes é o número de **WORKERs do Gunicorn**, que pode ser calculado, conforme a formula abaixo:

```
PROCESSOR_COUNT=$(nproc)
GUNICORN_WORKER_COUNT=$(( PROCESSOR_COUNT * 2 + 1 ))

echo $GUNICORN_WORKER_COUNT
```

##### Etapa 5

Na etapa **5**, substituir **{USUÁRIO}** pelo nome do usuário, onde a instalação será feita, EX:

```shell
sudo docker-compose --project-name pc_platform up -d
```

### Dependências python

Comando para instalação de dependências:

```shell
pip install -r /project/requirements.txt
```

### Conteúdo estático

Sempre que um arquivo estático, como JS, CSS ou plugin Jquery for alterado, é necessário rodar este comando:

```shell
python /project/manage.py collectstatic
```

Exemplo: `sudo docker exec -it pc_platform_appweb_1 bash -c "echo 'yes' | python /project/manage.py collectstatic"`

### Certificado

Rodar o container **certbot** para gerar os arquivos necessários para instalação do certificado.
O container **certbot** está compartilhando volumes com **webserver**, com origem local **./container/nginx/config/ssl_conf** e **./container/nginx/config/ssl_data**.
Substituir as variaveis pelos seus valores reais: **{{email}}**, **{{domain}}**.

A variável {{--staging}} é utilizada para testes.

```shell
docker-compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    {{--staging}} \
    --email {{email}} \
    {{-d domain}} \
    --rsa-key-size 4096 \
    --agree-tos \
    --force-renewal" certbot
```

Em seguida reinicie o container do **webserver**.

```
sudo docker restart webserver_1
```

O acesso por HTTPS deverá estar ok.
Para renovar, basta repetir os mesmos passos.

### Database

#### Primeira instalação:

1. Criar manualmente um database com o nome definido no arquivo **config.yml**.
2. Criar as collections: **pet**, **user**, **chat** e **pushQueue**.
3. Criar indice de geolocalização para a collection **pet**: `db.pet.createIndex({ location: "2dsphere" })`
4. Criar indice de geolocalização para a collection **user**: `db.user.createIndex({ location: "2dsphere" })`

### Cache

Para limpar o cache do python e visualziar as mudanças basta reiniciar o container onde está o serviço do python. Ex: `sudo docker restart {container_id}`

### Push

Os disparos em push são processados em uma fila, por um scrip python, podendo ser ativado com o seguinte comando:

```
sudo docker exec -it pc_api_app_1 bash -c "python manage.py PushQueue"
```