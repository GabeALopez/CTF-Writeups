# TL;DR

1. Clicked on button for a clicker game that prompted to get the flag
2. Saw in ZAP that the response gave back: "This game is currently available only from dev.apacheblaze.local."
3. I looked back at the source code and found that the X-Forwarded-Host needed to have "dev.apacheblaze.local" but the response did not change when added it in the request
4. I looked back at the httpd.conf file this time and saw that there were two V-hosts and tried to look into http smuggling POCs
5. POC didn't do anything and thus looked into the proxy modules that were in the httpd.conf file which turned up a http smuggling POC for the Apache proxy modules
6. I then changed the POC request to fit the challenge and I got back the flag

# Detailed Writeup

When first starting up the site we get this page:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ApacheBlaze/homepage.png)

Opening up ZAP and I started with clicking on all the buttons that were available. There a button that prompted to click on it for the flag, but I wanted to click the others one just in case I miss anything. 

But needless to say the other buttons did not have meaningful change accept for the button was under the label "Game 4". The response says that the clicker game is only available from the dev.apacheblaze.local host. 

This being the case, I had started to look at the source code. The two files that caught my attention were app.py and httpd.conf:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ApacheBlaze/app.png)
![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ApacheBlaze/conf-file.png)

Starting with the app.py we see that in that file whenever we send the "click_topia" text in the GET request and set the X-Forwarded-Host to dev.apacheblaze.local we should get the flag. So let's try it here:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ApacheBlaze/initial-try.png)

Nothing. That's strange. Lets look back at the project code. This is where the httpd.conf file had caught my attention. When I looked at it, I found that Apache was using a reverse proxy and a load balancer through Apache modules. This being the case, the thing that came to mind was an http smuggling request as there are two virtual hosts being used at the same time and that maybe these two v-hosts were processing the user request differently. I had tried some payloads like this one from hacktricks:

```
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 30
Connection: keep-alive
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
Foo: x
```

But I still didn't get anything different back from the response. I tried with an X-Forwarded-Host header and just a Host header, but still nothing. So I tried to go back to the conf file to see if there was anything else to glean from it. I saw again that Apache was using the proxy module, so I thought to try to look up information google about http smuggling and the proxy modules in Apache

This search term came up autocorrected after searching it: apache 2.4.55 mod_proxy http request smuggling and google gave me a link to a POC: https://github.com/dhmosfunk/CVE-2023-25690-POC

The POC that the Github page showed was this:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ApacheBlaze/github.png)

So I altered it and tried to send in this GET request and I got the flag:

```
GET http://<IP address>:<Port>/api/games/click_topia%20HTTP/1.1%0d%0aHost:%20dev.apacheblaze.local%0d%0a%0d%0aGET%20/ HTTP/1.1
host: <IP address>:<Port>
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Referer: http://<IP address>:<Port>/
X-Requested-With: XMLHttpRequest
Connection: keep-alive
content-length: 0
```

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ApacheBlaze/flag.png)