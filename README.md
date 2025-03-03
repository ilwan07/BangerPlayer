# BangerPlayer

#### A desktop music player app build with Python

---

![Interface Screenshot](https://cdn.hack.pet/U07E6R26ZC0/BangerPlayerScreenshot1.png)

---

## How to run

#### First way: Use the .exe compiled file (Windows only)

Go to the releases tab, and download the BangerPlayer.exe file, this is the whole software in a single file. Save it somewhere, on your desktop for example, and execute it to launch the app.

#### Second way: Use the source code (Any platform)

Either clone the main branch of this repository, or download the source code from the releases tab, then uncompress and save it somewhere on your computer. If it's not already the case, download python (reasonably recent version, this has been developped on Python 3.13.1)

Then, open a terminal in the folder you just saved, make sure it's set in this directory, and run `python3 -m venv .venv`, then run `.venv\Scripts\Activate` on Windows, or `source .venv/bin/activate` on Linux and MacOS to enter the venv. Finally, install the dependencies from the given file by running `pip3 install -r requirements.txt`. Now, you'll be able to run the app when in the venv by using `python3 project/main.pyw`.

---

## How to use

Simply open the app, and add use the button at the top to add your music folders. Then, select the folder you want to play the musics from by clicking it on the list. To remove a folder, simply click the cross on the right of the folder item.

After opening a folder, there is multiple buttons at the bottom. From left to right:

#### Global play button: Use this button to play/pause the music, this will select one if it's not already the case.

#### Loop mode:

- No loop (crossed out icon): Will play the music once, then stop.
- Play everything once (default, loop with down arrow): Will play every music once, in a relevant order.
- Play one on repeat (loop with a "1" inside): Will play the selected music on repeat.
- Repeat forever (loop icon): Will play every music indefinitely

#### Shuffle: If enabled, will play the musics in a random order (relevant only for the "play everything once" and repeat forever" loop modes), else the musics will play in order as defined by the loop mode.

#### Autoplay: If enabled, will automatically start playing a music when selected.

#### Sorting:

There are 3 sorting modes, each with ascending or descending order:

- Sort by title: Sorts the musics alphabetically from their title.
- Sort by author: Sorts the music alphabetically by author, with the musics without author at the bottom (will sort by title when the author is identical).
- Sort by time: Sorts the musics by their lenght, from the shortest to the longest, or the opposite.



When a music is selected, a panel will open on the right. You can click the play/pause button or press the space key to control the music. You can also click the progress bar to jump to a specified music time.

In this panel, you can set different music metadata, wich are the music title (different from the file name), the music author(s), and a cover art image. These data pieces are stored in the music file itself, which means that after modifying them from this app, you'll be able to see them from other softwares such as VLC Media Player too, or see the cover art as the file thumbnail for example.
