# Github Release bot

This bot report new releases of repositories that you want to monitor through Telegram API.

## Create api.ini

Let's create `api.ini` file, and set your `api_id` and `api_hash`.  
For more information, please refer to [this website](https://my.telegram.org/auth).

The format of `api.ini` is like this:

```ini
[TELEGRAM]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH

; Username or ID to receive message from this bot
target_user = TARGET_USERNAME

[GITHUB]
; Fine-grained tokens
token = TOKEN
```

## TODO

- [ ] Manage `node_id`, `tag_name` and URL information using Database like SQLite.
- [ ] Allow to resister additional repository usign Telegram app.
