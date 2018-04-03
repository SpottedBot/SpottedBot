[![Build Status](https://travis-ci.org/SpottedBot/SpottedBot.svg?branch=master)](https://travis-ci.org/SpottedBot/SpottedBot) [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

[![forthebadge](https://forthebadge.com/images/badges/fuck-it-ship-it.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

SpottedBot
==========

A platform for university students to send "spotteds", that aims to be completely automated using artificial intelligence to check for spam or inadequate messages.

How does it work?
-------------
Spotteds are submitted through the main app's page and their attachments are sent to Web of Trust's API to be evaluated. They are also sent to Google Safe Browsing and are only deemed safe if both reply that the links are safe.

Next, the spotted is sent to the SpottedAPI for evaluation. The SpottedAPI decides whether it should be posted to Facebook right away, rejected and deleted or sent to human evaluation.

If it is posted, notifications are sent through Facebook's Notification API to every person related to the spotted.

If it is sent to human evaluation, moderators will then analyze the spotted's contents and either approve it for publication or reject it. The decision is again sent to the SpottedAPI to be incorporated into it.


# Setup

## APIs e mais APIs

Você vai precisar pegar chaves de várias APIs.
Vamo das mais complicadas pra as mais simples:

### Facebook

Antes de começar, certifique-se de que você é Admin da página que quer associar ao seu spotted.

* Começe virando um Dev do Facebook. [Clique aqui](https://developers.facebook.com/)
* Crie um app pro seu spotted
* Dentro do seu app, vá para `Settings -> Basic` e clique, no final, em `Add Plataform`
 * Clique em `website` e digite o nome do seu domínio do heroku(https://unicampspotted.herokuapp.com por exemplo) e salve suas alterações
 * Clique em `Add Plataform` de novo e adicione um `Facebook Canvas`. Em `Secure Canvas URL` digite seu site de novo e salve suas alterações
* No seu app, vá para `App Review` e clique em `Make ___ Public?` e salve suas alterações
* Vá em `Dashboard` e anote seu `App ID` e `App Secret`. Vamos usar eles mais tarde.

Agora vamos pegar o Token da sua página.

Siga [esse tutorial](https://medium.com/@Jenananthan/how-to-create-non-expiry-facebook-page-token-6505c642d0b1)

Entre no [Graph Explorer](https://developers.facebook.com/tools/explorer/)

* Em `Application`, selecione o app que acabou de criar
* Em `Get Token`, selecione `Get User Access Token`
* Na janelinha, selecione `manage_pages` e `publish_pages` e clique em `Get Access Token`
* Clique em `Get Token` de novo e selecione a sua página.
* Copie o Token inteiro e vá para o [Token Debugger](https://developers.facebook.com/tools/debug/accesstoken)
* Cole o seu token e aperte em `Debug`
* Lá em baixo, clique em `Extend Access Token`
* Pegue esse Token novo, anote e guarde com sua vida

Se você fez tudo certo, terminamos com o Facebook.

### reCaptcha

Vamos pegar umas chaves pro nosso reCaptcha agora. Ninguém gosta de bots enviando milhões de spotteds pra a gente e spammando nossa caixa, né?

[Clica aqui](https://www.google.com/recaptcha/intro/) e se cadastra lá.

Vai em `Register a new site` em domínio digita o domínio do seu site. Se você tiver um domínio próprio, digita ele aqui. Digita o do heroku tb(Ex: unicampspotted.herokuapp.com) sem o http e pá

Em `client-side integration` você vai ver uma parada tipo assim:

`<div class="g-recaptcha" data-sitekey="6LdeuwcUAAAAAOmN80hxQzWGMIVPqHhWkQPJQV4O"></div>`

Pega esse `6LdeuwcUAAAAAOmN80hxQzWGMIVPqHhWkQPJQV4O` e anota como sua public key do recaptcha

Em `server side integration` pega e anota o `secret` como sua secret key do recaptcha

Done.

### Web of Trust

Ninguém gosta de receber vírus ou pornografia como anexo, especialmente nos spotteds.

Vamos prevenir isso usando alguns filtros de URLs perigosas.

Cria uma conta [aqui](https://www.mywot.com/)

Dentro do seu perfil, procura por API

Clica lá e cria um Token pra você. Guarda esse token tb

### Google Safe Browsing

Ninguém melhor que o google pra filtrar urls né não diga aí

vira um dev do [Google Cloud](https://cloud.google.com/)

tenta [clicar aqui](https://console.cloud.google.com/apis/api/safebrowsing.googleapis.com/overview) pra acessar o console na Google Safe Browsing API.

Clica lá em `ENABLE`

Vem [aqui agora](https://console.cloud.google.com/apis/credentials) e cria uma credencial pra você com acesso a tudo e pá

Pega a `Key` e guarda ela.

### GoogleAds

Se você quiser colocar google ads no seu site, [venha aqui](https://www.google.com/adsense/start/) e pegue o `google_ad_client`.

Salve esse valor tb como seu cliente do Google Ads

### Imgur

Você também pode permitir que seus usuários façam upload de imagens. Essas imagens não ficam salvas no seu servidor. Elas são automaticamente enviadas para o imgur por meio da api deles.

Para permitir isso, você precisa da chave de cliente e do secret de uma conta no imgur.

Primeiro [entre ou crie uma conta](https://imgur.com/register?redirect=https%3A%2F%2Fimgur.com%2F) e depois [crie um client novo aqui](http://api.imgur.com/oauth2/addclient).

Na criação do cliente, selecione "Anonymous usage without user authentication".

A URL de callback pode ser qualquer coisa. Coloque algo como `https://<nome_do_seu_spotted>.herokuapp.com`

Copie e guarde as chaves que ele dá no final.

### SpottedAPI

Guardei o melhor pro finak, uhu

Pra postar os spotteds bonitinho você precisa se comunicar com minha api.

Infelizmente só quem tem minha permissão pode ter uma key da minha api.

Pede pra mim que eu provavelmente sou bem de boa em deixar *wink wink*

# Finalmentes

Você pode clonar esse rep e rodar tudo local usando esses valores aí de cima dentro de um `.env`, ou pode ir adiante e jogar tudo no heroku direto.

Pra fazer isso, basta clicar no botão abaixo e colocar as paradas certas quando ele pedir. Você já deve ter tudo que precisa.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Heroku CLI

Instala a [CLI do Heroku](https://devcenter.heroku.com/articles/heroku-cli)

e executa os seguintes comandos, depois de logar na sua conta pelo CLI:

`heroku run --app <nome-do-seu-app> python manage.py migrate`

Agora você vai querer criar uma conta de superusuário. Com ela você vai conseguir adicionar moderadores e pá

`heroku run --app <nome-do-seu-app> python manage.py createsuperuser`

