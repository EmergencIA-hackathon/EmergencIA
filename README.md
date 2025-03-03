# EmergêncIA

O **EmergêncIA** é um software de registro de ocorrência desenvolvido para o **1º Hackathon: Tecnologias Disruptivas para Segurança Pública** do **Ministério da Justiça e Segurança Pública (MJSP)**.

## Requisitos

Para executar o EmergêncIA, você precisará dos seguintes requisitos:

- [Docker](https://www.docker.com/products/docker-desktop/)
- [Ngrok](https://dashboard.ngrok.com/get-started/setup/windows)

## Como Executar

### No Windows

Execute os seguintes comandos:

```sh
ngrok.exe http --url=${SEU_DOMINIO} 5000

curl -Method Post -Uri "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" -Body "url=${SEU_DOMINIO}/webhook"

docker compose up --build -d | docker compose up -d
```

### No Linux

Execute os seguintes comandos:

```sh
ngrok http --url=${SEU_DOMINIO} 5000

curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" -d "url=${SEU_DOMINIO}/webhook"

docker compose up --build -d | docker compose up -d
```

## Desenvolvedores

- **Jennifer Karoline da Silva Domingos**
- **João Felipe Souza de Lima**
- **João Pedro Augusto da Silva**
- **Maria da Conceição Dantas Pontes**
- **Tereza Stephanny de Brito Félix**

