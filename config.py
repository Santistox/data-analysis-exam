# -*- coding: utf-8 -*-

from enum import Enum
from private import teletoken, db_file


class States(Enum):
	# Get user key
	S_KEY = "0"

	# Start
	S_START = "00"

	# Task 1
	S_TASK1_DATASET = "10"
	S_TASK1_Q3 = "11"
	S_TASK1_KRVTL = "12"

	# Task 2
	S_TASK2_DATASET = "20"
	S_TASK2_Q1 = "21"
	S_TASK2_BRDR = "22"
	S_TASK2_BRDR_WD = "23"
	S_TASK2_WD = "24"
	S_TASK2_LVL = "25"

	# Task 3
	S_TASK3_DATASET = "30"