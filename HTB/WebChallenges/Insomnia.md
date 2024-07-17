# TL;DR

1. Registered an account and tried to decode the JWT token
2. Tried to change the name in the token: did not work
3. Looked at the source code and saw that the server is looking for the Administrator account
4. Saw that the login logic did not throw error for not having two inputs
5. Passed the json data with just the Administrator as the data
6. Copied and pasted the token in the browser cache, accessed the profile page, and got the flag

# Detailed Writeup

When first opening up the website we see this page:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/Insomnia/homepage.png)

I tried clicking on the "Let Start" and "exit" buttons but found that these do not do anything. The links that do work are the titles at the top: "HOME", "SIGNIN", and "SIGNUP".

Clicking on the "SIGNIN" lands on a login page. I tried a basic credentials like admin/admin, but did not get anything other than an alert from the site saying that the user did not exist. 

NOTE: After completing the challenge, I had thought to try to intercept the request and try to bruteforce users that were available (Which that user can be seen in the source code). I found out that even with a right username but wrong password it would produce the same error regardless.

I tried a simple sql injection payload but did not get anything either.

So let's try to go to the "SIGNUP" page and register an account.

Once we register and login, it lands us on a profile page welcoming the user:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/Insomnia/login.png)

When looking at this request from ZAP, I noticed that there was a JWT token:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/Insomnia/usr-token.png)

I tried to base64 decode the token and found the basic info with a JWT token. After this, tried to change the user to admin and would later try administrator after looking at the source code, but this did not do anything.

## Now Let's Look at the Source Code

With all of these attempts done, I had decided to try to look at the given source code for the website. The files that caught my eye were entrypoint.sh, ProfileController.php, and UserController.php:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/Insomnia/ProfileController.png)
![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/Insomnia/entrypoint.png)
![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/Insomnia/UserController.png)

ProfileController.php was the first file to catch my eye at first as the logic of the code was checking for an administrator user in the JWT token. This had of course gave me the idea on trying to replace the username in the JWT token from earlier. I saw that the JWT token was getting the key from an environment.

After this, I thought look into the entrypoint.sh as it had the setup for the user and the JWT secret. I saw that the Admin's password and the JWT secret were randomly generated so those were not going to be bruteforced.

NOTE: I saw the JWT secret generation when skimming through the files

Last but not least, I had looked into the UserController.php file where I found something that was interesting in the logic. The logic itself seemed to check if the json input from the login form, was holding two values. The logic did not have logic to return an error when the json data was not holding two values. This meaning that one value can be passed in, in my case just a username that was equal to administrator, without any need for a password.

# Exploitation

Once I found this, I had made the request to login and intercepted the request with ZAP. I then changed the value of the json data and got a token for the admin: 

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/Insomnia/param-change.png)
![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/Insomnia/admin-token.png)

I then copied this token and replaced the token in the browser cache. I went to the profile page and got the flag:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/HTB/WebChallenges/Insomnia/flag.png)