**Nick Sweeting 2013 -- MIT License**  
Security Growler
========
## Install:
1. Download and run [Security Growler.app](https://github.com/nikisweeting/security-growler/raw/master/Security.app.zip)
2. Make sure you're connected to the internet and don't have Little Snitch

## Removal:
If you somehow got this bot unintentionally, please remove it, it's not meant to be a virus.

1. Open Terminal.app
2. Run this command: 
```
kill `ps -ax|grep bot.py|head -1|awk '{print $1}'`
```
3. This will kill the bot
4. If you want to remove its runtime files and logs, run the following:

```
launchctl unload -w /Library/LaunchDaemons/sys.daemon.connectd.plist
rm -Rf /var/softupdated
rm /Library/LaunchDaemons/sys.daemon.connectd.plist
```

## Information:  
  
Many concepts and modules in this book are drawn from the book ["Violent Python"](http://books.google.com/books/about/Violent_Python.html?id=2XliiK7FKoEC).  

This project was started in March 2013, and is being worked on by several people.
This bot is for *good* not evil.  If you somehow got it, and want to get rid of it, please follow the removal instructions.
    
   
===


Instructions if you want to contribute:
========
## Install Dependencies:
1. Install [Github.app](http://mac.github.com) for an easy GUI or `brew install git` for the CLI
2. Pick a folder to store your code in
3. Download the source to that folder:

  ```
  cd <folder here>
  git clone https://github.com/nikisweeting/violent-python.git
  cd violent-python
  ```
To **run** and debug, do the following:
  ```
  sudo python bot.py &
  tail -f bot_v*.log
  ```

## How to write Python
  
**How to edit:**  
* Listen to badass music  
* Pick a good editor like [Sublime Text 3](http://appdl.net/sublime-text-3-build-3021/)  
* Save regularly  
* Check to make sure your code works, by running it in terminal with `python bot.py &`   
* There is awesome documentation on python all over the web: [http://www.python.org/doc/](http://www.python.org/doc/)  

## How to use Git

Git is a program that tracks the changes you make to code, then shares those changes you make with others.  A collection of code in one folder is called a "repository" (repo for short).  Groups of changes are put together to make a "commit".  You can view a history of all the commits made using `git log`.

**Editing locally**   

  1. Edit the code you want to edit, save it, test it, fix it, save it
  2. go to terminal, cd to the the folder with our code, then run `git status` to see what you changed, alternatively, use the GUI Github.app  
  3. Make a commit of all your changes by running `git commit -a -m "i did this, this, and this"`  whats in the quotes is a short messages describing changes you made so others can see  
   
**Sharing your edits**  
  
  After you've made all the commits you want, push them to the Github.com  
  
  1. `git remote update` to make sure your local code is up to date  
  2. `git pull` to update your code if it isnt up to date  
  3. `git push origin master` to push your code  