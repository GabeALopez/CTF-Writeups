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








