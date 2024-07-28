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
