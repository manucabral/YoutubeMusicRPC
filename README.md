<p align="center">
<img src="https://github.com/manucabral/YoutubeMusicRPC/blob/main/assets/logo.png?raw=true" width="250" title="example">
<img src="https://github.com/manucabral/YoutubeMusicRPC/blob/main/assets/app.png?raw=true" title="app">
<img src="https://github.com/manucabral/YoutubeMusicRPC/blob/main/assets/listening.png?raw=true" width="400" title="listening">
<img src="https://github.com/manucabral/YouTubeMusicRPC/blob/main/assets/pause.png?raw=true" width="400" title="pause">
<img src="https://github.com/manucabral/YouTubeMusicRPC/blob/main/assets/browser.png?raw=true" width="400" title="browser">
</p>

<p align="center">
A YouTube Music Rich Presence app client that shows what you're listening to, made with ❤️.
</p>

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ⏬ Download
The lastest release is available [here](https://github.com/manucabral/YoutubeMusicRPC/releases)

## 🗒️ Supported browsers
- Google Chrome
- Yandex Browser
- Microsoft Edge
- Opera (Normal, One and GX)

If you want support for another browser, please create an [issue](https://github.com/manucabral/YoutubeMusicRPC/issues).

## 📝Notes
- Currently only compatible with Microsoft Windows systems.

## :grey_question: How does that work
The application opens your browser with remote debugging enabled (Chrome Dev Tools) to access all YouTube Music tabs. Once this is done, the app executes a script to obtain all the data through [MediaSession](https://developer.mozilla.org/en-US/docs/Web/API/MediaSession) and finally creates a Rich Presence for Discord.

## 🔨 Troubleshooting
- My Rich Presence client is not displaying.
  - Try the following:
    - Go to your User Settings > Activity Status > Display current activity as a status message and make sure it's enabled.
    - Close the app and wait a few seconds, then open it again.
- Do I need Discord open on my PC to use this app?
  - Yes, you need to have Discord open to run the app.
- The app crashes on startup.
  - Try the following:
    - Close all browser instances and run it again.
    - If you have the YouTube Music Desktop Application open, close it as well. I recommend closing instances from the task manager.
    - Restart Discord and try opening the app again.
  - If the problem persists, please create an issue and attach your `client.log` file.

     
## 🙌 Credits
- [MediaSession](https://developer.mozilla.org/en-US/docs/Web/API/MediaSession) for accessing media metadata.
- [pypresence](https://github.com/qwertyquerty/pypresence) for Discord Rich Presence integration.
- [pybrinf](https://github.com/manucabral/pybrinf) for browser information.

## 📜 License & Disclaimer
This application is not an official product of YouTube or Google and is licensed under the MIT License.

## ✨ Contributing
All contributions, including bug reports, fixes, enhancements, and new ideas are welcome!
If you want to contribute, simply create a pull request or an issue. We will review your submission and get back to you as soon as possible.
Thank you for helping to improve the application!
