# coding: utf-8
import configparser
import requests


# load api.ini
api_ini = configparser.ConfigParser()
api_ini.read('api.ini', encoding='utf-8')

url_list = []
node_id_list = []
tag_name_list = []


def change_url_for_api(url: str) -> str:
    splited_url = url.strip().split("/")
    new_url = splited_url[0]+"/"+splited_url[1]+"/api."+splited_url[2] + \
        "/repos/"+splited_url[3]+"/"+splited_url[4]+"/releases"
    return new_url


def get_node_id_and_tag_name(api_url: str):
    token = 'Bearer ' + api_ini["GITHUB"]['token']
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': token,
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response = requests.get(api_url, headers=headers)
    return response.json()[0]["node_id"], response.json()[0]["tag_name"]


def initialize_node_id_and_tag_name():
    with open("repos-list.txt", "r", encoding="utf-8") as file:
        for line in file:
            api_url = change_url_for_api(line)
            node_id, tag_name = get_node_id_and_tag_name(api_url)
            url_list.append(line)
            node_id_list.append(node_id)
            tag_name_list.append(tag_name)


def update_node_id_and_tag_name() -> list:
    updated_repos_index = []
    with open("repos-list.txt", "r", encoding="utf-8") as file:
        for line in file:
            api_url = change_url_for_api(line)
            node_id, tag_name = get_node_id_and_tag_name(api_url)
            for index in range(node_id_list):
                if node_id != node_id_list[index]:
                    updated_repos_index.append(index)
                    node_id_list[index] = node_id
                    tag_name_list[index] = tag_name

    return updated_repos_index


def get_updated_repos() -> list:
    updated_repos_url = []
    updated_repos_index = update_node_id_and_tag_name()
    for index in updated_repos_index:
        new_release_url = url_list[index] + "/release/" + tag_name_list[index]
        updated_repos_url.append(new_release_url)

    return updated_repos_url
