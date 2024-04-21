# Start

When we start up the challenge it prompts us to download the zip file, so let's download it and unzip it with the password

To complete this challenge we have to use Volatility, a python program that is dedicated to extracting information from RAM

Make sure to install it with pip 

# Question 1

Once we extract it we get a memory dump. So let's analyze it with Volatility with the following command: 

```
vol3 -f MemoryDump.mem windows.info
```

This will give information about the machine and what OS the memory dump came from

The first question on the challenge asks about suspicious processes on the memory dump. So let's do that with this command:

```
vol3 -f MemoryDump.mem windows.pstree | column -t
```

This will list the processes while also using the column command to format the output better:

{Insert image here}

To find processes that might be considered malware we can use this command:

```
vol3 -f MemoryDump.mem windows.malfind
```

There are two processes {something here} and oneetx.exe

In real analysis both processes would investigated, but since this a challenge the process **oneetx.exe** is the most suspicious 

# Question 2

The next question asks us what the child process of the suspicious process is. We can find the answer to that with the following command:

```
vol3 -f MemoryDump.mem windows.pstree | grep 5896
```

This command is the same command from earlier but we are going to grep for the specific PID number the our suspicious process is running with. 

After the command we find this: 

{Insert image here}