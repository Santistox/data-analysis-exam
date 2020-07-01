# -*- coding: utf-8 -*-
"""Functions for solving exam tasks and filling out a file

3 tasks - 3 patrs of functions

"""
import xlsxwriter

def analysis(mass, types):
	for i in mass:
		if i in types:
			types[i] += 1
		else:
			types[i] = 1


# определение границ нормы датасета и количества элементов нарушающего их
def get_norm_section(worksheet, coef, hi, low):
	worksheet.write('J1', coef)
	worksheet.write('J3', 'Нижняя граница нормы')
	worksheet.write('J4', 'Верхняя граница нормы')
	worksheet.write('J5', 'Кол-во ниже нормы')
	worksheet.write('J6', 'Кол-во выше нормы')
	worksheet.write_formula('K3', '={}-(({}-{})*1.5)'.format(low, hi, low))
	worksheet.write_formula('K4', '={}+(({}-{})*1.5)'.format(hi, hi, low))
	worksheet.write_formula('K5', '=COUNTIF(B:B, "<"&K3)')
	worksheet.write_formula('K6', '=COUNTIF(B:B, ">"&K4)')


# решение 1 варианта
def get_var_1(worksheet, counter, num):
	# print('start calc var 1')
	names = [
		'количество NA',
		'кол-во беp NA',
		'мин знач',
		'макс знач',
		'квартиль 1',
		'медиана ',
		'квартиль 3',
		'квартильный размах',
		'ср знач',
		'станд откл',
		'дисп',
		'ошибка выборки',
		'эксцесс',
		'коэф ассим',
		'левая Ех 0,99',
		'правая Ех 0,99',
		'левая Varx 0,99',
		'равая Varx 0,99',
		'квантиль',
		'количество выбросов'
	]
	get_norm_section(worksheet, 0.01, 'H7', 'H5')
	worksheet.write_column('G1', names)
	worksheet.write('H1', counter)
	worksheet.write_formula('H2', '=COUNT(B:B)')
	worksheet.write_formula('H3', '=MIN(B:B)')
	worksheet.write_formula('H4', '=MAX(B:B)')
	worksheet.write_formula('H5', '=QUARTILE(B:B, 1)')
	worksheet.write_formula('H6', '=MEDIAN(B:B)')
	worksheet.write_formula('H7', '=QUARTILE(B:B, 3)')
	worksheet.write_formula('H8', '=H7-H5')
	worksheet.write_formula('H9', '=AVERAGE(B:B)')
	worksheet.write_formula('H10', '=_xlfn.STDEV(B:B)')
	worksheet.write_formula('H11', '=_xlfn.VAR.S(B:B)')
	worksheet.write_formula('H12', '=_xlfn.STDEV.S(B:B) / SQRT(COUNT(B:B))')
	worksheet.write_formula('H13', '=KURT(B:B)')
	worksheet.write_formula('H14', '=SKEW(B:B)')
	worksheet.write_formula('H15', '=H9-_xlfn.T.INV(0.99, H2-1)*H10/SQRT(H2)')
	worksheet.write_formula('H16', '=H9+_xlfn.T.INV(0.99, H2-1)*H10/SQRT(H2)')
	worksheet.write_formula('H17', '=H11*(H2-1)/_xlfn.CHISQ.INV(1-J1/2,H2-1)')
	worksheet.write_formula('H18', '=H11*(H2-1)/_xlfn.CHISQ.INV(J1/2,H2-1)')
	worksheet.write_formula('H19', '=_xlfn.PERCENTILE(B:B, {})'.format(num))
	worksheet.write_formula('H20', '=K5+K6')


# решение 2 варианта
def get_var_2(worksheet, counter):
	# print('start calc var 2')
	names = [
		'объем исх выборки',
		'кол-во беp NA',
		'ошибка выборки',
		'мин знач',
		'макс знач',
		'квартиль 1',
		'медиана ',
		'квартиль 3',
		'ср знач',
		'дисп',
		'станд откл',
		'размах выборки',
		'эксцесс',
		'коэф ассим',
		'левая Ех 0,9',
		'правая Ех 0,9',
		'левая Varx 0,9',
		'равая Varx 0,9',
		'нижняя гран нормы',
		'верхняя гран нормы'
	]
	get_norm_section(worksheet, 0.1, 'H8', 'H6')
	worksheet.write_column('G1', names)
	worksheet.write('H1', counter)
	worksheet.write_formula('H2', '=COUNT(B:B)')
	worksheet.write_formula('H3', '=_xlfn.STDEV.S(B:B) / SQRT(COUNT(B:B))')
	worksheet.write_formula('H4', '=MIN(B:B)')
	worksheet.write_formula('H5', '=MAX(B:B)')
	worksheet.write_formula('H6', '=QUARTILE(B:B, 1)')
	worksheet.write_formula('H7', '=MEDIAN(B:B)')
	worksheet.write_formula('H8', '=QUARTILE(B:B, 3)')
	worksheet.write_formula('H9', '=AVERAGE(B:B)')
	worksheet.write_formula('H10', '=_xlfn.VAR.S(B:B)')
	worksheet.write_formula('H11', '=_xlfn.STDEV(B:B)')
	worksheet.write_formula('H12', '=H5-H4')
	worksheet.write_formula('H13', '=KURT(B:B)')
	worksheet.write_formula('H14', '=SKEW(B:B)')
	worksheet.write_formula('H15', '=H9-_xlfn.T.INV(0.9, H2-1)*H11/SQRT(H2)')
	worksheet.write_formula('H16', '=H9+_xlfn.T.INV(0.9, H2-1)*H11/SQRT(H2)')
	worksheet.write_formula('H17', '=H10*(H2-1)/_xlfn.CHISQ.INV(1-J1/2,H2-1)')
	worksheet.write_formula('H18', '=H10*(H2-1)/_xlfn.CHISQ.INV(J1/2,H2-1)')
	worksheet.write_formula('H19', '=K3')
	worksheet.write_formula('H20', '=K4')


# решение 3 варианта
def get_var_3(worksheet, counter):
	# print('start calc var 3')
	names = [
		'кол-во NA',
		'кол-во беp NA',
		'ср знач',
		'стандарт откл',
		'дисперсия',
		'квартиль 1',
		'квартиль 3',
		'медиана',
		'макс занч',
		'мин знач',
		'размах выборки',
		'эксцесс',
		'коэф ассим',
		'ошибка выборки',
		'левая Ех 0,95',
		'правая Ех 0,95',
		'левая Varx 0,95',
		'равая Varx 0,95',
		'кол-во выбросов ниже нормы',
		'кол-во выбросов выше нормы'
	]
	get_norm_section(worksheet, 0.05, 'H7', 'H6')
	worksheet.write_column('G1', names)
	worksheet.write('H1', counter)
	worksheet.write_formula('H2', '=COUNT(B:B)')
	worksheet.write_formula('H3', '=AVERAGE(B:B)')
	worksheet.write_formula('H4', '=_xlfn.STDEV(B:B)')
	worksheet.write_formula('H5', '=_xlfn.VAR.S(B:B)')
	worksheet.write_formula('H6', '=QUARTILE(B:B, 1)')
	worksheet.write_formula('H7', '=QUARTILE(B:B, 3)')
	worksheet.write_formula('H8', '=MEDIAN(B:B)')
	worksheet.write_formula('H9', '=MAX(B:B)')
	worksheet.write_formula('H10', '=MIN(B:B)')
	worksheet.write_formula('H11', '=H9-H10')
	worksheet.write_formula('H12', '=KURT(B:B)')
	worksheet.write_formula('H13', '=SKEW(B:B)')
	worksheet.write_formula('H14', '=_xlfn.STDEV.S(B:B) / SQRT(COUNT(B:B))')
	worksheet.write_formula('H15', '=H3-_xlfn.T.INV(0.95, H2-1)*H4/SQRT(H2)')
	worksheet.write_formula('H16', '=H3+_xlfn.T.INV(0.95, H2-1)*H4/SQRT(H2)')
	worksheet.write_formula('H17', '=H5*(H2-1)/_xlfn.CHISQ.INV(1-J1/2,H2-1)')
	worksheet.write_formula('H18', '=H5*(H2-1)/_xlfn.CHISQ.INV(J1/2,H2-1)')
	worksheet.write_formula('H19', '=K5')
	worksheet.write_formula('H20', '=K6')


def task1(task_sheet, mass, variant, kvrtl):
	# датасет неочищенный в текстовом формате
	inp1 = mass.replace(' ', '').replace(';', ' ').replace('.', ',').replace('{', '').replace('}', '')
	data_mass = list(map(str, inp1.split()))

	# датасет неочищенный в текстовом формате
	inp2 = mass.replace(' ', '').replace(';', ' ').replace('{', '').replace('}', '')
	fl_mass_str = list(map(str, inp2.split()))

	# очистка от NA
	while 'NA' in fl_mass_str:
		fl_mass_str.remove('NA')

	# перевод во float
	fl_mass = [float(elem) for elem in fl_mass_str]

	# сортировка
	fl_mass_sort = fl_mass.copy()
	fl_mass_sort.sort()

	# определение параметров датасета
	elem_all = len(data_mass)
	elem_na = data_mass.count("NA")
	elem_no_na = elem_all - elem_na

	# запись дататсета в файл
	task_sheet.write('A1', 'Исходный')
	task_sheet.write('B1', 'Без NA')
	task_sheet.write('C1', 'Чистый')
	task_sheet.write_column('A2', data_mass)
	task_sheet.write_column('B2', fl_mass)
	task_sheet.write_column('C2', fl_mass_sort)

	if variant == '1':
		get_var_1(task_sheet, elem_na, kvrtl)
	if variant == '2':
		get_var_2(task_sheet, elem_all)
	if variant == '3':
		get_var_3(task_sheet, elem_na)


def task2(task_sheet, mass, varik, alpha, lvl , tp_1, tp_2):
	# датасет неочищенный в текстовом формате
	inp1 = mass.replace(' ', '').replace(';', '\n').replace('.', ',').replace('{', '').replace('}', '')
	data_mass = list(map(str, inp1.split()))

	# датасет неочищенный в текстовом формате
	inp2 = mass.replace(' ', '').replace(';', ' ').replace('{', '').replace('}', '')
	fl_mass = list(map(str, inp2.split()))

	# очистка от NA
	while 'NA' in fl_mass:
		fl_mass.remove('NA')

	# определение параметров датасета
	elem_all = len(data_mass)
	elem_na = data_mass.count("NA")
	elem_no_na = elem_all - elem_na

	# запись дататсета в файл
	task_sheet.write('A1', 'Исходный')
	task_sheet.write('B1', 'Без NA')
	task_sheet.write_column('A2', data_mass)
	task_sheet.write_column('B2', fl_mass)

	types = {}
	analysis(fl_mass, types)
	# print(types)
	positions = {
		'num': len(types) + 1,
		'na': len(types) + 2,
		'all': len(types) + 3,
		'no_na': len(types) + 4,
	}
	i = 1
	tp_id_1 = 0
	tp_id_2 = 0
	for item in sorted(types):
		if item == tp_1:
			tp_id_1 = i
		if varik == '2':
			if item == tp_2:
				tp_id_2 = i
		task_sheet.write('D%s' % i, item)
		task_sheet.write_formula('E%s' % i, '=COUNTIF(A:A, "%s")' % item)
		task_sheet.write_formula('F%s' % i, '=E{}/E{}'.format(i, positions['no_na']))
		task_sheet.write_formula('G%s' % i, '=1/D%i' % positions['num'])
		task_sheet.write_formula('H%s' % i, '=G%i*E%i' % (i, positions['no_na']))
		task_sheet.write_formula('I%s' % i, '=(E%i-H%i)^2/H%i' % (i, i, i))
		i += 1
	task_sheet.write('D{}'.format(i), len(types))
	task_sheet.write_formula('I%s' % i, 'SUM(I1:I%i)' % (i - 1))
	i += 1
	task_sheet.write('D{}'.format(positions['na']), 'NA')
	task_sheet.write_formula('E{}'.format(positions['na']), '=COUNTIF(A:A, "NA")')
	i += 1
	task_sheet.write('D{}'.format(positions['all']), 'Всего')
	task_sheet.write_formula('E{}'.format(positions['all']), '=SUM(E1:E%i)' % (i - 1))
	i += 1
	task_sheet.write('D{}'.format(positions['no_na']), 'Без NA')
	task_sheet.write_formula('E{}'.format(positions['no_na']), '=E%i-E%i' % ((i - 1), (i - 2)))
	i += 1
	task_sheet.write('D{}'.format(i), 'P')
	task_sheet.write_formula('E{}'.format(i), '=F%i' % tp_id_1)
	i += 1
	task_sheet.write('D{}'.format(i), 'Q')
	task_sheet.write_formula('E{}'.format(i), '=1-E%i' % (i - 1))
	i += 1
	task_sheet.write('D{}'.format(i), 'Alpha')
	task_sheet.write('E{}'.format(i), float(alpha))
	i += 1
	task_sheet.write('D{}'.format(i), 'Z')
	task_sheet.write_formula('E{}'.format(i), '=_xlfn.NORM.S.INV((1-E%i)/2)' % (i - 1))
	i += 1
	task_sheet.write('D{}'.format(i), 'Delta')
	task_sheet.write_formula('E{}'.format(i), '=E{}*(E{}*E{}/E{})^0.5'.format((i - 1), (i - 3), (i - 4), (i - 5)))
	i += 1
	task_sheet.write('D{}'.format(i), 'ЛГ')
	task_sheet.write_formula('E{}'.format(i), '=E%i+E%i' % ((i - 5), (i - 1)))
	i += 1
	task_sheet.write('D{}'.format(i), 'ПГ')
	task_sheet.write_formula('E{}'.format(i), '=E%i-E%i' % ((i - 6), (i - 2)))
	i += 2

	# Варик 1
	if varik == '1':
		task_sheet.write('D{}'.format(i), 'Кол-во ответов')
		task_sheet.write_formula('E{}'.format(i), '=D%i' % (positions['na'] - 1))
		i += 1
		task_sheet.write('D{}'.format(i), 'Без NA')
		task_sheet.write_formula('E{}'.format(i), '=E%i' % positions['no_na'])
		i += 1
		task_sheet.write('D{}'.format(i), 'Кол-во NA')
		task_sheet.write_formula('E{}'.format(i), '=E%i' % positions['na'])
		i += 1
		task_sheet.write('D{}'.format(i), 'Доля %s' % tp_1)
		task_sheet.write_formula('E{}'.format(i), '=F%i' % tp_id_1)
		i += 1
		task_sheet.write('D{}'.format(i), 'Правая {} для {}'.format(alpha, tp_1))
		task_sheet.write_formula('E{}'.format(i), '=E%i' % (positions['no_na'] + 7))
		i += 1
		task_sheet.write('D{}'.format(i), 'Левая {} для {}'.format(alpha, tp_1))
		task_sheet.write_formula('E{}'.format(i), '=E%i' % (positions['no_na'] + 6))
		i += 1
		# lvl = input('lvl\n')
		task_sheet.write('D{}'.format(i), 'ХИ крит')
		task_sheet.write_formula('E{}'.format(i), '=_xlfn.CHISQ.INV(1-%f, E%i)' % (float(lvl), (i + 1)))
		i += 1
		task_sheet.write('D{}'.format(i), 'Кол-во степ свободы')
		task_sheet.write_formula('E{}'.format(i), '=D%i-1' % (positions['na'] - 1))
		i += 1
		task_sheet.write('D{}'.format(i), 'ХИ реал')
		task_sheet.write_formula('E{}'.format(i), '=I%i' % (len(types) + 1))
		i += 1
		task_sheet.write('D{}'.format(i), 'Гипотеза')
		task_sheet.write_formula('E{}'.format(i), '=IF(E%i>E%i,1,0)' % ((i - 1), (i - 3)))

	# Варик 2
	if varik == '2':
		task_sheet.write('D{}'.format(i), 'Кол-во без NA')
		task_sheet.write_formula('E{}'.format(i), '=E%i' % positions['no_na'])
		i += 1
		task_sheet.write('D{}'.format(i), 'Варианты ответа')
		task_sheet.write_formula('E{}'.format(i), '=D%i' % (positions['na'] - 1))
		i += 1
		task_sheet.write('D{}'.format(i), 'Кол-во %s' % tp_2)
		task_sheet.write_formula('E{}'.format(i), '=E%i' % tp_id_2)
		i += 1
		task_sheet.write('D{}'.format(i), 'Доля %s' % tp_1)
		task_sheet.write_formula('E{}'.format(i), '=F%i' % tp_id_1)
		i += 1
		task_sheet.write('D{}'.format(i), 'Левая {} для {}'.format(alpha, tp_1))
		task_sheet.write_formula('E{}'.format(i), '=E%i' % (positions['no_na'] + 6))
		i += 1
		task_sheet.write('D{}'.format(i), 'Правая {} для {}'.format(alpha, tp_1))
		task_sheet.write_formula('E{}'.format(i), '=E%i' % (positions['no_na'] + 7))
		i += 1
		task_sheet.write('D{}'.format(i), 'Кол-во степ свободы')
		task_sheet.write_formula('E{}'.format(i), '=D%i-1' % (positions['na'] - 1))
		i += 1
		# lvl = input('lvl\n')
		task_sheet.write('D{}'.format(i), 'ХИ крит')
		task_sheet.write_formula('E{}'.format(i), '=_xlfn.CHISQ.INV(1-%f, E%i)' % (float(lvl), (i - 1)))
		i += 1
		task_sheet.write('D{}'.format(i), 'ХИ реал')
		task_sheet.write_formula('E{}'.format(i), '=I%i' % (len(types) + 1))
		i += 1
		task_sheet.write('D{}'.format(i), 'Гипотеза')
		task_sheet.write_formula('E{}'.format(i), '=IF(E%i>E%i,1,0)' % ((i - 1), (i - 2)))
	# task_sheet.write_column('D2', fl_mass)

def task3(task_sheet, mass, variant1, variant2, lvl_1, lvl_2):
	# mass = input('datasets\n')

	# датасет неочищенный в текстовом формате
	inp1 = mass.replace(' ', '').replace(';', '\n').replace('(', '').replace(')', '').replace(',', '\n').replace('{', '').replace('}', '')
	data_mass = list(map(str, inp1.split()))
	i = 0
	col_1 = []
	col_2 = []
	for elem in data_mass:
		if i % 2 == 0:
			if elem != 'NA' and elem != 'NA':
				col_1.append(float(elem))
			else:
				col_1.append(elem)
		else:
			if elem != 'NA' and elem != 'NA':
				col_2.append(float(elem))
			else:
				col_2.append(elem)
		i += 1
	col_1_clear = []
	col_2_clear = []
	i = 0
	while i < len(data_mass)/2:
		if col_1[i] != 'NA' and col_2[i] != 'NA':
			col_1_clear.append(col_1[i])
			col_2_clear.append(col_2[i])
		i += 1

	# запись дататсета в файл
	task_sheet.write('A1', 'X1')
	task_sheet.write('B1', 'Y1')
	task_sheet.write_column('A2', col_1)
	task_sheet.write_column('B2', col_2)
	task_sheet.write('C1', 'X2')
	task_sheet.write('D1', 'Y2')
	task_sheet.write_column('C2', col_1_clear)
	task_sheet.write_column('D2', col_2_clear)

	task_sheet.write('F1', '1')
	task_sheet.write('F2', '2 alpha')
	task_sheet.write('F3', '2.1')
	task_sheet.write('F4', '2.2')
	task_sheet.write('F6', '3 alpha')
	task_sheet.write('F7', '3.1')
	task_sheet.write('F8', '3.2')

	task_sheet.write_formula('G1', '=_xlfn.CORREL(C:C,D:D)')
	task_sheet.write('G2', float(lvl_1))
	if variant1 == '2':
		task_sheet.write_formula('G3', '=_xlfn.T.TEST(C:C,D:D,2,3)/2')
	if variant1 == '1':
		task_sheet.write_formula('G3', '=_xlfn.T.TEST(C:C,D:D,2,3)')
	task_sheet.write_formula('G4', '=IF(G3>G2,0,1)')
	task_sheet.write('G6', float(lvl_2))
	if variant2 == '1':
		task_sheet.write_formula('G7', '=_xlfn.F.TEST(C:C,D:D)/2')
	if variant2 == '2':
		task_sheet.write_formula('G7', '=_xlfn.F.TEST(C:C,D:D)')
	task_sheet.write_formula('G8', '=IF(G7>G6,0,1)')

