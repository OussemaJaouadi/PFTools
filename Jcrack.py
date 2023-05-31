import argparse
import json
import os
import base64
import jwt
import pyfiglet
from colorama import Fore, Style
from tqdm import tqdm
import time
import sys

def generate_full_banner():
    banner_title = pyfiglet.figlet_format('J Crack', font='slant')
    banner_description = "A Json Web Token cracking tool using dictionnairy attack , wordlists and base rules"
    developers = ['Oussema Jaouadi', 'Ghassen Abida', 'Hassen Bouchhiwa']

    max_name_length = max(len(name) for name in developers)
    padding = ' ' * (max_name_length + 46)  # 16 for spacing and bullet point
    developers_banner = [f'{padding}{Fore.BLUE}• {name}{Style.RESET_ALL}' for name in developers]
    developers_banner.append('')
    developers_banner.append('')
    developers_banner = '\n'.join(developers_banner)

    full_banner = f'{Fore.MAGENTA}{Style.BRIGHT}{banner_title}{Style.RESET_ALL} {Fore.WHITE}{Style.BRIGHT} \n {Style.RESET_ALL} {banner_description}\n\n{developers_banner}'
    return full_banner


def decode_jwt_token(token):
    tmp = token.split('.')
    header = base64.b64decode(tmp[0].encode()).decode()
    alg = json.loads(header)['alg']
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False},verify=False)
        payload = decoded_token
        return alg,header, payload
    except jwt.exceptions.InvalidTokenError:
        print(alg,header)
        return alg,header, None
    
def read_input(input_arg):
    if os.path.isfile(input_arg):
        with open(input_arg, 'r') as file:
            return file.read()
    return input_arg


def apply_transformation(jwt_token, rule, wordlist_path):
    alg,header, payload = decode_jwt_token(jwt_token)

    if not header or not payload:
        print(f'\n\n{Fore.RED}Failed to decode JWT token!{Style.RESET_ALL}')
        return

    print(f'\n{Fore.YELLOW}{Style.BRIGHT} * [Algorithme]:{Style.RESET_ALL} {alg}')
    print(f'{Fore.YELLOW}{Style.BRIGHT} * [Header]:{Style.RESET_ALL} {header}')
    print(f'{Fore.YELLOW}{Style.BRIGHT} * [Payload]:{Style.RESET_ALL} {payload}')
    print(f'\n{Fore.YELLOW} {"-"*70} ')

    with open(wordlist_path, 'r',encoding='latin-1') as file:
        file_length = sum(1 for _ in file)
    print('\n')
    with tqdm(total=file_length, desc=f"{Fore.LIGHTCYAN_EX}Cracking", unit="line") as progress_bar:
        with open(wordlist_path, 'r') as file:
            for line in file:
                line = line.strip()
                if rule == 'classic':
                    if jwt_token == jwt.encode(payload, line, algorithm=alg):
                        return f"\n     {Fore.GREEN}{Style.BRIGHT}[SECRET] : {line}" 
                elif rule == 'base64':
                    try :
                        test = jwt.decode(jwt_token, base64.b64encode(line.strip().encode()).decode(), algorithms=[alg])
                        return f"\n     {Fore.GREEN}{Style.BRIGHT}[Real] : {Style.RESET_ALL}{Style.BRIGHT}{line} \n     {Fore.GREEN}{Style.BRIGHT}[Encoded] : {Style.RESET_ALL}{Style.BRIGHT}{base64.b64encode(line.encode()).decode()}" 
                    except jwt.exceptions.InvalidSignatureError :
                        pass
                elif rule == 'base32':
                    try:
                        test = jwt.decode(jwt_token, base64.b32encode(line.strip().encode()).decode(), algorithms=[alg])
                        return f"\n     {Fore.GREEN}{Style.BRIGHT}[Real] : {Style.RESET_ALL}{Style.BRIGHT}{line} \n     {Fore.GREEN}{Style.BRIGHT}[Encoded] : {Style.RESET_ALL}{Style.BRIGHT}{base64.b32encode(line.encode()).decode()}" 
                    except jwt.exceptions.InvalidSignatureError :
                        pass
                progress_bar.update(1)
                sys.stdout.flush()
                time.sleep(0.01)


def main():
    full_banner = generate_full_banner()
    print(full_banner)

    parser = argparse.ArgumentParser(description='J Crack: JWT cracking tool')
    parser.add_argument('-i', '--input', help='Specify input (string or file name)')
    parser.add_argument('--rule', choices=['classic', 'base64', 'base32'],default='classic', help='Specify rule')
    parser.add_argument('-w', '--wordlist', default='/usr/share/wordlists/rockyou.txt', help='Specify wordlist')
    args = parser.parse_args()
    start_message = pyfiglet.figlet_format('Start attacking', font='digital')
    print(f'{Fore.GREEN}{Style.BRIGHT}{start_message}{Style.RESET_ALL}')

    print(f'{Fore.YELLOW}{Style.BRIGHT}Arguments used:\n\n')
    print(f'{Fore.YELLOW}{Style.BRIGHT} [Input]: {Style.RESET_ALL}{os.path.abspath(args.input)}')
    print(f'{Fore.YELLOW}{Style.BRIGHT} [Rule]: {Style.RESET_ALL}{args.rule}')

    wordlist_path = args.wordlist or '/usr/share/wordlists/rockyou.txt'
    if not os.path.isfile(wordlist_path):
        print(f"Invalid wordlist path: {wordlist_path}. Defaulting to /usr/share/wordlists/rockyou.txt")
        wordlist_path = '/usr/share/wordlists/rockyou.txt'
    print(f'{Fore.YELLOW}{Style.BRIGHT} [Wordlist]: {Style.RESET_ALL}{wordlist_path}')

    input_value = read_input(args.input)
    transformed_value = apply_transformation(input_value, args.rule, wordlist_path)
    if transformed_value is None:
        print(f'\n{Fore.RED}{Style.BRIGHT}Secret not found!{Style.RESET_ALL}')
    else:
        print(f'\n{Fore.GREEN}{Style.BRIGHT}Secret found : \n{"-"*30}\n{Style.RESET_ALL}{transformed_value}{Style.RESET_ALL}')


if __name__ == '__main__':
    main()
