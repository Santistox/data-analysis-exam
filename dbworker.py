# -*- coding: utf-8 -*-
"""Work with Vedis database 

All functions work with data base

set_* - this functions push data to database
get_* - this functions get data form database
use_key - this function take 1 value from available value of using key

"""
from vedis import Vedis
import config


def get_current_state(user_id):
    with Vedis(config.db_file) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return config.States.S_KEY.value


def set_state(user_id, value):
    with Vedis(config.db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False


def set_key(key, value):
    with Vedis(config.db_file) as db:
        try:
            db[key] = value
            return True
        except:
            return False


def get_key_info(key):
    with Vedis(config.db_file) as db:
        try:
            return db[key].decode()
        except KeyError:
            return 0


def use_key(key):
    with Vedis(config.db_file) as db:
        try:
            db[key] = int(db[key]) - 1
            return True
        except:
            return False


def set_task_value(user_id, val_name, value):
    with Vedis(config.db_file) as db:
            try:
                place = str(user_id) + str(val_name)
                db[place] = value
                return True
            except:
                return False


def get_task_value(user_id, val_name):
    with Vedis(config.db_file) as db:
        try:
            place = str(user_id) + str(val_name)
            return db[place].decode()
        except KeyError:
            return 0
