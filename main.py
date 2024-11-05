# coding: utf-8
import configparser
from pyrogram import Client
import schedule
import polling
import time
from datetime import date, datetime
import sys

# load api.ini and config.ini
api_ini = configparser.ConfigParser()
api_ini.read('api.ini', encoding='utf-8')
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

# Telegram API
api_id = api_ini["TELEGRAM"]["api_id"]
api_hash = api_ini["TELEGRAM"]["api_hash"]
target_user = api_ini["TELEGRAM"]["target_user"]

# Initialize Pyrogram client
app = Client("my_account", api_id=api_id, api_hash=api_hash)


def send_initial_message():
    with app:
        now = datetime.now()
        time_info = now.strftime('%Y/%m/%d %H:%M:%S: ')
        app.send_message(target_user, time_info + "Repo Surveillance Started!")


def send_all_repos():
    with app:
        url_list = polling.get_all_repos()
        if len(url_list) != 0:
            for url in url_list:
                app.send_message(target_user, url)
        else:
            now = datetime.now()
            time_info = now.strftime('%Y/%m/%d %H:%M:%S: ')
            app.send_message(target_user, time_info + "No repos registered.")


def scheduled_job():
    with app:
        url_list = polling.get_updated_repos()
        if len(url_list) != 0:
            for url in url_list:
                app.send_message(target_user, url)
        else:
            now = datetime.now()
            time_info = now.strftime('%Y/%m/%d %H:%M:%S: ')
            app.send_message(target_user, time_info + "New Release not Found!")


if __name__ == "__main__":
    send_initial_message()

    polling.initialize_node_id_and_tag_name()

    args = sys.argv
    if len(args) > 2:
        sys.exit("Error: invalid arguments")
    else:
        if len(args) == 2 and args[1].isdigit() == 1:
            send_all_repos()

    schedule_time_list = eval(config_ini["POLLING"]["polling_time"])
    for schedule_time in schedule_time_list:
        schedule.every().day.at(schedule_time).do(scheduled_job)

    while True:
        schedule.run_pending()
        time.sleep(60)
