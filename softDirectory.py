import argparse
import os
import pyfiglet
import requests
from colorama import Fore, Style
import datetime
from tqdm import tqdm

def fuzz_directory(target_url, wordlist):
    with open(wordlist, 'r') as file:
        paths = file.read().splitlines()

    found_directories = []
    counter_200 = 0
    counter_401 = 0
    counter_403 = 0

    with tqdm(total=len(paths), desc='Fuzzing Directories', unit=' directory', ncols=80,
              bar_format='{l_bar}{bar} {n_fmt}/{total_fmt} [{postfix}]') as pbar:
        for path in paths:
            url = target_url + '/' + path
            response = requests.get(url)
            r = response.text


            if "401" in r:
                found_directories.append({
                    "url": url,
                    "status": 401
                })
                counter_401 += 1
            elif "403" in r:
                found_directories.append({
                    "url": url,
                    "status": 403
                })
                counter_403 += 1
            elif "404" in r :
                pass
            else :
                found_directories.append({
                    "url": url,
                    "status": 200
                })
                counter_200 += 1

            pbar.set_postfix({'200': counter_200, '401': counter_401, '403': counter_403})
            pbar.set_postfix_str(f"Testing: {path}")
            pbar.update(1)

    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'-' * 80}{Style.RESET_ALL}")

    print_directories(found_directories)


def print_directories(found_directories):
    print("\n\nDirectories Found:")
    print("------------------")

    if found_directories:
        for directory in found_directories:
            status = directory['status']
            url = directory['url']
            if status == 200:
                print(f"{Fore.GREEN}[+] {url}{Style.RESET_ALL}")
            elif status == 401:
                print(f"{Fore.YELLOW}[-] Unauthorized: {url}{Style.RESET_ALL}")
            elif status == 403:
                print(f"{Fore.RED}[-] Forbidden: {url}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}No directories found.{Style.RESET_ALL}")

def generate_full_banner():
    banner_title = pyfiglet.figlet_format('SoftFuzz', font='big')
    banner_description = "A directory fuzzing tool"
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
    parser = argparse.ArgumentParser(description='SoftFuzz - Directory Fuzzing Tool', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-u', '--url', help='Target URL (e.g., http://example.com)', required=True)
    parser.add_argument('-w', '--wordlist', help='Path to the wordlist file', default='/usr/share/wordlists/dirb/common.txt')

    args = parser.parse_args()

    target_url = args.url
    if not target_url.startswith('http://') and not target_url.startswith('https://'):
        target_url = 'http://' + target_url

    wordlist_path = args.wordlist

    if not os.path.exists(wordlist_path):
        print(f"{Fore.YELLOW}Wordlist not found at '{wordlist_path}'. Using default wordlist '/usr/share/wordlists/dirb/common.txt'.{Style.RESET_ALL}")
        wordlist_path = '/usr/share/wordlists/dirb/common.txt'

    print(generate_full_banner())
    print(f"{Fore.CYAN}Target URL: {target_url}\n")
    print(f"Wordlist: {wordlist_path}{Style.RESET_ALL}\n")

    print(f"{Fore.GREEN}{Style.BRIGHT}Starting attack...{Style.RESET_ALL}\n")
    start_time = datetime.datetime.now()

    print(f"{Fore.CYAN}{Style.BRIGHT}{'-' * 80}{Style.RESET_ALL}\n")

    fuzz_directory(target_url, wordlist_path)

    end_time = datetime.datetime.now()
    duration = end_time - start_time

    print("\n\nAttack completed!")
    print(f"{Fore.CYAN}{Style.BRIGHT}Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End Time: {Style.BRIGHT}{end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {Style.BRIGHT}{duration}{Style.RESET_ALL}")

if __name__ == '__main__':
    main()
