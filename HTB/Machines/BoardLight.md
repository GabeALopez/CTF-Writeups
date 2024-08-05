# TL;DR

1. Did nmap scan and found two ports open: port 22 and port 80
2. Went to the site and combed around to find nothing since it was a static site
3. Saw an email with board.htb and used that as a domain
4. Did a subdomain bruteforce and found crm.board.htb
5. Put in admin, admin as the creds and got in
6. looked for exploit for Dolibarr and found one that gave a reverse shell
7. Got the reverse shell, looked for config files, and found credentials for the user on the SSH service
8. Logged in and got the user flag
9. Enumerated user with linpeas
10. Further enumerated the box with find / -perm -4000 2>/dev/null to find any unusual SUIDs files
11. Saw a strange SUID file called ```enlightenment_sys``` and looked up a vulnerability for it 
12. Found exploit at ```https://github.com/MaherAzzouzi/CVE-2022-37706-LPE-exploit/tree/main```
13. Ran the shell script that the github page and got root shell

# Detailed Writeup

I first ran an nmap scan against the IP address and found the following results:

```
# Nmap 7.94SVN scan initiated Sun Aug  4 12:11:36 2024 as: nmap -vv -sVC -p- --min-rate=10000 -oA nmap/BoardLight 10.10.11.11
Nmap scan report for 10.10.11.11
Host is up, received conn-refused (0.10s latency).
Scanned at 2024-08-04 12:11:36 EDT for 23s
Not shown: 64514 filtered tcp ports (no-response), 1019 closed tcp ports (conn-refused)
PORT   STATE SERVICE REASON  VERSION
22/tcp open  ssh     syn-ack OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 06:2d:3b:85:10:59:ff:73:66:27:7f:0e:ae:03:ea:f4 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDH0dV4gtJNo8ixEEBDxhUId6Pc/8iNLX16+zpUCIgmxxl5TivDMLg2JvXorp4F2r8ci44CESUlnMHRSYNtlLttiIZHpTML7ktFHbNexvOAJqE1lIlQlGjWBU1hWq6Y6n1tuUANOd5U+Yc0/h53gKu5nXTQTy1c9CLbQfaYvFjnzrR3NQ6Hw7ih5u3mEjJngP+Sq+dpzUcnFe1BekvBPrxdAJwN6w+MSpGFyQSAkUthrOE4JRnpa6jSsTjXODDjioNkp2NLkKa73Yc2DHk3evNUXfa+P8oWFBk8ZXSHFyeOoNkcqkPCrkevB71NdFtn3Fd/Ar07co0ygw90Vb2q34cu1Jo/1oPV1UFsvcwaKJuxBKozH+VA0F9hyriPKjsvTRCbkFjweLxCib5phagHu6K5KEYC+VmWbCUnWyvYZauJ1/t5xQqqi9UWssRjbE1mI0Krq2Zb97qnONhzcclAPVpvEVdCCcl0rYZjQt6VI1PzHha56JepZCFCNvX3FVxYzEk=
|   256 59:03:dc:52:87:3a:35:99:34:44:74:33:78:31:35:fb (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBK7G5PgPkbp1awVqM5uOpMJ/xVrNirmwIT21bMG/+jihUY8rOXxSbidRfC9KgvSDC4flMsPZUrWziSuBDJAra5g=
|   256 ab:13:38:e4:3e:e0:24:b4:69:38:a9:63:82:38:dd:f4 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILHj/lr3X40pR3k9+uYJk4oSjdULCK0DlOxbiL66ZRWg
80/tcp open  http    syn-ack Apache httpd 2.4.41 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun Aug  4 12:11:59 2024 -- 1 IP address (1 host up) scanned in 23.29 seconds
```

Seeing that there only two ports open, I had went to the website. The homepage looked liked this:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/Machines/BoardLight/)

I started looking around and testing the contact forms to see if there any requests being sent from them. I didn't find anything and decided to try bruteforcing directories. I had noticed that pages were php pages and so I tried to bruteforce with that in mind using the following command:

```bash
ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-words.txt -u 'http://<IP address here>/FUZZ.php
```

I didn't get much so I tried to try looking for any domains on the site to try to include in the /etc/hosts file for subdomain bruteforcing

I ended up finding the email domain board.htb and added that to the hosts file

After that I tried bruteforcing for subdomains with the following command:

```bash
ffuf -w /usr/share/wordlists/seclists/DNS/subdomains-top1million-5000.txt -u 'http://board.htb' -H 'HOST: FUZZ.board.htb'
```

I ended up finding one subdomain called crm.board.htb and navigated to it:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/Machines/BoardLight/)

Finding the CRM is Dolibarr 17.0, I had looked up a vulnerablity for it and found this github page: ```https://github.com/nikn0laty/Exploit-for-Dolibarr-17.0.0-CVE-2023-30253```

The vulnerablity works if you have authenticated access to the site. So I tried some default creds with admin, admin and I got in. Once I did that, I ran the exploit script and got a reverse shell:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/Machines/BoardLight/)

I started looking for config files and found one this path: ```/var/www/html/crm.board.htb/htdocs/conf/conf.php``` where it had contained a password for the database. I used the pass for the larissa user on the box and got the user shell. After this, I started doing some enumeration with linpeas, and some manual enumeration with these commmands: ```sudo -l``` and ```find / -perm -4000 2>/dev/null```

From this enumeration, I found a strang SUID file called ```enlightenment_sys``` and looked up a vulnerability for it. After some searching, I landed on this github page: ```https://github.com/MaherAzzouzi/CVE-2022-37706-LPE-exploit/tree/main``` which has the POC as well as how it works.

After running it, I had gotten the root shell

