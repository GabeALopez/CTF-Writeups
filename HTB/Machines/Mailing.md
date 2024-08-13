# TL;DR

1. Ran Nmap and showed a few ports open for a website, mailing service, and smb
2. Enumerated some on the mailing service ports
3. Went to the website and started enumerating it
4. Found LFI vuln with the download button on the main webpage
5. Found the hmailserver.ini file through the LFI and grabbed the MD5 password hash
6. Cracked password with hashcat and looked for a vuln related to the mail server 
7. Found a vuln for CVE-2024-21413 and used POC to send a malicious payload to the maya bot user
8. Retrieved the NTLM hash of the maya user and cracked it
9. Then used the username and password to access the user shell with EvilWinRm
10. Looked around and found a vulnerable LibreOffice in the program files with CVE CVE-2023-2255
11. Found that the vuln is an RCE vuln and found a POC that create a malicious ODT file that executed this command: ```net localgroup Administradores maya /add```
12. I created the ODT with the POC and executed the file in the "Important Documents" folder where then the ODT was clicked on by bot user
13. Now with the maya user as admin I had then got the SAM hashes from crackmapexec
14. I then used used wmiexec from impacket with the maya user's SAM hash and then I went to cat the root flag