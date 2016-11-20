# midiget
Midiget allows you to crawl the pages of a website recursively and easily to download all hosted midi files. The programme is ideal to automate file retrieving from large midi repositories like www.vgmusic.com and www.midiworld.com  

# Usage
Launch midiget from the command line specifying the url of the target website from which you want to download the files: 
```
python midiget http://www.vgmusic.com/
```
You must be in the midiget directory when launching the program. In the example above, midiget starts crawling the pages of vgmusic.com in search for midi files. 

When launching the program, it is also possible to input a second (numerical) argument in order to specify the maximum number of pages midiget will visit before halting:
```
python midiget http://www.vgmusic.com/ 1000
```
If the second argument is not provided, the maximum number of pages is defaulted to 1000.

The files downloaded are saved in a directory called 'midisaves', placed in the root directory of the programme.

# Installation
Download midiget and unzip it. If you're on a linux machine, you can use the following command -- granted you have unzip installed:
```
unzip midiget-master.zip
```

# Dependencies
You need to have beautifulsoup4 installed in order to run midiget. To install beautifulsoup4, run this code from the command line:
```
$ pip install beautifulsoup4
```
