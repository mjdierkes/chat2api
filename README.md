# CHAT2API

🤖 A simple ChatGPT TO API proxy

🌟 Free and unlimited use of `GPT-3.5` without needing an account

💥 Supports using AccessToken with accounts, compatible with `O1-Preview/mini`, `GPT-4`, `GPT-4o/mini`, and `GPTs`

🔍 Response format is completely consistent with the real API, compatible with almost all clients

👮 Accompanied by the user management frontend [Chat-Share](https://github.com/h88782481/Chat-Share). Before use, configure the environment variables in advance (set `ENABLE_GATEWAY` to True and `AUTO_SEED` to False)

## Community Chat

[https://t.me/chat2api](https://t.me/chat2api)

Please read the repository documentation thoroughly, especially the FAQ section, before asking questions.

When asking questions, please provide:

1. A screenshot of the startup logs (mask sensitive information, including environment variables and version numbers)
2. The error log information (mask sensitive information)
3. The status code and response body returned by the API

## Sponsors

Thanks to Capsolver for sponsoring this project. For any human-machine CAPTCHA on the market, you can use [Capsolver](https://www.capsolver.com/zh?utm_source=github&utm_medium=repo&utm_campaign=scraping&utm_term=chat2api) to solve it.

[![Capsolver](docs/capsolver.png)](https://www.capsolver.com/zh?utm_source=github&utm_medium=repo&utm_campaign=scraping&utm_term=chat2api)

## Features

### The latest version number is stored in `version.txt`

### Reverse API Features

> - [x] Streamed and non-streamed transmission
> - [x] GPT-3.5 conversations without login
> - [x] GPT-3.5 model conversations (if the model name does not include gpt-4, it defaults to gpt-3.5, which is text-davinci-002-render-sha)
> - [x] GPT-4 series model conversations (if the model name includes: gpt-4, gpt-4o, gpt-4o-mini, gpt-4-mobile, you can use the corresponding model by providing an AccessToken)
> - [x] O1 series model conversations (if the model name includes o1-preview, o1-mini, you can use the corresponding model by providing an AccessToken)
> - [x] GPT-4 model for drawing, coding, and internet access
> - [x] Supports GPTs (use model names: gpt-4-gizmo-g-\*)
> - [x] Supports Team Plus accounts (requires passing the team account id)
> - [x] Upload images and files (in API-compatible formats, supports URL and base64)
> - [x] Can be used as a gateway with multi-machine distributed deployment
> - [x] Multi-account polling, supporting both `AccessToken` and `RefreshToken`
> - [x] Retry on request failure, automatically polling the next Token
> - [x] Token management, supporting upload and clearance
> - [x] Scheduled use of `RefreshToken` to refresh `AccessToken` / On each startup, all tokens are refreshed non-forcibly once, and forcibly refreshed once every four days at 3 AM.
> - [x] Supports file downloads, requires enabling history records
> - [x] Supports output of the inference process for `O1-Preview/mini` models

### Official Website Mirror Features

> - [x] Supports native official website mirrors
> - [x] Randomly selects from the backend account pool, `Seed` sets random accounts
> - [x] Direct login using `RefreshToken` or `AccessToken`
> - [x] Supports O1-Preview/mini, GPT-4, GPT-4o/mini
> - [x] Disables sensitive information interfaces and some setting interfaces
> - [x] `/login` login page, automatically redirects to the login page after logout
> - [x] `/?token=xxx` direct login, where xxx is `RefreshToken`, `AccessToken`, or `SeedToken` (random seed)

> TODO
>
> - [ ] Mirror support for `GPTs`
> - [ ] None for now, welcome to submit `issues`

## Reverse API

A completely `OpenAI`-formatted API that supports passing in `AccessToken` or `RefreshToken`, and can use GPT-4, GPT-4o, GPTs, O1-Preview, O1-Mini:

```bash
curl --location 'http://127.0.0.1:5005/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{Token}}' \
--data '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "stream": true
   }'
```

Pass your account's `AccessToken` or `RefreshToken` as `{{ Token }}`.
Alternatively, you can provide the value of the environment variable `Authorization`, which will randomly select a backend account.

If you have a team account, you can pass in `ChatGPT-Account-ID` to use a Team workspace:

- Method 1:
  Pass the `ChatGPT-Account-ID` value in the `headers`

- Method 2:
  `Authorization: Bearer <AccessToken or RefreshToken>,<ChatGPT-Account-ID>`

If the `AUTHORIZATION` environment variable is set, you can pass the configured value as `{{ Token }}` to perform multi-token polling.

> - **AccessToken Retrieval**: After logging into ChatGPT, open [https://chatgpt.com/api/auth/session](https://chatgpt.com/api/auth/session) to obtain the `accessToken` value.
> - **RefreshToken Retrieval**: The method for obtaining this is not provided here.
> - **No-login GPT-3.5**: No Token is required.

## Token Management

1. Configure the environment variable `AUTHORIZATION` as the `authorization code`, then run the program.

2. Access `/tokens` or `/{api_prefix}/tokens` to view the existing number of Tokens, upload new Tokens, or clear Tokens.

3. When making requests, pass the `authorization code` configured in `AUTHORIZATION` to use the polling Tokens for conversations.

![tokens.png](docs/tokens.png)

## Official Website Native Mirror

1. Set the environment variable `ENABLE_GATEWAY` to `true`, then run the program. Note that after enabling, others can directly access your gateway through the domain.

2. Upload `RefreshToken` or `AccessToken` on the Token management page.

3. Visit `/login` to go to the login page.

![login.png](docs/login.png)

4. Enter the official website native mirror page for use.

![chatgpt.png](docs/chatgpt.png)

## Environment Variables

Each environment variable has a default value. If you do not understand the meaning of an environment variable, please do not set it, and do not pass empty values. Strings do not require quotes.

| Category     | Variable Name       | Example Value                                               | Default Value         | Description                                                                                                                                                                                      |
| ------------ | ------------------- | ----------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Security** | `API_PREFIX`        | `your_prefix`                                               | `None`                | API prefix password. If not set, it is easily accessible. If set, you need to request `/your_prefix/v1/chat/completions`                                                                         |
|              | `AUTHORIZATION`     | `your_first_authorization`,<br/>`your_second_authorization` | `[]`                  | Authorization codes you set for using multi-account polling Tokens, separated by commas                                                                                                          |
|              | `AUTH_KEY`          | `your_auth_key`                                             | `None`                | Private gateways require adding an `auth_key` in the request header to set this item                                                                                                             |
| **Request**  | `CHATGPT_BASE_URL`  | `https://chatgpt.com`                                       | `https://chatgpt.com` | ChatGPT gateway URL. Setting this changes the request website. Multiple gateways are separated by commas                                                                                         |
|              | `PROXY_URL`         | `http://ip:port`,<br/>`http://username:password@ip:port`    | `[]`                  | Global proxy URL. Enabled when encountering 403. Multiple proxies are separated by commas                                                                                                        |
|              | `EXPORT_PROXY_URL`  | `http://ip:port` or<br/>`http://username:password@ip:port`  | `None`                | Exit proxy URL to prevent leaking the origin IP when requesting images and files                                                                                                                 |
| **Features** | `HISTORY_DISABLED`  | `true`                                                      | `true`                | Whether to not save chat history and return `conversation_id`                                                                                                                                    |
|              | `POW_DIFFICULTY`    | `00003a`                                                    | `00003a`              | The difficulty of the Proof of Work to solve. Do not set if you do not understand                                                                                                                |
|              | `RETRY_TIMES`       | `3`                                                         | `3`                   | Number of retry attempts on errors. Using `AUTHORIZATION` will automatically randomly/poll the next account                                                                                      |
|              | `CONVERSATION_ONLY` | `false`                                                     | `false`               | Whether to use the conversation interface directly. Enable only if your gateway supports automatic POW solving                                                                                   |
|              | `ENABLE_LIMIT`      | `true`                                                      | `true`                | After enabling, it does not attempt to bypass the official request limit, minimizing the risk of account bans                                                                                    |
|              | `UPLOAD_BY_URL`     | `false`                                                     | `false`               | After enabling, dialogues are conducted based on `URL + space + text`. Automatically parses and uploads URL content. Multiple URLs are separated by spaces                                       |
|              | `CHECK_MODEL`       | `false`                                                     | `false`               | Checks if the account supports the passed model. Enabling can slightly avoid GPT-4 returning GPT-3.5 content, but increases request latency and does not solve the intelligence downgrade issue  |
|              | `SCHEDULED_REFRESH` | `false`                                                     | `false`               | Whether to periodically refresh `AccessToken`. After enabling, all tokens are non-forcibly refreshed once on each startup and forcibly refreshed once every four days at 3 AM                    |
|              | `RANDOM_TOKEN`      | `true`                                                      | `true`                | Whether to randomly select backend `Token`. If enabled, backend accounts are randomly selected; if disabled, they are polled in order                                                            |
| **Gateway**  | `ENABLE_GATEWAY`    | `false`                                                     | `false`               | Whether to enable gateway mode. Enabling allows using mirror sites but makes it unsecured                                                                                                        |
|              | `AUTO_SEED`         | `false`                                                     | `true`                | Whether to enable random account mode. By default enabled, randomly matches backend `Token` after inputting `seed`. After disabling, manual interface docking is required for `Token` management |

## Deployment

### Zeabur Deployment

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/6HEGIZ?referralCode=LanQian528)

### Direct Deployment

```bash
git clone https://github.com/LanQian528/chat2api
cd chat2api
pip install -r requirements.txt
python app.py
```

### Docker Deployment

You need to install Docker and Docker Compose.

```bash
docker run -d \
  --name chat2api \
  -p 5005:5005 \
  lanqian528/chat2api:latest
```

### (Recommended, supports PLUS accounts) Docker Compose Deployment

Create a new directory, for example, `chat2api`, and enter the directory:

```bash
mkdir chat2api
cd chat2api
```

Download the `docker-compose.yml` file from the repository into this directory:

```bash
wget https://raw.githubusercontent.com/LanQian528/chat2api/main/docker-compose-warp.yml
```

Modify the environment variables in the `docker-compose-warp.yml` file, then save and run:

```bash
docker-compose up -d
```

## Frequently Asked Questions

> - **Error Codes:**
>
>   - `401`: The current IP does not support no-login access. Please try changing the IP address, set a proxy in the `PROXY_URL` environment variable, or your authentication has failed.
>   - `403`: Please check the specific error information in the logs.
>   - `429`: The current IP has exceeded the request limit within 1 hour. Please try again later or change the IP.
>   - `500`: Internal server error. The request failed.
>   - `502`: Server gateway error or network is unavailable. Please try changing the network environment.
>
> - **Known Issues:**
>
>   - Many Japanese IPs do not support no-login access. It is recommended to use US IPs for no-login GPT-3.5.
>   - 99% of accounts support free `GPT-4o`, but the activation depends on the IP region. Currently, Japanese and Singaporean IPs have a higher activation probability.
>
> - **What is the `AUTHORIZATION` environment variable?**
>
>   - It is an authorization code you set for `chat2api` to use the saved Tokens in a polling manner. Pass it as an `APIKEY` during requests.
>
> - **How to obtain `AccessToken`?**
>   - After logging into ChatGPT, open [https://chatgpt.com/api/auth/session](https://chatgpt.com/api/auth/session) to get the `accessToken` value.

## License

MIT License
