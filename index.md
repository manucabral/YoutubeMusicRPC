<p align="center">
<img src="https://github.com/manucabral/YoutubeMusicRPC/blob/main/assets/logo.png?raw=true" width="250" title="example">
<img src="https://github.com/manucabral/YoutubeMusicRPC/blob/main/assets/app.png?raw=true" title="app">
<img src="https://github.com/manucabral/YoutubeMusicRPC/blob/main/assets/listening.png?raw=true" width="250" title="listening">
<img src="https://github.com/manucabral/YouTubeMusicRPC/blob/main/assets/pause.png?raw=true" width="250" title="pause">
<img src="https://github.com/manucabral/YouTubeMusicRPC/blob/main/assets/browser.png?raw=true" width="250" title="browser">
</p>

<p align="center">
   A YouTube Music Rich Presence app client that show what you're listening client made with ❤️.
</p>
<p align="center">
   Note: This is not an official app made by YouTube Music or Google.
</p>

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ⏬ Download
The lastest release is available [here](https://github.com/manucabral/YoutubeMusicRPC/releases)

## 🗒️ Supported browsers
- Google Chrome
- Yandex Browser
- Microsoft Edge

If you want a support for another browser, please make an [issue](https://github.com/manucabral/YoutubeMusicRPC/issues).


## :grey_question: How does that work
The application opens your browser with remote debugging enable (Chrome Dev Tools) to access all Youtube Music tabs, once this is done the app executes a script to obtain all the data throught [MediaSession](https://developer.mozilla.org/en-US/docs/Web/API/MediaSession) and finally create a Rich Presence for Discord.

## 🔨 Troubleshooting
- My rich presence client is not displaying?
  - Try
    - Go to your User Settings > Activity Status > Display current activity as a status message and make sure it's enabled.
    - Close the app and wait a few seconds, then open it again.
- Do I need Discord open on my pc to use this app?
    - Yes, you need to open Discord to run the app.
- The app crashes on start
    - Try
        - Close all browser instances and run it again.
        - If you've Youtube Music Desktop Application close it too.
          - I recommended to close instances from the task manager.
        - Restart discord and open it again.
    - If the problem persist please make an issue and adjunt your __client.log__ file.
     

Credits to [pypresence](https://github.com/qwertyquerty/pypresence)

## ✨ Contributing
All contributions, bug reports, fixes, enhancements, and ideas are welcome. Just make a pull request or a issue!

