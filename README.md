## PetsCarentesPlatform

Serviços de api para o aplicativo PetsCarentes.

### Tecnologias

* Backend: Python com framework Starlette.
* Banco de dados Mongodb.
* Fila assíncrona com redis.
* Orquestração de containers com docker e docker-compose.

### Requisitos

1. Sistema operacional Linux, Windows ou MacOS.
2. Docker-CE instalado e corretamente configurado. - https://docs.docker.com/install/
3. Docker compose instalado e corretamente configurado. - https://docs.docker.com/compose/install/

### Roadmap

* Reconhecimento de imagem: A API OpenAI GPT-3 pode ajudar a criar um modelo de reconhecimento de imagem que pode
  identificar animais em fotos, identificar raças e outras características dos animais.
* Chatbots: A API OpenAI GPT-3 também pode ajudar a criar chatbots para responder às perguntas dos usuários sobre
  animais e fornecer informações úteis sobre a adoção e cuidados de animais.
* Geração de Texto: A API OpenAI GPT-3 pode ser usada para gerar automaticamente descrições de animais, como
  personalidade, comportamento, hábitos alimentares, etc.
* Análise de Sentimento: A API OpenAI pode ser usada para analisar o sentimento dos usuários em relação ao seu
  aplicativo e à adoção de animais.
* Recomendação de animais: A inteligência artificial pode ser usada para recomendar animais para os usuários com base em
  suas preferências e histórico de adoção.

### Configuração

1. Setar as variáveis de ambiente no arquivo **.env**. Nos diretórios `./pets_carentes_platform` e `.
   /pets_carentes_platform/app_api/` (renomear .env_setup para .env).

### Instalação

1. docker-compose up -d

### Testes

```
cd app_api
docker exec pets_carentes_platform_app_api_1 bash -c "cd app_api && coverage run -m pytest && coverage report && coverage lcov -o coverage/lcov" && genhtml coverage/lcov -o coverage/html && open coverage/html/index.html
```

### Certificado - TODO

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

### Database

1. Criar manualmente um database com o nome definido no arquivo **.env**.
2. Criar as collections: **pet**, **user**.
3. Criar índice de geolocalização para a collection **pet**: `db.pet.createIndex({ location: "2dsphere" })`
