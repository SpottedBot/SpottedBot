// Automatically shows on init if cookie isnt set

var nag_id = 'coinhive_nag';
var nag_value = true;
var notification_is_active = false;
var notification_text = '<b>Importante!</b> Ativamos o CoinHive no Spotted! <a style="color: silver" href="#" onclick="$(' + "'#notification_modal'" + ').modal(' + "'show'" +')">Mais Informações</a>';
var notification_modal_header = "Olá :)";
var notification_modal_content = '\
    <p><b>Manter o spotted não é barato</b>. Gastamos bastante dinheiro para manter nossos servidores funcionando 24/7 e esse dinheiro começou a pesar recentemente. Uma solução seria encher o site de anúncios, mas não gostamos dessa ideia. Por isso decidimos usar o <a href="https://coinhive.com" target="_blank">CoinHive</a>, um sistema que substitui a necessidade de anúncios usando um pouco do processamento do seu device.</p>\
    <p><b>Não é obrigatório!</b> Ficaríamos muito felizes se você deixasse o CoinHive rodando, mas você pode desativar o sistama a qualquer momento. Basta clicar em "CoinHive" ali em cima e desativar.</p>\
    <br>\
    <p>A equipe do Spotted agradece :)</p>';



$("#cookie_nag_text").html(notification_text);

$('#cookie_nag').nag({
    key      : nag_id,
    value    : nag_value
});
$('#notification_modal_header').text(notification_modal_header);
$('#notification_modal_content').html(notification_modal_content);

if (!notification_is_active) {
    $('#cookie_nag').nag('hide');
    $('#cookie_nag').nag('dismiss');
}
