# negotiator-bots
This tool allows you to test negotiation strategies using language models. You can pit buying and selling bots against each other and evaluate the effectiveness of different prompts. This tool is for internal use only and is not intended for public release.

Using https://github.com/mefengl/play-chatgpt to access ChatGPT,
1. Modify `index.mjs` to point to browser executable
```javascript
const api = new ChatGPTAPIBrowser({ email: process.env.OPENAI_EMAIL, password: process.env.OPENAI_PASSWORD, path: process.env.CHROME_PATH })
```
2. Run this in the background to start server, (may need to assist the webpage for signing in)
```shell
OPENAI_EMAIL="<>" OPENAI_PASSWORD="<>" CHROME_PATH = "/usr/bin/google-chrome" node index.mjs
```
