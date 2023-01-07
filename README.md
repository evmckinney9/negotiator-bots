# negotiator-bots

This tool allows you to test negotiation strategies using language models. You can pit buying and selling bots against each other and evaluate the effectiveness of different prompts.

**This framework can be used to connect 2 ChatGPT instances directly to each other.**  Without a publically released API yet, we use a web server to mock inputs, alternating sharing responses between 2 open conversations using asynchronous python queries. 

___
A potential application of advanced language models is to use for negotiating contracts on your behalf automatically[^1] [^2]. Why not have a robot friend working for you in the background trying to save you money? That makes me wonder how we can test the effectiviness of different ChatGPT prompts for maximizing your discounts. Just for fun, I want to create a tournament of bots who are making deals, 1) just to see what happens 2) understand what works or what doesn't. We will test the strategy against only bots, so of course if a real human was on the otherside of the phone, it is possilbe things would go much differently.
___

Using https://github.com/mefengl/play-chatgpt to access ChatGPT,
1. Modify `index.mjs` to point to browser executable
```javascript
const api = new ChatGPTAPIBrowser({ email: process.env.OPENAI_EMAIL, password: process.env.OPENAI_PASSWORD, path: process.env.CHROME_PATH })
```
2. Run this (`start.sh`) in the background to start server, (may need to assist the webpage for signing in)
```shell
OPENAI_EMAIL="<>" OPENAI_PASSWORD="<>" CHROME_PATH = "/usr/bin/google-chrome" node index.mjs
```

[^1]: https://futurism.com/the-byte/ai-chatbot-lawyer-customer-service
[^2]: https://www.pcmag.com/news/watch-donotpays-ai-chatbot-renegotiate-a-comcast-bill-to-be-120-lower
