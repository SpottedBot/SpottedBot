[![Build Status](https://travis-ci.org/SpottedBot/SpottedBot.svg?branch=master)](https://travis-ci.org/SpottedBot/SpottedBot) [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

# SpottedBot

A platform for university students to send "spotteds", that aims to be completely automated using artificial intelligence to check for spam or inadequate messages.

It's being used by many universities in Brazil as a state-of-the-art spotted automation system.

It's stable and [live](https://spottedsunicamp.herokuapp.com/) with more than five thousand users and about three hundred daily spotted submissions.

## Features

SpottedBot is packed with various features. Check out some of them:

### For users
- Users can easily submit spotteds though the web interface
- Attachments can be added to the spotted, including picture URLs
- Imgur integration for uploading of images
- Facebook integration for user login (enables users to delete their spotteds later)
- Ability to tag other users that have logged in using Facebook, leting they see the tagged posts in their dashboards.
- The bot automatically scans spotteds to find names to tag
- Users receive Facebook notifications when their spotteds are accepted or when they are tagged
- Spotteds can be reported to the moderation or deleted by users and tagged users
- All spotteds are anonymous to the moderation and to the general public. Only the poster and the tagged person(if allowed) know each other's identities

### For moderators
- Spotteds are automatically posted to your Facebook page using the Graph API
- Artificial intelligence learns from your moderation patterns and automatically approves or rejects spotteds, sending to you only the ones that it's insecure about
- reCaptcha integration to prevent bot abuse
- Integrated contact form
- Easy to use interface to approve or reject spotteds
- Attachments are processed using Google's Safe Browsing API and the Web of Trust API to ensure that no malicious links are posted nor shown to you
- Includes an easy to setup chatbot for Messenger that engages with user's and serves as FAQ with fallback to humans only if presented with hard-to-answer questions
- Automatically logs moderator activity to track and rank the most active moderators
- Option to enable [CoinHive](https://coinhive.com/) and Google Ads.

## Pré Setup (in Portuguese)

A configuração do SpottedBot é relativamente simples. A maioria dos passos será para coleta de chaves de API usadas pelo bot. Nenhuma alteração é necessária no código, apesar de você ter a opção de alterar o CSS para personalizar seu bot.

### Chaves de API

Vamos então seguir para a coleta das chaves. Boa parte delas é opcional e nenhuma deve custar nada.

#### reCaptcha (Opcional)

A API do reCaptcha é opcional e usada durante a submissão de spotteds.

Vá para a [página do reCaptcha](https://www.google.com/recaptcha/intro/) e efetue seu cadastro.

Vai em *Register a new site* em domínio digite o domínio do seu site.

Se você tiver um domínio próprio, digite ele aqui. Senão, usaremos o Heroku para hospedagem. O formato do domínio no Heroku é `<nome-do-app>.herokuapp.com`

Você também pode colocar `localhost` se quiser fazer testes na sua máquina local.

Em *client-side integration* você vai ver algo assim:

`<div class="g-recaptcha" data-sitekey="6LdeuwcUAAAAAOmN80hxQzWGMIVPqHhWkQPJQV4O"></div>`

Pega esse `6LdeuwcUAAAAAOmN80hxQzWGMIVPqHhWkQPJQV4O` e anota como sua public key do reCaptcha. Vamos usar depois.

Em *server side integration* pega e anota o `secret` como sua secret key do reCaptcha, que também vamos usar depois.

#### Web of Trust (Opcional)

A API do WoT é usada para verificar os attachments enviados. Ela impede que links maliciosos sejam enviados.

Comece criando uma [conta na API](https://www.mywot.com/)

Dentro do seu perfil, procure por *API*. Lá será possível criar um `token`. Anote-o como token do WoT.

#### Google Safe Browsing (Opcional)

Usado no mesmo lugar que o WoT para uma segunda camada de segurança.

Comece se tornando um dev na [Google Cloud](https://cloud.google.com/)

Acesse o [console](https://console.cloud.google.com/apis/api/safebrowsing.googleapis.com/overview) da Google Safe Browsing API.

Clique em *ENABLE*

Crie [credenciais](https://console.cloud.google.com/apis/credentials) para acessar a API.

Salve a *Key* como token do GSB.

#### Google Ads (Opcional)

É bem difícil ser aceito pelo Google Ads com um site como esse, pois ele tem poucas páginas, mas você pode tentar se quiser.

[Crie uma conta](https://www.google.com/adsense/start/) no AdSense e guarde o `google_ad_client`.


#### Imgur (Opcional)

Você também pode permitir que seus usuários façam upload de imagens. Essas imagens não ficam salvas no seu servidor. Elas são automaticamente enviadas para o imgur por meio da api deles.

Para permitir isso, você precisa da chave de cliente e do secret de uma conta no imgur.

Primeiro [entre ou crie uma conta](https://imgur.com/register?redirect=https%3A%2F%2Fimgur.com%2F) e depois [crie um client novo aqui](http://api.imgur.com/oauth2/addclient).

Na criação do cliente, selecione "Anonymous usage without user authentication".

A URL de callback pode ser qualquer coisa. Coloque algo como `https://<nome_do_seu_spotted>.herokuapp.com`

Copie e guarde as chaves que ele dá no final.


#### SpottedAPI

SpottedAPI é a API usada na análise de spotteds.

Para conseguir um token basta falar comigo por email: `gustavomaronato` (no gmail)


#### Facebook

A GraphAPI do Facebook é usada para fazer login de usuários e para postar na página.

Comece se certificando de que você é admin da sua página de spotteds. Se não tiver uma, crie.

Agora basta se [tornar um dev](https://developers.facebook.com/) e clicar em *criar app*.

Dentro do seu app, você vera uma tela pedingo para *Adicionar produto*. Comece selecionando *Facebook Login*.

Na criação do login, selecione *Web* e coloque a URL do seu site (ou `https://localhost:8000`) se for começar testando localmente. Clique em *Save* e *Continue*. Pronto.

No menu da esquerda procure por *Facebook Login* e selecione *Settings* dentro dele.

Em *Settings*, vá para *Valid OAuth Redirect URIs* e digite `https://<Seu-Domínio>/auth/facebook/login_response/`,
trocando `<Seu-Domínio>` pelo domínio do seu site. Se for usar o Heroku, use `https://<nome_do_seu_spotted>.herokuapp.com`.
Se for fazer testes locais, `https://localhost:8000/auth/facebook/login_response/`

Clique em *Save Changes*.

Agora, no menu da esquerda, procure por *Settings->Basic*. Em *App Domains* digite os domínios do seu app (`localhost` se testando localmente)

Desça a tela até ver *Website*. Preencha com a url do seu site (ou `http://localhost:8000/`).

Volte ao topo e anote os valores em *App ID* e *App Secret*.

O próximo passo será gerar um token de acesso para seu app conseguir postar em sua página.

Siga [esse tutorial](https://medium.com/@Jenananthan/how-to-create-non-expiry-facebook-page-token-6505c642d0b1) a partir do passo 2.

***Atenção!** Na hora de selecionar as permissões do token, selecione `pages_messaging` caso queira usar o chatbot incluído!*

Guarde o token de acesso e vamos agora para o setup local do seu SpottedBot!

## Setup Local

Os requerimentos do spottedbot são:
- Python >=3.6.5
- SQLite 3
- PostgreSQL
- Redis

Comece [instalando Python 3.6.5 ou superior](https://www.python.org/)

agora [instale SQLite 3](https://www.sqlite.org/index.html)

e [PostgreSQL](http://initd.org/psycopg/)

por fim, [instale o Redis](https://redis.io/).

Para rodar localmente, recomendo que você use o [virtualenv](`https://virtualenv.pypa.io/en/stable/`) para isolar seus pacotes do SpottedBot do resto dos seus projetos.

Depois de instalado, ative o `virtualenv` e rode:
```
pip install -r requirements.txt
```
para instalar as dependências.

Agora rode:
```
python initialize.py
```
e siga as instruções.

Crie um super usuário para acessar a tela de admin:
```
python manage.py createsuperuser
```
e teste seu app rodando:
```
./run.sh
```
*Para fechar, use ctrl+c*

Esse comando faz 3 coisas:
- Inicia o seu servido de Django
- Inicia o servidor do Redis
- Instancia um Celery worker que vai cuidar de jobs paralelos

Para se conectar à API do Facebook para login e tal, é necessária uma conexão HTTPS (ou o uso de uma porta exposta - [veja abaixo](#exposição-de-portas-opcional)). Para iniciar uma versão do servidor com suporte limitado para HTTPS, execute:
```
./run-ssl.sh
```

Agora vamos testar seu login com o Facebook. Inicie seu app com `./run-ssl.sh`, acesse [seu app](https://localhost:8000) e clique em fazer login com facebook.

Se tudo estiver configurado corretamente, você deve ser capaz de logar e uma conta será criada no site. Agora vá para [a tela de Admin](https://localhost:8000/admin) e faça o login com suas credenciais de super usuário.

Nessa nova tela, vá em *Moderators-Adicionar* e selecione o usuário com seu nome. Clique em *Salvar* e depois em *Encerrar Sessão*.

Volte para [seu app](https://localhost:8000), faça o login e vá na tela [Meus Spotteds](https://localhost:8000/dashboard/). A tela de moderação deve estar disponível.

Experimente agora enviar um spotted e depois aprová-lo pela tela de moderação!

### Exposição de portas (Opcional)
(Obrigatório para teste local do Chatbot)
Outra recomendação é que você instale algum serviço para expor seu app para a internet. Ele será útil enquanto você estiver testando seu app, configurando o seu chatbot e se quiser compartilhar a sua tela de desenvolvimento com alguém.

Recomendo que você use o [ngrok](https://ngrok.com/) ou o [localtunnel](https://localtunnel.github.io/www/)

*Obs: Se for expor sua porta, inicie seu servidor com `./run.sh`*

Você agora deve ser capaz de abrir seu app usando o link fornecido pela ferramenta.

*Obs: Esses links são temporários e mudam a cada vez que você roda o ngrok ou localtunnel*

## Configurando o Chatbot pro Messenger (Opcional)

Caso você queira usar o chatbot incluso, você deve configurar o messenger. Volte na página de configurações do seu App Facebook e clique no `+` para adicionar outro produto. Dessa vez você vai escolher *Messenger*.

Na página de configuração do Messenger, vá para *Token Generation*, selecione sua página e gere um token(não vamos usar ele por enquanto)

Agora vá em *Webhooks*, *Setup Webhooks*.

Em *Callback URL*, digite `https://<Seu-Domínio>/hooks/messenger/`

*Obs: se você estiver testando o site localmente, você deverá usar o domínio do localtunnel ou do ngrok, **não localhost***

Em *Verify Token*, coloque a sequência de caracteres que você digitou em `Token de verificação do Messenger` quando rodou o [initialize.py](#setup-local)

Agora selecione `messages`, `messaging_postbacks`, `standby`, `message_echoes` e `messaging_handovers` e aperte *Verify and Save*

A página deve recarregar. Vá novamente em *Webhooks*, selecione sua página em *Select a Page* e clique em *Subscribe*

Vamos configurar sua página agora. Vá até sua página no Facebook e clique em *Settings*. Na lista da esquerda, clique em *Messenger Platform*. Selecione *Responses are partially automated, with some support by people* e, em *Subscribed Apps*, marque o seu app como *Primary Receiver* e *Page Inbox* como *Secondary Receiver*.

Pare o servidor (não o localtunnel/ngrok) e execute:
```
python manage.py setup_messenger
```
Inicie o servidor novamente, vá até sua página e abra uma janela de chat.


## Subindo para o Heroku

Para subir seu app para o Heroku, clique no botão abaixo e siga as instruções:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Todo

- [ ] put all of these instructions in a wiki or docs
