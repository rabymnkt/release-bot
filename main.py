# coding: utf-8
import configparser
from pyrogram import Client
import schedule
import polling
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys

# load api.ini and config.ini
api_ini = configparser.ConfigParser()
api_ini.read("api.ini", encoding="utf-8")
config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")

# Telegram API
api_id = api_ini["TELEGRAM"]["api_id"]
api_hash = api_ini["TELEGRAM"]["api_hash"]
target_user = api_ini["TELEGRAM"]["target_user"]

# Initialize Pyrogram client
app = Client("my_account", api_id=api_id, api_hash=api_hash)


def send_initial_message():
    with app:
        now = datetime.now()
        time_info = now.strftime("%Y/%m/%d %H:%M:%S: ")
        app.send_message(target_user, time_info +
                         "Repo Surveillance Started!✈", disable_notification=True)


def send_all_repos():
    with app:
        url_list = polling.get_all_repos()
        if len(url_list) != 0:
            for url in url_list:
                app.send_message(target_user, url)
        else:
            now = datetime.now()
            time_info = now.strftime("%Y/%m/%d %H:%M: ")
            app.send_message(target_user, time_info +
                             "No repos registered.👍", disable_notification=True)


def scheduled_job():
    with app:
        url_list = polling.get_updated_repos()
        if len(url_list) != 0:
            for url in url_list:
                app.send_message(target_user, url)
        # else:
        #     now = datetime.now()
        #     time_info = now.strftime("%Y/%m/%d %H:%M: ")
        #     app.send_message(target_user, time_info +
        #                      "New Release not Found!", disable_notification=True)


def weekly_job():
    today = datetime.now() + relativedelta(days=-1)
    one_week_before = datetime.now() + relativedelta(days=-7)
    week_str = one_week_before.strftime(
        "%Y/%m/%d") + " - " + today.strftime("%Y/%m/%d")
    with app:
        Message = "📢WEEKLY UPDATE (" + week_str + ")"
        Message += "\n"
        weekly_updated_releases = polling.get_weekly_update()
        if len(weekly_updated_releases) != 0:
            for index in range(len(weekly_updated_releases)):
                if index != 0:
                    Message += "\n\n"
                Message += weekly_updated_releases[index][0] + ":\n" + \
                    weekly_updated_releases[index][1] + \
                    " ➠ " + \
                    weekly_updated_releases[index][2] + \
                    "\n" + weekly_updated_releases[index][3]
        else:
            Message += "New Release not Found!👍"

        app.send_message(
            target_user, Message, disable_notification=True, disable_web_page_preview=True)


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

    schedule.every().monday.at("9:00").do()
    while True:
        schedule.run_pending()
        time.sleep(60)
