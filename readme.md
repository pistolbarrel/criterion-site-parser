# criterion-site-parser
Parses criterion channel site for movie information. Also was an exercise to package 
and publish a module on PyPi.

This is where it all started. I just wanted to be able to track movies I wanted to see.
I also wanted to be able to have this data in a form I could copy/paste into 
[MediaMonkey](https://www.mediamonkey.com/). It was a hassle to copy/paste from the
web. For a long time, generating text files for the various collections that the 
[Criterion Channel](https://www.criterionchannel.com/) was good enough. I also used grep
to find movies in more than one list, check if they were going away soon, etc.

I was looking to learn some other technology and therefore created a database with a web
frontend that was implemented with some web services. That can all be found in 
[moviedbweb](https://github.com/pistolbarrel/moviedbweb).

You can install this module from [pypi](https://pypi.org/project/criterion-site-parser/).

## Usage

Basic usage is pretty simple once the module is installed.
> python -m critparse -h
usage: __main__.py [-h] [-n] [-a] [-s] [-q] url
>
> This is how you use this thing
>
>positional arguments:
>  url                  URL to parse
>
>optional arguments:
> 
>  -h, --help           show this help message and exit<br>
  -n, --noprint        Suppress printing the movie info<br>
  -a, --api            Add movie via REST api<br>
  -s, --skipdiscovery  Skip the discovery of collections<br>
  -q, --quiet          Suppress the printing of the title of each movie as it is added via api

## Sample Output

python -m critparse https://www.criterionchannel.com/60s-hitchcock

url has been determined to be: None

Discovering collections ...

Examined https://www.criterionchannel.com/60s-hitchcock
++++++++++++++++++++++++++++++++++++++++++++++++++++++<br>
Criterion:’60s Hitchcock<br>
By the 1960s, with multiple masterpieces already to his name, Alfred Hitchcock kept on innovating, pushing the boundaries of on-screen violence and harnessing his technical mastery to create commercial entertainment that doubled as a v
ehicle to explore his darkest and most personal obsessions. The shocking modernism of PSYCHO, the unfathomable existential terror of THE BIRDS, and the perverse psychological mystery of MARNIE—each is among the Master of Suspense’s mos
t stylistically and thematically complex films and a key to understanding his career-long fascination with the links between sex, violence, guilt, and voyeurism.<br>
++++++++++++++++++++++++++++++++++++++++++++++++++++++<br>


======================================================<br>
1<br>
1:59:34<br>
Criterion:’60s Hitchcock<br>
https://www.criterionchannel.com/60s-hitchcock/season:1/videos/the-birds <br>
Birds, The (1963)<br>
Alfred Hitchcock<br>
United States<br>
Tippi Hedren; Rod Taylor; Jessica Tandy<br>
<br>
A powerful, terrifying study of paranoia and hysteria in the wake of unexplained chaos, THE BIRDS is one of Alfred Hitchcock’s most singular and unforgettable films. It all begins rather innocuously, as a mischievous San Francisco soci
alite (Tippi Hedren) travels to the coastal town of Bodega Bay to hook up with a rugged lawyer (Rod Taylor) she’s only just met. Once there, however, bizarre things start happening. The birds, you see, are behaving strangely. With impr
essive special effects and innovative electronic sound design, Hitchcock delivers some of the most harrowing set pieces of his career.<br>
======================================================<br>


======================================================

... (trimmed - would contain similar info for Psycho and Marnie)

======================================================


egrep "^Birds, The \([1,2,N]" *<br>
egrep "^Psycho \([1,2,N]" *<br>
egrep "^Marnie \([1,2,N]" *<br>


Birds, The (1963); Psycho (1960); Marnie (1964)<br>
Criterion:’60s Hitchcock<br>

