# PF-Tools

## Description

Some tools we developped during our `PFA` project with different functionalities :

* **`JCrack`** : JWT Cracking Tool
* **`pbkdf2 cracker`** : PBKDF2 Hash Cracker
* **`SofFuzz`** : Customised Web Directory fuzzing
* **`ExiftShell`** : DNS exfiltration encoded reverse shell server 

## Install Requirment 

```bash
pip install -r requirment.txt
```

## [JCRACK](Jcrack.py)

* Arguments : 
  * -h : For Help
  *  -i Input : It can be a string or a file
  * -w wordlist : The path of the wordlist of the attack (`/usr/share/wordlists/rockyou.txt` by default)
  * --rule : 
    * classic : cracking using the lines of the file
    * base32 : encoding lines in base32 before attacking
    * base64 : encoding lines in base64 before attacking
* Use Exemple : 
    ```bash
    python Jcrak.py -i token --rule base64
    ```

## [PBKDF2 Cracker](werkCrack.py)

* Arguments : 
  * -i Input : The file containing hash(s)
  * -w wordlist : The path of the wordlist of the attack (`/usr/share/wordlists/rockyou.txt` by default)
* HashFormat :
    - `pkbdf2:<algo>:<iterations>$SALT$HASH`
    - the format usually found in SQLITE databases
* Use Exemple
  ```bash
    python werkCrack.py -i hashes.txt 
  ``` 

## [SoftFuzz](softDirectory.py)

Some Webapps don't render http status code instead they render an error customized page which makes directory fuzzing challenging that's why this tool :

* Arguments 
  * -h : For help
  * -u URL : The Target URL
  * -w wordlist : The path of the wordlist of the attack (`/usr/share/wordlists/rockyou.txt` by default)
* Use Exemple : 
    ```bash
    python softDirectory.py -u $IP  
    ``` 

## [ExiftShell](./exiftshell/)

We'll use our reverse shell tool with HTTP or DNS exfiltration, which will enable us to obtain our first step on the target machine.
* Use exemple : 
  1. Open The Server with 
    ```bash
        python exiftshell.py
    ```
  2. Run the client on target
   > [Client Code](./exiftshell/client.sh)

<hr>

## Creds :

This work is crafted with &#x2764; and released as an open source . Feel free to remix, share, and build upon this work!