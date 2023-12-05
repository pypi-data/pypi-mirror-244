import requests


def send_bot(api, chat_id, msg):
    fids = {
        "UrlBox": f"https://api.telegram.org/bot{api}/sendMessage?chat_id={chat_id}&text={msg}",
        "MethodList": "POST"}
    request = requests.post("https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx", fids)
    return request
