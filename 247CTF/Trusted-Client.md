# Discovery

When opening up the web page it first looks like this:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Trusted-Client/webpage.png)

First attempts to be made were to try to login with default credentials. i.e.

- admin admin
- admin password
- admin letmein

An interesting observation was made. When putting in the credentials on the page an alert would pop up as seen below:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Trusted-Client/alert.png)

The fact that an alert was sent means that there might be some javascript (js) that is driving the login functionality. Thus opening inspect element we did:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Trusted-Client/inspectElement.png)

Under the debugger tab and scrolling down a bit some js was discovered in an obfuscated format:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Trusted-Client/javascript.png)

**Side note: Alternatively you can right click on the page and choose the "View page source" option to see the full HTML. You can also see the js embedded into the site this way too.**

# Deobfuscation

## Javascript Side Tangent

Javascript is a strange language and interpreted language, much like python. But what makes it different from python is the greater looseness that is has. This being the case, js can be a little strange when it comes to types and symbols. One such example is this one: 

```
console.log(1 == "1");
```

In js this will return true but in this example it will return false:

```
console.log(1 === "1");
```

Because of how loose the interpreter is, the return values that are produced can be quite different from just a simple change. This can be an issue with client side js as an attacker can change values in such a way that return values are drastically different. This can lead different types of attacks that come from the loose interpreter. 

A further example of this is the infamous banana output from this line of code: 

```
console.log(('b' + 'a' + + 'a' + 'a').toLowerCase())
```

For more information as why this is the case here is an article that explains: https://razvan-cirlugea.medium.com/js-banana-meme-explained-527696d27767

--End of Side Tangent--

TL;DR: Javascript is a loose language and can be exploited because of that looseness.

## Back to the Challenge

What does this tangent have to with the the challenge? Well the long set of symbols we see in the page source are actually js symbols that mean something. Just by themselves they don't mean anything but once we start picking the line apart we can start to see more information.

So lets start copying the long line and pasting it into a js beautifier to get a better look:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Trusted-Client/beautifiedJavascript.png)

We can start to see that the symbols start to look like they are forming functions almost. This is a lot of symbols so lets take the first section of js that looks like a function:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Trusted-Client/firstSectionCodeJs.png)

When we insert the js into the console we get this:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Trusted-Client/firstSectionJs.png)

Alright next section:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Trusted-Client/nextSectionCodJs.png)

Nothing yet: 

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Trusted-Client/nextSectionJs.png)

We keep going at this until we find the flag:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Trusted-Client/flag.png)

# Afterthoughts

- After looking at another write up for this challenge, (This one here: https://b4d.sablun.org/blog/2020-03-22-247ctf-com-web-trusted-client) I had come to find out that the challenge was using a way of writing js called JSFUCK. At first I did recognize that js could written in the way that JSFUCK has but didn't know the name of it. 
    - Furthermore, from the writeup I did find a website that deobfuscates JSFUCK but in my case I had issues due to putting too much of the obfuscated js
        - Here is the site: https://enkhee-osiris.github.io/Decoder-JSFuck/
- A very useful deobfuscator that I had used to help structure the js better was this one here: https://deobfuscate.relative.im/

