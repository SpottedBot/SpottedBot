SpottedBot
==========

O que é?
--------
É uma plataforma de spotteds que almeja funcionar de forma 100% automatizada

Funcionamento
-------------
O app usa o Graph API do Facebook para postar os Spotteds e usa uma REST API feita por mim, ainda a ser postada, para filtrar as paradas.


Configuração
------------

##APIs e mais APIs

Você vai precisar pegar chaves de várias APIs.
Vamo das mais complicadas pra as mais simples:

###Facebook

Antes de começar, certifique-se de que você é Admin da página que quer associar ao seu spotted.

* Começe virando um Dev do Facebook. [Clique aqui](https://developers.facebook.com/)
* Crie um app pro seu spotted
* Dentro do seu app, vá para `Settings -> Basic` e clique, no final, em `Add Plataform`
 * Clique em `website` e digite o nome do seu domínio do heroku(https://unicampspotted.herokuapp.com por exemplo) e salve suas alterações
 * Clique em `Add Plataform` de novo e adicione um `Facebook Canvas`. Em `Secure Canvas URL` digite seu site de novo e salve suas alterações
* No seu app, vá para `App Review` e clique em `Make ___ Public?` e salve suas alterações
* Vá em `Dashboard` e anote seu `App ID` e `App Secret`. Vamos usar eles mais tarde.

Agora vamos pegar o Token da sua página.

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

###reCaptcha

Vamos pegar umas chaves pro nosso reCaptcha agora. Ninguém gosta de bots enviando milhões de spotteds pra a gente e spammando nossa caixa, né?

[Clica aqui](https://www.google.com/recaptcha/intro/) e se cadastra lá.

Vai em `Register a new site` em domínio digita o domínio do seu site. Se você tiver um domínio próprio, digita ele aqui. Digita o do heroku tb(Ex: unicampspotted.herokuapp.com) sem o http e pá

Em `client-side integration` você vai ver uma parada tipo assim:

`<div class="g-recaptcha" data-sitekey="6LdeuwcUAAAAAOmN80hxQzWGMIVPqHhWkQPJQV4O"></div>`

Pega esse `6LdeuwcUAAAAAOmN80hxQzWGMIVPqHhWkQPJQV4O` e anota como sua public key do recaptcha

Em `server side integration` pega e anota o `secret` como sua secret key do recaptcha

Done.

###Web of Trust

Ninguém gosta de receber vírus ou pornografia como anexo, especialmente nos spotteds.

Vamos prevenir isso usando alguns filtros de URLs perigosas.

Cria uma conta [aqui](https://www.mywot.com/)

Dentro do seu perfil, procura por API

Clica lá e cria um Token pra você. Guarda esse token tb

###Google Safe Browsing

Ninguém melhor que o google pra filtrar urls né não diga aí

vira um dev do [Google Cloud](https://cloud.google.com/)

tenta [clicar aqui](https://console.cloud.google.com/apis/api/safebrowsing.googleapis.com/overview) pra acessar o console na Google Safe Browsing API.

Clica lá em `ENABLE`

Vem [aqui agora](https://console.cloud.google.com/apis/credentials) e cria uma credencial pra você com acesso a tudo e pá

Pega a `Key` e guarda ela.

###SpottedAPI

Guardei o melhor pro finak, uhu

Pra postar os spotteds bonitinho você precisa se comunicar com minha api.

Infelizmente só quem tem minha permissão pode ter uma key da minha api.

Pede pra mim que eu provavelmente sou bem de boa em deixar *wink wink*

#Finalmentes

Você pode clonar esse rep e rodar tudo local usando esses valores aí de cima dentro de um `.env`, ou pode ir adiante e jogar tudo no heroku direto.

Pra fazer isso, basta clicar no botão abaixo e colocar as paradas certas quando ele pedir. Você já deve ter tudo que precisa.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

##Tchüss!
