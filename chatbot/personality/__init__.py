import random


class PersonalityGen:
    def __init__(self):
        for pers, values in personalities.items():
            setattr(self, pers, self.rand_pers(values))

    def rand_pers(self, pers):
        return random.choice(pers)


personalities = {
    'greetings': [
        'Oie!',
        'Oie',
        'Olá :)',
        'Helou!',
        'Olar',
        'Colé de merma!',
        'Fala aí 😎',
    ],
    'polite_followback': [
        'Tudo de boa?',
        'Tudo bom?',
        'Suave?',
        'Tudo de buenas?',
        'Tudo bem?',
    ],
    'hold_spotted': [
        'Segura esse spotted aí!',
        'Não manda o spotted ainda!',
        'Ainda não manda o spotted!',
    ],
    'lets_talk': [
        'Vamos bater um papo antes',
        'Vamos bater um papo :)',
        'Conversa comigo antes!',
        'Conversa comigo primeiro :)',
        'Saca só as infos primeiro!'
    ],
    'base_messages': [
        'Diz aí do que você precisa',
        'Me conta mais sobre como posso te ajudar',
        'Que posso fazer por ti?',
        'Sdds crush... :(\nOpa! Como posso ajudar?',
        'Me fala como que eu posso te ajudar',
        'What business have you?',
        'Yes?',
        'E esse lolzinho?\nMas sério, como posso ajudar?',
        "Somebody once told me the world roll me. I ain't the sharpest tool in the shed...🎶\nEpa hehe :), como posso ajudar?",
        "'Cause if you liked it, then you should have put a ring on it...🎶\nRainha me distraiu :D\n Onde estávamos?",
        'Yes milord?',
        '"Algumas pessoas sentem a chuva, outras só se molham"\nEr, chat errado! Como posso ajudar?',
        'Traz o papel higiênico aqui pls.\nOpa, chat errado hehe 😳\nComo posso ajudar?',
        'To chegando aí pro Netflix 😏\nAh, chat errado 😳\nComo posso ajudar?',
        'Pesquisas apontam que com o Spotted suas chances no <3 crescem em 312%\nQue tal enviar um?',
        'O que é inteligente, te entende, responde rápido e cozinha o melhor Tiramisu do mundo?\nO Spotted 😏',
        'ELA O QUE?\nOops, número errado :O, Como posso ajudar?',
        'Wubba lubba dub dub!\nHehe, como posso ajudar?',
        'Você quer brincar na neve?\nQuem dera. Enquanto isso, você quer mandar um spotted?',
        'Tem um momento para ouvir a palavra do SpottedBot?',
        'THE CAKE IS A LIE!\nMas seu crush não precisa saber ;)',
        'What does the fox say?\n"Vamo se pegar!"',
        'Autodestruição em 3, 2, 1...',
        'E essa saúde mental? Não deixa em segundo plano!',
        'Você é incrível! Sério, nunca esqueça :)\nEspalhe o amor com um Spotted!',
        'Você é a minha pessoa favorita nesse momento, sabia?\nO que mais posso fazer por você?',
        'Hey, crush 😏\nQual o motivo da sua visita?',
        'Vem sempre aqui?',
        'Quando é a próxima festa?\nEnquanto isso, pq não se preparar pra ela com um spotted?',
        'Que todos os seus spotteds sejam aprovados e seus crushes não sejam trouxas ;)',
        'Oi Siri! Manda um Spotted pra mim!',
        'Nessa crise de privacidade, sabia que o Spotted nunca compartilha seus dados pessoais?'
    ],
    'send_spotted1': [
        'Adeus spotteds pelo inbox, olá privacidade!',
        'Privacidade rainha, inbox nadinha! :D',
        'Segura esse teclado! Não é aqui que manda :)',
        'Aí sim! Espalha esse amor 😏',
        'Essa é a sua chance! (mas sempre tem outra) :)',
    ],
    'send_spotted2': [
        'Pra mandar o spotted, é só acessar o nosso site:',
        'Respira fundo e vai lá no site pra enviar!',
        'Manda lá pelo nosso site que a privacidade é garantida!',
        'Seu Spotted + Nosso site = Sucesso no <3'
    ]
}
