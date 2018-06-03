from django.utils.crypto import get_random_string
import subprocess
from shutil import copyfile
import os


def ask_user(name, title, required, default=None, next_questions={}):
    print()
    print(f'{title} {"(Opcional)" if not required else ""}')
    if list(next_questions.keys()) != []:
        print(f'Opções: {list(next_questions.keys())}')
    if default is not None:
        default = str(default)
        print(f'Não digite nada para escolher "{default}"')
    answer = input(f'{name}: ')
    if required and next_questions != {}:
        while answer not in list(next_questions.keys()):
            print(f'{answer} deve estar em {list(next_questions.keys())}!')
            answer = input(f'{name}: ')
        for question in next_questions[answer]:
            process_question(question)
    if required and answer == '':
        if default is not None:
            answer = default
        while answer == '':
            print(f'{name} é obrigatório!')
            answer = input(f'{name}: ')
    return answer


def process_question(question):
    name = question['name']
    title = question['title']
    default = question.get('default', None)
    ask = question.get('ask', True)
    required = question.get('required', False)
    next_questions = question.get('next', {})
    value = default
    if ask:
        value = ask_user(name, title, required, default, next_questions)
    env_string = f'\n# {title}\n{name}={value}\n'
    with open(".env-temp", "a") as file:
        file.write(env_string)


def process_questions(questions):
    with open(".env-temp", "w+") as file:
        file.write('# Environment Variables\n')
    for question in questions:
        process_question(question)


env = [
    {
        'name': 'DEBUG',
        'title': 'Ativar modo de debug',
        'default': True,
        'ask': False
    },
    {
        'name': 'SECRET_KEY',
        'title': 'Chave privada de encriptação usada pelo Django',
        'default': get_random_string(32),
        'ask': False,
    },
    {
        'name': 'EMAIL_ACCOUNT',
        'title': 'Endereço de email para envio de logs de erro',
        'ask': True,
        'required': True
    },
    {
        'name': 'EMAIL_PASSWORD',
        'title': 'Senha do endereço de email',
        'ask': True,
        'required': True
    },
    {
        'name': 'ADMIN_ACCOUNT',
        'title': 'Conta de admin para receber logs de erro',
        'default': 'gustavomaronato@gmail.com',
        'ask': True,
        'required': True
    },
    {
        'name': 'ROOT_URL',
        'title': 'URL base do seu app',
        'default': 'localhost:8000',
        'ask': True,
        'required': True
    },
    {
        'name': 'REDIS_URL',
        'title': 'URL do servidor redis',
        'default': 'redis://localhost:6379/0',
        'ask': True,
        'required': True
    },
    {
        'name': 'FACEBOOK_KEY',
        'title': 'ID do seu app no Facebook',
        'ask': True,
        'required': True
    },
    {
        'name': 'FACEBOOK_SECRET',
        'title': 'Secret do seu app no Facebook',
        'ask': True,
        'required': True
    },
    {
        'name': 'FACEBOOK_PAGE_TOKEN',
        'title': 'Token de acesso de página do Facebook',
        'ask': True,
        'required': True
    },
    {
        'name': 'FACEBOOK_USE_CHATBOT',
        'title': 'Quer usar o chatbot incluso?',
        'ask': True,
        'required': True,
        'next': {
            'true': [
                {
                    'name': 'FACEBOOK_VERIFY_CHATBOT',
                    'title': 'String para verificação do chatbot (pode ser qualquer uma, mas DECORE)',
                    'ask': True,
                    'required': True,
                    'default': 'abc123'
                }
            ],
            'false': [
                {
                    'name': 'FACEBOOK_VERIFY_CHATBOT',
                    'title': 'String para verificação do chatbot (pode ser qualquer uma, mas DECORE)',
                    'ask': False,
                    'required': True,
                }
            ],
        }
    },
    {
        'name': 'INITIAL_COUNT',
        'title': 'Número inicial de spotteds (use apenas se já tinha uma página antes)',
        'ask': True,
        'required': True,
        'default': 0
    },
    {
        'name': 'RECAPTCHA_PUBLIC_KEY',
        'title': 'Chave pública do reCaptcha',
        'ask': True,
        'required': False,
    },
    {
        'name': 'RECAPTCHA_PRIVATE_KEY',
        'title': 'Chave privada do reCaptcha',
        'ask': True,
        'required': False,
    },
    {
        'name': 'WOT_SECRET',
        'title': 'Token do Web of Trust',
        'ask': True,
        'required': False,
    },
    {
        'name': 'GSB_SECRET',
        'title': 'Token do Google Safe Browsing',
        'ask': True,
        'required': False,
    },
    {
        'name': 'IMGUR_CLIENT',
        'title': 'Cliente do Imgur',
        'ask': True,
        'required': False,
    },
    {
        'name': 'IMGUR_SECRET',
        'title': 'Segredo do Imgur',
        'ask': True,
        'required': False,
    },
    {
        'name': 'SPOTTED_API_URL',
        'title': 'URL do SpottedAPI',
        'ask': False,
        'default': 'http://spottedapi.herokuapp.com'
    },
    {
        'name': 'SPOTTED_API_SECRET',
        'title': 'Token do SpottedAPI',
        'ask': True,
        'required': True
    },
]


if __name__ == "__main__":
    try:
        process_questions(env)
        print()
        print("Salvar alterações? (s/n)")
        r = 'd'
        while r not in ['s', 'n']:
            r = input()
        if r == 's':
            print('Salvando...')
            copyfile('.env-temp', '.env')
    except KeyboardInterrupt:
        print('\n')
        print('Revertendo alterações...')
        pass
    os.remove('.env-temp')
    print()
    print('Migrando banco de dados...')
    print(subprocess.check_output(['python', 'manage.py', 'migrate']).decode("utf-8"))
