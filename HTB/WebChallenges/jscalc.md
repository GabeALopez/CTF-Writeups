# TL;DR

1. Saw that special input had caused a difference in behavior
2. Looked into the source code that was given and found that the logic that handled the calculation
3. Saw that the logic was using eval() dangerously
4. Looked around online for payloads to read file on server
5. Found a payload that worked and was able to execute commands on the server
6. "Cated" the flag.txt

# Detailed Writeup

When first running the website and browsing to it we see this page: 

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/jscalc/website.png)



We first hit the calculate button and it returns the value from the values that already put into the form:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/jscalc/calculate.png)

We can first try to put in some special characters like single or doubles quotes. We end up getting a blank error alert which is interesting:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/jscalc/special-character.png)

If you wanted you could fuzz for this parameter with a tool like FUFF or with burp/Zap's fuzzers. But at this point I had started to look at the source code that the was given with this challenge.

I had unzipped it and look at the directory with VS Code. The two files that caught my eye the first was the index.js and more specifically the logic that handles passing the form data into a calculate function. The second, was calculatorHelper.js which contained the logic that handles the calculation:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/jscalc/index-js-file.png)

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/jscalc/calculatorHelper-js-file.png)

When examining the code for calculatorHelper.js we see a function that JavaScript (JS) uses that is known to be dangerous. Along with an anonymous function inside the eval statement.

I get into why the function is dangerous to use in the following header

## Why is eval() Dangerous?

The short and sweet of it is that eval() can lead to at lot of injection attacks. 

In the following simple sample code, one can execute arbitrary code because of the eval statement:

```
malicious_input = "alert(1)"

eval(malicious_input)
```

When ran in a console, you will notice that an alert had popped up on the browser. Now this does mean much when just looking at the sample code. Now when you put this in the context of some kind of user input, let's say a login form on Amazon website, on the back end of that website it can be seen as dangerous. An attacker can use this to try to get a shell on the server and gain an initial access to Amazon website.

# Getting Back to the CTF

Now that we know that is part of the logic is dangerous, we need to figure out the payload to try to read files on the system. 

After some searching around on the internet for a JS payload that executes commands and some testing I had arrived at the following payload:

```
(() => { return require('child_process').execSync('ls /'); })()
```

This payload had produced this result from the server:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/jscalc/bytes.png)

I used ChatGPT to write up a quick python script to decode the bytes from a file:

```
def decode_decimal_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read().strip()
            decimal_values = data.split(',')
            decoded_text = ''.join(chr(int(value)) for value in decimal_values)
            return decoded_text
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

# Example usage:
file_path = 'bufferData.txt'  # Replace with your actual file path
decoded_text = decode_decimal_data(file_path)

if decoded_text:
    print("Decoded data:")
    print(decoded_text)

```

And the code produced the following result after copying the bytes into a text file:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/jscalc/read-bytes.png)

Ok this is good, now we can read files on the server. 

After this, I "cated" out the flag.txt at the root directory, copied the bytes into the file, and ran the script to get the flag.

