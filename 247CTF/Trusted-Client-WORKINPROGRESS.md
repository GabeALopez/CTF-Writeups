# Discovery

When opening up the web page it first looks like this:

(Insert image here)

First attempts to be made were to try to login with default credentials. i.e.

- admin admin
- admin password
- admin letmein

An interesting observation was made. When putting in the credentials on the page an alert would pop up as seen below:

(Insert image here)

The fact that an alert was sent means that there might be some javascript (js) that is driving the login functionality. Thus opening inspect element we did:

(Insert image here)

Under the debugger tab and scrolling down a bit some js was discovered in an obfuscated format:

(Insert image here)

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

(Insert image here)

We can start to see that the symbols start to look like they are forming functions almost. This is a lot of symbols so lets take the first section of js that looks like a function:

(Insert Image here)

When we insert the js into the console we get this:

(Insert image here)

Alright next section:

(Insert image here)

Nothing yet: 

(Insert image here)

We keep going at this until we find the flag:

