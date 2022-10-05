import requests, json

url = "https://discord.com/api/webhooks/1027002584680116274/YbeUat0MJaoWVNWbZ4cbJDIVvoR9gGKrdlANQgcrRjvMa5CaNPiS3LyaeqvXEDeofUqo"
data = {'content': f"The refresh token has expired." }
requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})