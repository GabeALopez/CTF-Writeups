# Discovery

The challenge starts with this web page:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Secured-Session/webPage.png)

Upon combing through the code there is a route "/flag" that seems accessible. So let navigate to it:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Secured-Session/incorrectKey.png)

There doesn't seem to be anything at the page. The challenge references a secured session so let's try to open inspect element and see if we have any cookies.

Lo and behold there is a cookie called session but it is in a different for than usual:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Secured-Session/inspectElement.png)

# Solving the Challenge

The format itself looks like it is in base64 so let decode it with this linux one liner:

```
echo "eyJmbGFnIjp7IiBiIjoiTWpRM1ExUkdlMlJoT0RBM09UVm1PR0UxWTJGaU1tVXdNemRrTnpNNE5UZ3dOMkk1WVRreGZRPT0ifX0.Zhhxlw.AxH8wu13LSUufsZk7LPXWKWekeo" | base64 -d
```

after running the command we get:

```
{"flag":{" b":"MjQ3Q1RGe2RhODA3OTVmOGE1Y2FiMmUwMzdkNzM4NTgwN2I5YTkxfQ=="}}
```

The value inside the json looks familiar. 

So let's decode once again with this one liner:

```
echo "MjQ3Q1RGe2RhODA3OTVmOGE1Y2FiMmUwMzdkNzM4NTgwN2I5YTkxfQ==" | base64 -d
```

After this we get the flag:

![alt text](https://github.com/GabeALopez/CTF-Writeups/blob/main/Images/247CTF/Secured-Session/flag.png)

