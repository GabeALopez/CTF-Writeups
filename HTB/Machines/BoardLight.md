# TL;DR

1. Did nmap scan and found two ports open: port 22 and port 80
2. Went to the site and combed around to find nothing since it was a static site
3. Saw an email with board.htb and used that as a domain
4. Did a subdomain bruteforce and found crm.board.htb
5. Put in admin, admin as the creds and got in
6. looked for exploit for Dolibarr and found one that gave a reverse shell
7. Got the reverse shell, looked for config files, and found credentials for the user on the SSH service
8. Logged in and got the user flag
9. Enumerated user with linpeas, tried dirty cow exploit, and failed
10. Saw an exploit script that was in the home directory of the user to get root access? CVE-2022-37706 Check back later to make sure
find / -perm -4000 2>/dev/null