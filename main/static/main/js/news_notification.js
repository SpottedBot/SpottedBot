// Automatically shows on init if cookie isnt set
$("#cookie_nag_text").html('Olá! Algumas coisas mudaram aqui no Spotted. <a style="color: silver" href="#" onclick="$(' + "'#notification_modal'" + ').modal(' + "'show'" +')">Clique aqui</a> para saber das novidades!');
$('#cookie_nag').nag({
    key      : 'accepts-cookies',
    value    : true
});
$('#notification_modal_header').text("SpottedBot v2!");
$('#notification_modal_content').html('\
    <p><b>Spotteds mais intuitivos.</b> Refizemos todo o fluxo de envio de Spotteds. Tiramos todos aqueles tutoriais confusos e opções redundantes.</p>\
    <p><b>Recomendações inteligentes.</b> Nós também fizemos o Spotted mais inteligente! Ele lê o seu spotted e te sugere crushes para você marcar.</p>\
    <p><b>Menos é mais.</b> Também removemos a opção de Spotteds públicos e privados. Ninguém entendia o que elas faziam mesmo!</p>\
    <p><b>Inteligência artificial ao resgate.</b> Por fim nós atualizamos nosso Bot Moderador. Seus spotteds são avaliados instantâneamente para que você não tenha mais que ficar esperando horas até a moderação te aprovar!</p>');

