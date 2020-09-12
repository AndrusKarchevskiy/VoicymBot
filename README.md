# VoicymBot

**Description:**

It's VK Bot that create fan audio messages, recognize audio and text, uses Google speech recognition technologies. *Now, works only on russian language*.

**Base Stack:** 

Python3.8.5, vkwave-new async vk-api framework. 

All used modules and libs you can check in project or at requirements.txt

**Installation:** 

1) *git clone https://github.com/AndrusKarchevskiy/VoicymBot* 

2) *pip install -r requirements.txt*

3) Create *.env* file in root directory of project. 

4) In *.env* create 2 main variables: 

`BOT_TOKEN` -- get it in your VK-group

`GROUP_ID` -- get it in your VK-group

5) Install ESpeak:

On Linux (Unix): `apt-get install espeak` 

On Windows: 

5.1) Install .exe file: http://espeak.sourceforge.net/download.html

5.2) Add *your_path_to_eSpeak\eSpeak\command_line\espeak.exe to PATH*

6) Install ffmpeg plugin:

On Linux (Unix): `apt-get install ffmpeg`

On Windows: 

follow the instructions: http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

**Links**

Bot in the internal VK' search: Войсим Бот.

Bot's Link in browser: https://vk.com/Voicym.

Link on Github: https://github.com/AndrusKarchevskiy/VoicymBot.
