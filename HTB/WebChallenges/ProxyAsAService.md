# TL;DR

1. Looked at the source code and found the url param could be manipulated
2. Found that the website has a debug page that holds the flags and can only be accessed via localhost
3. Tried appending an "@" and then an internal IP address
4. Found that it crashed the server and I looked back into the source code
5. Found that there is a blacklist blocking the input and that the debug page needs to be accessed on port 1337
6. Gave another IP address that represents localhost and port number with the debug directory, which produced the flag

# Detailed Writeup

When first opening up website it shows us this if you are not authenticated to reddit:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ProxyAsAService/homepage.png)

At first, I considered experimenting with the URL parameter, but then I opted to inspect the source code instead, to avoid blindly guessing what was going break the website.

I downloaded the zip file and looked at the routes.py and util.py files:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ProxyAsAService/routes.png)
![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ProxyAsAService/util.png)

The interesting part about the routes.py code were these pieces of code:

```
target_url = f'http://{SITE_NAME}{url}'
response, headers = proxy_req(target_url)
```

The "url" var is a var that is under user control. This being the case, I can put any value that I wanted that could potentially change the behavior of the website.

The main issue though is that the site appends "reddit.com" to the query string so we need an input that forces the website to go to another IP address. Luckily, book.hacktricks.xyz has a resource dedicated to "URL Format Bypasses". The page, has a portion of the URL format bypasses dedicated to "Domain Confusion" where input after a URL without any backslashes can be used to redirect to other malicious pages. The first example the page shows is this one here:

```
https://{domain}@attacker.com
```
If we read into the website source code a bit more, we see that there is a directory to the debug route that shows the environment variables. When looking into the other files for the website we see that the environment var (seen in the Dockerfile) for the site actually holds the flag, so we want to get to the "debug/environment" path. But according to the code, we can only access it via localhost. Luckily we found a way to do redirects, so we can try to redirect to localhost on the site and access the "debug/environment" path. So let's go ahead and do that:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ProxyAsAService/first-try.png)

Well it looks like that input isn't doing anything. Perhaps it is being blocked. So let's look into the source code once again, but this time let's look at the util.py file to see why. 

It looks like this python file shows that values that hold "localhost", "127.", "192.168.", "10.", or "172." are blocked so we need to use a value that represents localhost but does not fit this blacklist. Luckily, 0.0.0.0 is a known IP address the represents localhost. That being the case, we can try that and see if it works:

NOTE: If you do not know that 0.0.0.0 represents localhost you can go on google and search around. I ended up landing on a GeeksforGeeks page that explains about the localhost IP addresses.

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ProxyAsAService/second-try.png)

Welp, no environment vars. Let's look at some other files in the website project. I looked around and found the run.py file. I found out here that the site runs on port 1337:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ProxyAsAService/port.png)

So let's try again, but with the port:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/ProxyAsAService/flag.png)

Voilà, we have the flag.