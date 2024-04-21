# Start

When opening up the challenge the following web page is shown:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Compare-The-Pair/mainPage.png)

It is some php code of how the web page works on the background. The code is seems to vulnerable with the conditional.

To start with, the password hash variable holds a special string. The string starts with 0e followed by numbers. 

## PHP Weirdness 

The strange thing about PHP is that it interprets some certain types of strings strangely. Not only that PHP has in conditionals, what is called type juggling. Type juggling means that two inputs can interpreted differently. Here is an example:

```
if("1" == 1){
    return true;
}

```
In the example above, since PHP has type juggling this example will return true. The "==" operator is more loose than the "===" operator in PHP, thus the statement returns true.

# Back to the Challenge

In the case of the challenge, the password hash variable that has the 0e is interpreted as 0 in conditionals. So what does this mean in the challenge? This means that we can pass in a specific string using our own input that would make the condition true. When that happens it will return the flag

When we pass in the value it will hash the value using an md5 hash. So we need to find a value that when md5 hashed, wll return a hash that starts with 0e

So let's create a python a script that will find this:

```
import hashlib
import itertools

#Code adapted from: https://github.com/hehacks/Hacking_Notes_obsidian/blob/master/labs/web/247ctf.md

salt = "f789bbc328a3d1a3"

for number in itertools.count():
    # Concatenate salt and password
    salted_password = salt + str(number)

    # Compute MD5 hash
    hashed_password = hashlib.md5(salted_password.encode()).hexdigest()

    if(hashed_password[:2] == '0e' and hashed_password[2:].isnumeric()):
        print("Number: " + str(number) + " Hash: " + hashed_password + " Number length: "  + str(len(str(number))))
        break
    else:
        continue
```

After sitting for a while, we get the number 237701818

When we pass it in with "/?password=237701818" we get the flag:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Compare-The-Pair/flag.png)
