import requests

webhook_url = "https://discord.com/api/webhooks/1447688102180294832/ZimF4PlxGM2myuRB7f1msop5FgDfoEXn_vctbK6fz2RTKLKXnkazl80T8Z7b1GX6imuo"

data = {
    "content": "Merhaba!"
}

response = requests.post(webhook_url, json=data)

print("Status:", response.status_code)
print("Response:", response.text)
