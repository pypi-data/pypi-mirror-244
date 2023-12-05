import yaml
import json
import os
import datetime as datetime
from aerarium.consts import AERARIUM_PATH, DATA_FILE_PATH, CONFIG_FILE_PATH


def generate_config():
    account_name = input("Enter account name: ")
    account_balance = float(input("Enter account balance: "))

    config = {
        "account_name": account_name,
        "account_balance": account_balance,
        "data_file_path": DATA_FILE_PATH,
    }

    return config


def update_config(account_balance):
    file_path = CONFIG_FILE_PATH
    with open(file_path, "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    config["account_balance"] = account_balance

    with open(file_path, "w") as file:
        yaml.dump(config, file)


def make_config(config):
    if not os.path.exists(AERARIUM_PATH):
        os.makedirs(AERARIUM_PATH)

    with open(CONFIG_FILE_PATH, "w") as file:
        yaml.dump(config, file)


def append_to_json(new_data):
    file_path = DATA_FILE_PATH
    try:
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(new_data)

    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=2)


def get_transactions():
    file_path = DATA_FILE_PATH
    with open(file_path, "r") as file:
        transactions = json.load(file)

    return transactions


if __name__ == "__main__":
    config = generate_config()
    make_config(config)
