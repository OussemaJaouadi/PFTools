import argparse
import hashlib
import os
import pyfiglet
import datetime
from colorama import Fore, Style
from tqdm import tqdm

def crack_hash(hash_to_crack, wordlist):
    #print(hash_to_crack)
    hash_algo, hashed_password = hash_to_crack.split(':')[1:]
    iterations,salt,hashed_password = hashed_password.split('$')
    #print(hash_algo,hashed_password,iterations,salt)
    iterations = int(iterations)
    try:
        salt = bytes.fromhex(salt)
    except ValueError:
        salt = salt.encode()

    
    with open(wordlist, 'r', encoding='latin-1') as file:
        total_passwords = sum(1 for _ in file)  # Count the total number of passwords in the wordlist
        file.seek(0)  # Reset the file pointer to the beginning

        with tqdm(total=total_passwords, desc='Cracking Password', unit=' password') as pbar:
            for password in file:
                password = password.strip()  # Remove leading/trailing whitespaces and line breaks
                hashed_attempt = hashlib.pbkdf2_hmac(hash_algo, password.encode(), salt, iterations)
                if hashed_attempt.hex() == hashed_password:
                    return password
                pbar.update(1)

    return None

def generate_full_banner():
    banner_title = pyfiglet.figlet_format('pbkdf2 cracker', font='big')
    banner_description = "A tool to crack PBKDF2-hashed passwords"
    developers = ['Oussema Jaouadi', 'Ghassen Abida', 'Hassen Bouchhiwa']

    max_name_length = max(len(name) for name in developers)
    padding = ' ' * (max_name_length + 46)  # 16 for spacing and bullet point
    developers_banner = [f'{padding}{Fore.BLUE}• {name}{Style.RESET_ALL}' for name in developers]
    developers_banner.append('')
    developers_banner.append('')
    developers_banner = '\n'.join(developers_banner)

    full_banner = f'{Fore.MAGENTA}{Style.BRIGHT}{banner_title}{Style.RESET_ALL} {Fore.WHITE}{Style.BRIGHT}\n{Style.RESET_ALL} {banner_description}\n\n{developers_banner}'
    return full_banner

def main():
    parser = argparse.ArgumentParser(description='pbkdf2 cracker - A tool to crack PBKDF2-hashed passwords')
    parser.add_argument('-i', dest='hash_file', help='Input file containing hashed password(s)')
    parser.add_argument('-w', dest='wordlist', help='Path to the wordlist file')

    args = parser.parse_args()

    hash_file = args.hash_file
    wordlist = args.wordlist

    if not hash_file or not os.path.exists(hash_file):
        print(f"{Fore.RED}Error: Hash file not found at '{hash_file}'. Please provide a valid hash file using the -i option.{Style.RESET_ALL}")
        return

    if not wordlist or not os.path.exists(wordlist):
        print(f"{Fore.RED}Error: Wordlist not found at '{wordlist}'. Please provide a valid wordlist file using the -w option.{Style.RESET_ALL}")
        return

    print(generate_full_banner())
    print(f"{Fore.CYAN}Hash File: {hash_file}\n")
    print(f"Wordlist: {wordlist}{Style.RESET_ALL}\n")

    print(f"{Fore.GREEN}{Style.BRIGHT}Starting cracking process...{Style.RESET_ALL}\n")
    start_time = datetime.datetime.now()

    with open(hash_file, 'r') as file:
        for hash_line in file:
            hash_line = hash_line.strip()  # Remove leading/trailing whitespaces and line breaks
            cracked_password = crack_hash(hash_line, wordlist)
            if cracked_password:
                print(f"{Fore.GREEN}Password found: {cracked_password}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Password not found.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{Style.BRIGHT}{'-' * 80}{Style.RESET_ALL}\n")

    end_time = datetime.datetime.now()
    duration = end_time - start_time

    print(f"{Fore.CYAN}{Style.BRIGHT}Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End Time: {Style.BRIGHT}{end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {Style.BRIGHT}{duration}{Style.RESET_ALL}")

if __name__ == '__main__':
    main()
