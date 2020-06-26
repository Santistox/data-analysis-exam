import xlsxwriter
from collections import Counter


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
	print('start calc var 1')
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
	print('start calc var 2')
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
	print('start calc var 3')
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
	inp1 = mass.replace(' ', '').replace(';', ' ').replace('.', ',')
	data_mass = list(map(str, inp1.split()))

	# датасет неочищенный в текстовом формате
	inp2 = mass.replace(' ', '').replace(';', ' ')
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

	print(elem_all, elem_na, elem_no_na)
	print(data_mass)
	print(fl_mass)
	print(fl_mass_sort)

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
	# mass = input('datasets\n')
	# varik = input('varik?\n1-2?\n')
	# датасет неочищенный в текстовом формате
	inp1 = mass.replace(' ', '').replace(';', '\n').replace('.', ',')
	data_mass = list(map(str, inp1.split()))

	# датасет неочищенный в текстовом формате
	inp2 = mass.replace(' ', '').replace(';', ' ')
	fl_mass = list(map(str, inp2.split()))

	# очистка от NA
	while 'NA' in fl_mass:
		fl_mass.remove('NA')

	# определение параметров датасета
	elem_all = len(data_mass)
	elem_na = data_mass.count("NA")
	elem_no_na = elem_all - elem_na

	# arrays = Counter(fl_mass)
	# types = len(list(arrays))
	print(elem_all, elem_na, elem_no_na)
	print(data_mass)
	print(fl_mass)
	# print(len(list(arrays)))

	# запись дататсета в файл
	task_sheet.write('A1', 'Исходный')
	task_sheet.write('B1', 'Без NA')
	task_sheet.write_column('A2', data_mass)
	task_sheet.write_column('B2', fl_mass)

	types = {}
	analysis(fl_mass, types)
	print(types)
	positions = {
		'num': len(types) + 1,
		'na': len(types) + 2,
		'all': len(types) + 3,
		'no_na': len(types) + 4,
	}
	i = 1

	#alpha = input('alpha\n')

	tp_id_1 = 0
	tp_id_2 = 0
	for item in sorted(types):
		print("'%s':%s" % (item, types[item]))
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


# выбор варианта
# variant = input('Variant? 1-3\n')
#
# if variant == '1':
# 	get_var_1(task_sheet, elem_na)
# if variant == '2':
# 	get_var_2(task_sheet, elem_all)
# if variant == '3':
# 	get_var_3(task_sheet, elem_na)

def task3(task_sheet):
	mass = input('datasets\n')

	# датасет неочищенный в текстовом формате
	inp1 = mass.replace(' ', '').replace(';', '\n').replace('.', ',')
	data_mass = list(map(str, inp1.split()))

	# датасет неочищенный в текстовом формате
	inp2 = mass.replace(' ', '').replace(';', ' ')
	fl_mass = list(map(str, inp2.split()))

	# очистка от NA
	while 'NA' in fl_mass:
		fl_mass.remove('NA')

	# определение параметров датасета
	elem_all = len(data_mass)
	elem_na = data_mass.count("NA")
	elem_no_na = elem_all - elem_na

	# arrays = Counter(fl_mass)
	# types = len(list(arrays))
	print(elem_all, elem_na, elem_no_na)
	print(data_mass)
	print(fl_mass)
	# print(len(list(arrays)))

	# запись дататсета в файл
	task_sheet.write('A1', 'Исходный')
	task_sheet.write('B1', 'Без NA')
	task_sheet.write_column('A2', data_mass)
	task_sheet.write_column('B2', fl_mass)


def main():
	# filename = 'hello'
	filename = input('file\n')
	filename += '.xlsx'
	workbook = xlsxwriter.Workbook(filename)

	# task 1
	print('---------TASK 1---------\n')
	#mass = input('dataset\n')
	mass = "160.6; 165.1; NA; 161.7; 139.9; 173.4; 159.3; 140.7; 143.6; 133.8; 165.6; 134.3; 205.8; 125.6; 165; 200.1; NA; 198.4; 119.5; 120.1; 146.6; 135.1; 175.1; 157.3; 144.9; 143.7; 183.7; 124; 184.6; NA; NA; NA; 145.7; 183.9; 218.1; 198.6; 141.4; 179.7; NA; 227.4; 181.3; 161.4; 123.3; 159.9; 31.3000000000001; 180.5; 159.6; 179.1; 118.4; 138.1; 99.2; 168.5; 183.5; NA; 153.4; 184.5; 135; 209; 181.2; NA; 188.5; 185.7; 221.9; NA; 156.9; 165; 159.1; 134.5; 119.5; 132.7; 195.9; 134.5; 193.9; 219.7; 121.9; 135.3; 168.6; NA; 152.6; 166.8; 161; 120.5; 155.9; NA; 115.2; 121.5; 170; 129.3; 134.8; 117.4; NA; 180.2; 145.6; 161.1; 128; 211.2; 174.4; 133.2; 154.2; 118.7; 167.2; 135.9; NA; 201.6; NA; 180.5; 160.2; 126.5; 139.8; 134.6; 168.8; 145; NA; 161.2; 130.7; 166.6; 176.7; 158.2; NA; 200.9; 171.2; 145.3; 157.3; 81.1; 148.7; 163.7; 167.9; NA; 138.9; 162.7; 172.3; 144.8; 150.7; 139.4; 196.7; NA; 149.7; 177.5; 111.8; 138.5; 107.6; 158.6; 135.8; NA; 88.6; 102.5; 98.8; 124.5; 147.5; 140.3; 175; 163.4; 169.8; 141.8; 118; 199; 164.6; 144.4; 123.2; 142.3; 201.8; 83.2; 187.3; 162.7; 162.9; 208.1; 143.6; 142.5; 141.6; NA; 182.8; 183.2; 175.1; 176.2; 172; 191; 135.9; 183.1; 133.8; NA; 162.3; 179.5; 110.6; 132.3; 179.2; NA; 108; 179.2; 163.5; 154.7; 177.9; 128.9; NA; 183.1; 168.1; 186; 164.2; 159.1; 153.3; 140.6; 133.9; 181.9; 228.4; NA; 103.8; 106.1; NA; 114.4; 164.4; NA; 168.2; 136.6; 182.9; 119.9; 163.5; 99.5; 178; 135.8; 170; 160.4; 151.6; 188.1; 164.6; NA; 195.2; 148.6; 161.1; 102.5; 122.7; 116.7; 130.9; 152.3; 122.1; 175.6; 134.8; 134.7; 134; 197; 94.7; 183.9; 176; 198.5; NA; 164.8; 139.8; 151; 171.4; 154.7; 125.4; 118.2; 131; 170.1; 142.1; 180.7; 152.6; 176.2; 191.8; 148.8; 185.8; 151.9; 125.4; 135.7; 169.3; 129.2; 122.5; 179.5; 157.1; 195.6; 158.9; 152.3; 321.1; NA; 111.3; 101.8; 110.1; 175.6; 362.5; 186.2; 158.8; 139.7; 108.4; NA; 80.5; NA; 145.3; 170.1; 161.9; 179; 131.9; 137.5; 194.1; 196.6; 188.4; NA; 129.3; 165.2; 187.8; 110.3; 161.6; NA; 174.8; 163.8; 160; 142.5; 131.3; 191.8; 169.6; 194.6; 190.9; 162.1"
	variant_task1 = input('variant? 1-3\n')
	kvrtl_task1 = 0
	if variant_task1 == '1':
		kvrtl_task1 = input('kvtl?\n')
	worksheet = workbook.add_worksheet()
	task1(worksheet, mass, variant_task1, kvrtl_task1)

	# task 2
	print('---------TASK 2---------\n')
	# mass = input('datasets\n')
	mass = "L; L; S; M; XXL; XXL; XXL; L; NA; XL; L; NA; M; NA; L; S; L; XL; L; L; M; XXL; XL; XL; XL; M; NA; S; S; XL; XXL; S; L; XL; L; NA; L; S; XL; S; L; XXL; XL; M; XL; M; S; S; S; XXL; XXL; XXL; M; S; L; M; S; L; NA; NA; XXL; M; L; XL; M; NA; NA; M; M; XXL; XXL; NA; M; XXL; XXL; L; S; L; NA; NA; XL; M; NA; M; XL; L; XL; L; S; S; XL; XL; M; L; M; NA; M; XXL; NA; M; M; M; S; S; L; XL; S; NA; XXL; M; XL; XXL; S; XL; S; XXL; M; XXL; S; S; M; XL; XL; XXL; M; XL; S; XL; XXL; S; NA; XL; L; XXL; L; XXL; XL; M; S; L; L; XL; L; L; S; S; XL; NA; NA; S; XL; M; M; NA; XXL; S; L; S; M; NA; NA; L; S; M; XXL; XL; S; NA; XXL; M; L; S; XL; S; NA; S; L; L; S; NA; L; L; XXL; XXL; S; M; NA; XXL; XXL; XXL; M; S; NA; XXL; XL; XL; M; S; L; XXL; M; L; XXL; NA; L; M; NA; XL; XXL; XXL; M; S; S; XXL; S; XL; M; NA; XXL; L; XXL; S; M; S; S; S; XL; L; S; L; S; XL; XXL; XXL; XXL; XXL; L; M; XL; NA; S; L; XXL; NA; NA; NA; M; L; NA; S; XL; NA; XXL; S; XL; S; XL; S; M; S; XXL; S; S; L; L; M; NA; M; S; XL; NA; XL; L; S; NA; S; S; XXL; NA; L; NA; XXL; XL; XL; M; S; XL; S; S; L; L; XL; S; XXL; M; NA; XXL; M; XXL; NA; L; S; S; NA; M; S; XL; NA; XXL; NA; XXL; S; XXL; M; M; L; M; S; XL; XL"
	varik = input('varik?\n1-2?\n')
	alpha = input('alpha\n')
	lvl = input('lvl\n')
	if varik == '2':
		tp_1 = input('parametr 1\n')
		tp_2 = input('parametr 2\n')
	if varik == '1':
		tp_1 = input('parametr 1\n')
		tp_2 = ''
	worksheet = workbook.add_worksheet()
	task2(worksheet, mass, varik, alpha, lvl, tp_1, tp_2)
	# print('---------TASK 3---------\n')
	# worksheet = workbook.add_worksheet()
	# task3(worksheet)
	workbook.close()


main()
