# Pixel Jumper
My first game created in PyGame by myself from the beginning to the end.

## Content of project
* [General info](#general-info)
* [Technologies](#technologies)
* [Application view](#application-view)
* [Setup](#setup)
* [Functionalities](#functionalities)
* [Modifications](#modifications)
* [Inspiration & Sources](#inspiration--sources)
* [Contact](#contact)

## General info
Pixel Jumper is a simple platformer game created in PyGame. Our hero jumps on moving platforms as high as he can.
But it is not that easy! The higher he is, the faster he has to jump because the scrolling background is chasing him.
You can choose between 2 characters (Mr. and Mrs. Pixel).<br>
Do your best to jump to the top of the highscores list!

## Technologies
<ul>
<li>Python 3.10.5</li>
<li>PyGame 2.1.2</li>
</ul>

## Application view

<img src=https://user-images.githubusercontent.com/108935246/205730124-be9c0bcb-6e0b-49f8-968f-53d6082367ce.png width="30%">

<img src=https://user-images.githubusercontent.com/108935246/205730129-41806737-e711-4897-888b-cccf132b36c4.png width="30%">

<img src=https://user-images.githubusercontent.com/108935246/205730131-8fe7655b-0199-4f33-b62f-18e18f880963.png width="30%">

## Setup
To everything work properly you need to install PyGame on your machine.<br>
```commandline
python3 -m pip install -U pygame --user
```
If you have any problems with that look at the PyGame documentation:<br>
```
https://www.pygame.org/wiki/GettingStarted
```
Creating an executable file is easy and fun.<br>
<b>Firstly</b> you have to install pyinstaller:
```commandline
pip install pyinstaller
```
When it's done you can create en ```.exe``` using this command:
```commandline
pyinstaller --windowed --onefile main.py
```

New file is created in ```dist/``` folder. Last thing to do is copy ```graphics/```, ```sounds/```, ```fonts/``` and 
```highscores.json``` from working directory and paste them in  ```dist/```.<br>

### Now you can run the game and have fun!

## Functionalities

You start by selecting the player you want to play.<br><br>
To move player to the sides use arrows
<img src=https://user-images.githubusercontent.com/108935246/205730138-77a3d324-0119-41dd-9c5d-86168638a643.png width="5%">.
and
<img src=https://user-images.githubusercontent.com/108935246/205730136-06777c0c-96c0-45ac-bcd0-91b1d5b96464.png width="5%">
<br><br>
Press 
<img src=https://user-images.githubusercontent.com/108935246/205730141-72ca9954-5f7d-4da5-b7b2-c37c60a13dba.png width="25%">
or 
<img src=https://user-images.githubusercontent.com/108935246/205730142-a2c61c97-d156-48f6-a0c9-c7d7f95d968f.png width="5%">
to jump.<br><br>
To restart press 
<img src=https://user-images.githubusercontent.com/108935246/205730145-04768a9c-cc7b-4c2b-b65f-57233933ca84.png width="5%">

## Modifications
You can customize my game to your requirements

##### Graphics
To change player images just replace graphics in ```graphics/player``` or ```graphics/player_pink```.
The size doesn't really matter, because in Player Class imported images are scaled to 60x60 pixels.
And remember to save it in ```.png``` with transparent background.<br>
Similarly, you can replace a background image or platforms images.

##### Music
If you want change background music or jump sound just replace them in ```sounds/``` folder

##### Game options
To change jump power just edit in ```player.py``` 
```commandline
self.jump_speed = Your_Value
```
You can do the same with other values like:
<ul>
<li>player speed</li>
<li>player gravity</li>
</ul>

## Inspiration & Sources
<p>My wife is a huge fan of Mario and Icy Tower so when I told her that I'm going to learn to make game in Python,
my plans to make some RPG had to be modified. So this is my version of Icy Tower named <b>Pixel Jumper!</b> </p>

<p>The subject of PyGame is so extensive that I must have spent many hours with different tutorials to make such 
a simple game like that. I would love make much more complicated game in future because it's really fascinating, but 
there is so many other things to learn, I just have not enough time to sacrifice a weeks or even months to make a 
semi-professional game. Especially with my basic level. But maybe some day..</p>

Making this game wouldn't be possible without some excellent tutorials:<br>
&emsp;&emsp;<i>The ultimate introduction to Pygame</i> by ```Clear Code``` on <strong>YouTube</strong><br>
&emsp;&emsp;The Pygame series by ```Coding With Russ``` on <strong>YouTube</strong><br>
&emsp;&emsp;A good documentation of a ```PyGame``` was also helpfully.

Graphics was downloaded from [OpenGameArt.org](https://opengameart.org/). Don't ask for a specific author.. I took every
image from another account, and I couldn't find it again.

## Contact
If you have any questions or ideas for development fell free to contact me via email:</br>
```maritn.brzezinski@wp.eu```

## Running in the Browser (Pygbag)

You can run Pixel Jumper in your browser using [Pygbag](https://github.com/pygame-web/pygbag):

1. Install pygbag:
   ```bash
   pip install pygbag
   ```
2. In your project directory, run:
   ```bash
   pygbag --build main.py
   ```
3. Open the generated `build/web/index.html` in your browser, or deploy the `build/web` folder to a static web host.

**Note:** Highscores are not available in browser mode due to browser file system limitations.
