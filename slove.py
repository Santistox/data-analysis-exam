import xlsxwriter
import dbworker
import tasks

def create_file(user_id, filename):
	# create clear workbook
	workbook = xlsxwriter.Workbook('./works/%s.xlsx' % filename)

	# task 1
	dataset_task1 = dbworker.get_task_value(user_id, 'dataset_task1')
	variant_task1 = dbworker.get_task_value(user_id, 'variant_task1')
	kvrtl_task1 = dbworker.get_task_value(user_id, 'kvrtl_task1')
	worksheet = workbook.add_worksheet('Задание 1')
	tasks.task1(worksheet, dataset_task1, variant_task1, kvrtl_task1)

	# task 2
	dataset_task2 = dbworker.get_task_value(user_id, 'dataset_task2')
	variant_task2 = dbworker.get_task_value(user_id, 'variant_task2')
	alpha_task2 = dbworker.get_task_value(user_id, 'alpha_task2')
	lvl_task2 = dbworker.get_task_value(user_id, 'lvl_task2')
	tp_1_task2 = dbworker.get_task_value(user_id, 'tp_1_task2')
	tp_2_task2 = dbworker.get_task_value(user_id, 'tp_2_task2')
	worksheet = workbook.add_worksheet('Задание 2')
	tasks.task2(worksheet, dataset_task2, variant_task2, alpha_task2, lvl_task2, tp_1_task2, tp_2_task2)

	# task3
	dataset_task3 = dbworker.get_task_value(user_id, 'dataset_task3')
	variant1_task3 = dbworker.get_task_value(user_id, 'variant1_task3')
	variant2_task3 = dbworker.get_task_value(user_id, 'variant2_task3')
	lvl_1_task3 = dbworker.get_task_value(user_id, 'lvl_1_task3')
	lvl_2_task3 = dbworker.get_task_value(user_id, 'lvl_2_task3')
	worksheet = workbook.add_worksheet('Задание 3')
	tasks.task3(worksheet, dataset_task3, variant1_task3, variant2_task3, lvl_1_task3, lvl_2_task3)

	# close workbook file
	workbook.close()
