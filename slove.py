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

def task3(task_sheet, mass, variant, lvl_1, lvl_2):
	# mass = input('datasets\n')

	# датасет неочищенный в текстовом формате
	inp1 = mass.replace(' ', '').replace(';', '\n').replace('(', '').replace(')', '').replace(',', '\n')
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

	if variant == '1':
		task_sheet.write('F1', '1')
		task_sheet.write('F2', '2 alpha')
		task_sheet.write('F3', '2.1')
		task_sheet.write('F4', '2.2')
		task_sheet.write('F6', '3 alpha')
		task_sheet.write('F7', '3.1')
		task_sheet.write('F8', '3.2')

		task_sheet.write_formula('G1', '=_xlfn.CORREL(C:C,D:D)')
		task_sheet.write('G2', float(lvl_1))
		task_sheet.write_formula('G3', '=_xlfn.T.TEST(C:C,D:D,2,3)')
		task_sheet.write_formula('G4', '=IF(G3>G2,0,1)')
		task_sheet.write('G6', float(lvl_2))
		task_sheet.write_formula('G7', '=_xlfn.F.TEST(C:C,D:D)/2')
		task_sheet.write_formula('G8', '=IF(G7>G6,0,1)')
	if variant == '2':
		task_sheet.write('F1', '1')
		task_sheet.write('F2', '2 alpha')
		task_sheet.write('F3', '2.1')
		task_sheet.write('F4', '2.2')
		task_sheet.write('F6', '3 alpha')
		task_sheet.write('F7', '3.1')
		task_sheet.write('F8', '3.2')

		task_sheet.write_formula('G1', '=_xlfn.CORREL(C:C,D:D)')
		task_sheet.write('G2', float(lvl_1))
		task_sheet.write_formula('G3', '=_xlfn.T.TEST(C:C,D:D,2,3)')
		task_sheet.write_formula('G4', '=IF(G5>G2,0,1)')
		task_sheet.write('G6', float(lvl_2))
		task_sheet.write_formula('G7', '=_xlfn.F.TEST(C:C,D:D)')
		task_sheet.write_formula('G8', '=IF(G7>G6,0,1)')


def main():
	# filename = 'hello'
	filename = input('file\n')
	filename += '.xlsx'
	workbook = xlsxwriter.Workbook(filename)

	# task 1
	print('---------TASK 1---------\n')
	#mass = input('dataset\n')
	# mass = "160.6; 165.1; NA; 161.7; 139.9; 173.4; 159.3; 140.7; 143.6; 133.8; 165.6; 134.3; 205.8; 125.6; 165; 200.1; NA; 198.4; 119.5; 120.1; 146.6; 135.1; 175.1; 157.3; 144.9; 143.7; 183.7; 124; 184.6; NA; NA; NA; 145.7; 183.9; 218.1; 198.6; 141.4; 179.7; NA; 227.4; 181.3; 161.4; 123.3; 159.9; 31.3000000000001; 180.5; 159.6; 179.1; 118.4; 138.1; 99.2; 168.5; 183.5; NA; 153.4; 184.5; 135; 209; 181.2; NA; 188.5; 185.7; 221.9; NA; 156.9; 165; 159.1; 134.5; 119.5; 132.7; 195.9; 134.5; 193.9; 219.7; 121.9; 135.3; 168.6; NA; 152.6; 166.8; 161; 120.5; 155.9; NA; 115.2; 121.5; 170; 129.3; 134.8; 117.4; NA; 180.2; 145.6; 161.1; 128; 211.2; 174.4; 133.2; 154.2; 118.7; 167.2; 135.9; NA; 201.6; NA; 180.5; 160.2; 126.5; 139.8; 134.6; 168.8; 145; NA; 161.2; 130.7; 166.6; 176.7; 158.2; NA; 200.9; 171.2; 145.3; 157.3; 81.1; 148.7; 163.7; 167.9; NA; 138.9; 162.7; 172.3; 144.8; 150.7; 139.4; 196.7; NA; 149.7; 177.5; 111.8; 138.5; 107.6; 158.6; 135.8; NA; 88.6; 102.5; 98.8; 124.5; 147.5; 140.3; 175; 163.4; 169.8; 141.8; 118; 199; 164.6; 144.4; 123.2; 142.3; 201.8; 83.2; 187.3; 162.7; 162.9; 208.1; 143.6; 142.5; 141.6; NA; 182.8; 183.2; 175.1; 176.2; 172; 191; 135.9; 183.1; 133.8; NA; 162.3; 179.5; 110.6; 132.3; 179.2; NA; 108; 179.2; 163.5; 154.7; 177.9; 128.9; NA; 183.1; 168.1; 186; 164.2; 159.1; 153.3; 140.6; 133.9; 181.9; 228.4; NA; 103.8; 106.1; NA; 114.4; 164.4; NA; 168.2; 136.6; 182.9; 119.9; 163.5; 99.5; 178; 135.8; 170; 160.4; 151.6; 188.1; 164.6; NA; 195.2; 148.6; 161.1; 102.5; 122.7; 116.7; 130.9; 152.3; 122.1; 175.6; 134.8; 134.7; 134; 197; 94.7; 183.9; 176; 198.5; NA; 164.8; 139.8; 151; 171.4; 154.7; 125.4; 118.2; 131; 170.1; 142.1; 180.7; 152.6; 176.2; 191.8; 148.8; 185.8; 151.9; 125.4; 135.7; 169.3; 129.2; 122.5; 179.5; 157.1; 195.6; 158.9; 152.3; 321.1; NA; 111.3; 101.8; 110.1; 175.6; 362.5; 186.2; 158.8; 139.7; 108.4; NA; 80.5; NA; 145.3; 170.1; 161.9; 179; 131.9; 137.5; 194.1; 196.6; 188.4; NA; 129.3; 165.2; 187.8; 110.3; 161.6; NA; 174.8; 163.8; 160; 142.5; 131.3; 191.8; 169.6; 194.6; 190.9; 162.1"
	mass = "-227.6213; -199.5337; -202.0336; NA; -248.8253; -272.6407; -226.2243; -179.491; NA; -223.4054; -259.2346; -256.7101; NA; -208.4208; -266.3436; -280.8019; -241.8182; -203.2602; -235.9212; -230.8589; -240.6542; -299.0201; -247.0767; -240.9629; -241.4085; -195.8456; -299.9968; NA; -234.619; -231.5322; -227.7073; -266.4477; -200.3727; -297.6278; NA; -212.8851; NA; -250.7922; -227.597; -270.1709; -237.6468; NA; -231.7208; -212.1776; NA; -240.9355; -169.5872; -249.419; -247.1839; -247.4514; -256.7765; -276.6104; -206.8165; -313.4783; -269.9264; NA; -219.9504; -272.9077; -232.7854; -233.8773; -252.3968; -307.6149; -176.8246; -291.2035; -264.8078; -250.9765; -216.9979; NA; NA; -239.3021; -303.2924; -282.4026; -192.4573; -275.4714; -221.7437; -240.8525; -293.7416; -272.1717; -210.6525; -392.1413; -256.7276; -277.435; -208.3491; NA; -254.0554; -281.7946; -264.3328; -251.8733; -220.2485; -227.3754; -423.558; -256.9092; -252.9669; -250.5092; -273.0656; -276.0768; -308.5489; -198.2229; -263.6435; -228.6621; -211.0967; -235.6719; -241.4968; -265.011; -270.4399; -210.3694; -264.4546; -242.4303; -380.1024; -259.7752; -206.0542; -258.3691; -222.5555; -264.6826; -237.7613; -211.1415; -222.5755; -281.8463; -214.166; -258.5195; -302.044; -230.1333; -271.2273; -218.3612; -198.4914; -274.9114; -228.4973; -244.1283; -240.2103; -262.4723; -233.9211; -288.6843; -207.1918; -228.0142; -236.0548; -262.5656; -214.0815; -221.2577; NA; NA; -254.6171; -266.6473; -253.1815; -283.4647; -270.6105; -215.3834; NA; -237.1222; -255.5555; -282.9171; -269.4282; -188.8348; -277.2821; NA; -231.6738; -231.4801; NA; -256.0811; -270.1005; -275.125; -223.7382; -264.4113; -205.227; -295.4579; -291.4472; -242.5397; -244.209; -270.3185; -265.4197; -227.3016; -197.5573; -272.4488; -206.5748; -223.3643; -228.36; -281.8175; -251.1989; -213.064; -277.8647; -240.948; -232.9723; -278.0171; -256.3762; -246.0639; -324.0153; -248.498; -208.8366; -259.0976; -293.3409; -291.5813; -268.099; -242.9624; NA; -248.327; -227.1038; -265.1735; -264.8946; -239.0615; -254.0026; -260.7524; -256.1071; -263.7735; -242.43; -308.4623; NA; -200.3658; -32.4576000000001; -275.8553; -254.042; -303.5438; -219.1057; -275.3425; -250.22; -294.3961; -230.3668; -217.7879; -293.27; -231.8082; -224.2509; -276.71; -216.5876; NA; -299.234; -285.1679; -296.7297; -283.3421; -216.022; -246.1733; NA; -278.9084; -272.6785; -284.5284; -232.109; -226.9796; -276.3598; -260.6267; -264.0144; -257.6228; -262.2392; -272.2471; -247.6989; -291.3662; -219.5946; -328.2803; -230.6614; -236.5446; -302.4193; -254.4586; -249.0583; -227.9886; -303.3888; -234.5782; -247.5386; -231.0948; -273.8202; -216.5165; NA; -260.4022; -206.7997; -233.3101; -237.0732; -240.3341; -238.7222; -246.535; -269.4215; 10.9979999999999; -275.4929; -279.5187; -246.1887; -277.713; -200.5533; -298.9331; -285.6239; -264.5099; -213.8464; -211.1741; -252.0822; -238.9318; -234.6827; -258.5436; -249.3548; -274.2804; -287.3971; -263.2834; -260.4974; -207.3936; -221.9364; -241.5626; -299.6849; -200.3782"
	variant_task1 = input('variant? 1-3\n')
	kvrtl_task1 = 0
	if variant_task1 == '1':
		kvrtl_task1 = input('kvtl?\n')
	worksheet = workbook.add_worksheet()
	task1(worksheet, mass, variant_task1, kvrtl_task1)

	# task 2
	print('---------TASK 2---------\n')
	# mass = input('datasets\n')
	# mass = "L; L; S; M; XXL; XXL; XXL; L; NA; XL; L; NA; M; NA; L; S; L; XL; L; L; M; XXL; XL; XL; XL; M; NA; S; S; XL; XXL; S; L; XL; L; NA; L; S; XL; S; L; XXL; XL; M; XL; M; S; S; S; XXL; XXL; XXL; M; S; L; M; S; L; NA; NA; XXL; M; L; XL; M; NA; NA; M; M; XXL; XXL; NA; M; XXL; XXL; L; S; L; NA; NA; XL; M; NA; M; XL; L; XL; L; S; S; XL; XL; M; L; M; NA; M; XXL; NA; M; M; M; S; S; L; XL; S; NA; XXL; M; XL; XXL; S; XL; S; XXL; M; XXL; S; S; M; XL; XL; XXL; M; XL; S; XL; XXL; S; NA; XL; L; XXL; L; XXL; XL; M; S; L; L; XL; L; L; S; S; XL; NA; NA; S; XL; M; M; NA; XXL; S; L; S; M; NA; NA; L; S; M; XXL; XL; S; NA; XXL; M; L; S; XL; S; NA; S; L; L; S; NA; L; L; XXL; XXL; S; M; NA; XXL; XXL; XXL; M; S; NA; XXL; XL; XL; M; S; L; XXL; M; L; XXL; NA; L; M; NA; XL; XXL; XXL; M; S; S; XXL; S; XL; M; NA; XXL; L; XXL; S; M; S; S; S; XL; L; S; L; S; XL; XXL; XXL; XXL; XXL; L; M; XL; NA; S; L; XXL; NA; NA; NA; M; L; NA; S; XL; NA; XXL; S; XL; S; XL; S; M; S; XXL; S; S; L; L; M; NA; M; S; XL; NA; XL; L; S; NA; S; S; XXL; NA; L; NA; XXL; XL; XL; M; S; XL; S; S; L; L; XL; S; XXL; M; NA; XXL; M; XXL; NA; L; S; S; NA; M; S; XL; NA; XXL; NA; XXL; S; XXL; M; M; L; M; S; XL; XL"
	mass = "C; F; D; F; C; E; A; D; E; NA; B; E; E; F; E; D; E; E; E; A; F; E; C; B; D; A; NA; E; NA; A; E; A; NA; E; E; E; NA; E; B; B; NA; E; C; E; F; NA; E; C; F; E; E; E; A; F; A; F; NA; E; C; D; E; C; A; C; E; NA; D; A; C; D; C; NA; F; A; A; C; D; E; E; F; E; D; C; F; E; D; C; E; A; C; E; E; A; A; F; B; A; NA; A; A; D; E; NA; NA; E; F; F; B; C; B; F; E; NA; E; A; E; D; D; A; D; F; D; D; D; E; B; B; B; B; D; NA; A; E; C; F; F; E; F; A; B; E; F; C; NA; E; A; NA; E; C; E; B; B; D; E; NA; F; E; NA; A; E; B; E; E; E; E; E; A; E; NA; D; E; C; F; A; D; NA; F; F; E; C; F; E; E; F; E; D; C; NA; D; C; D; A; D; B; B; D; F; B; E; D; E; B; B; E; D; NA; E; NA; E; B; B; C; C; B; F; NA; B; E; C; E; D; F; D; F; A; NA; E; E; A; E; B; D; E; A; E; E; A; C; C; A; E; NA; B; E; E; B; E; F; A; F; NA; NA; F; A; E; D; A; F; E; E; A; E; A; E; C; NA; NA; E; D; E; C; E; B; E; F; E; D; C; B; A; D; A; E; E; E; F; E; B; B; D; F; E; E; E; E; E; E; B; F; E"
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

	# task3
	print('---------TASK 3---------\n')
	# mass = "(-120.9, -207.2); (-183.4, -222.5); (-166.5, -196.4); (-150.5, -177.6); (-117.2, -209.6); (-142.9, -183.7); (-152.1, -216.6); (-132.4, -181.4); (NA, -156.8); (-181.1, -207.1); (-176.6, -191.1); (-176.8, -201.7); (-113.9, -185.6); (-169.1, -252.1); (-144.3, -196.2); (-155.9, -228.5); (-152.9, -193.9); (-177.6, -193.2); (-172.1, -176.3); (-161.1, NA); (-154.7, -272.5); (-170.5, -202); (NA, -228.2); (-202.6, -186.9); (-190, -231.3); (-153.5, -218.8); (-126.8, -230.9); (-161.6, -195.9); (-161.6, -171.2); (-134.8, -181.4); (-175.3, -209.2); (-185.7, -232.3); (-180, -182.5); (-185.6, NA); (-192.5, -163.2); (-143.4, -174.7); (-186.7, -175.5); (-170, -226.1); (-151.1, -204.1); (-137.8, -205.7); (-150.2, -194); (-159.2, -212); (-171.3, -184.6); (-156.2, -189.5); (-186.5, -176.2); (-182.3, NA); (-165, -179.4); (NA, NA); (-139.8, -225.3); (-128.3, NA); (-175.6, -147); (NA, -191.8); (-166.9, -202.1); (-133, -181.2); (-188.9, -178.2); (-139.3, -160.9); (-207.1, -188); (NA, -183.4); (-166.4, -189.8); (-175.1, -206.8); (-164.1, -206.1); (-138.3, -226.5); (-130, -208); (-128.6, -192.8); (-167.7, -241); (-169.6, -171.3); (NA, -188.3); (-178.1, -197.4); (-163.7, -196.5); (-156.4, -210.3); (NA, -184.9); (-183.9, -213.4); (-136.7, -185.3); (-142, -175.1); (NA, -205.2); (-116.7, NA); (-173.9, NA); (-175.1, -185.2); (-148.7, -217.4); (-158.5, -197.2); (-165.3, -194.2); (NA, -179.3); (-199.7, -190.3); (-167.7, -160.5); (-157.2, -200.1); (-162.3, -181.8); (-160.6, -200.5); (-126.1, -197.1); (-151.8, -229.1); (-81.3, -165.8); (-183, -186.5); (-170.2, -160.7); (-161, -172.7); (-170.6, -206.8); (-185.3, -216.6); (-140, -191); (-132.8, -206.9); (-100.5, -231); (-180.9, -169.4); (NA, -221.7); (-165.1, -229.3); (-122.4, -225.5); (-168.3, -226.7); (-162.9, -203.6); (-147.4, -186.9); (-167.3, -179.1); (-149.5, -170.6); (-180.2, -208); (-139.8, -194); (-144.1, -145.8); (-134.9, -159.5); (NA, -212.5); (-149.2, -197.4); (-133.1, -199.8); (-145.5, -170.2); (-155.2, -170.7); (-178.2, -178.8); (-112.6, -204.6); (-122.3, NA); (-153.7, -149.1); (-156, -191.4); (-145.2, -167.5); (-134.5, -223.8); (-162.5, -213); (-151.9, -186.9); (-177.9, NA); (-176.9, -251.6); (-143.6, -141.1); (NA, NA); (-188.1, NA); (-156.8, -179.7); (-187.7, -209.6); (-135.5, -190.1); (-155.2, -215.3); (-129.9, -188.6); (-129.7, -190.8); (-141.2, -213.6); (-161.1, -208.4); (-132.9, -199.2); (-150.1, -241.5); (-211.1, -210.6); (-146.8, -171.3); (-203.2, -175.1); (-182.1, -185.8); (-133.9, -187.7); (-138.3, -170.6); (-176.4, -149.5); (-123.1, -193.2); (-137.5, -211.2); (-168.3, -186.9)"
	mass = "(NA, -174.102); (-179.48, -129.426); (NA, -158.889); (-194.668, -97.03); (-157.32, -160.724); (-158.761, -150.272); (-127.029, -133.668); (-123.598, -139.103); (-145.083, -168.8); (NA, -121.466); (-170.936, -164.921); (-161.44, -160.871); (-152.482, -142.145); (-125.868, -150.07); (-192.441, NA); (-165.582, -180.738); (-165.573, -163.864); (-136.898, -145.576); (-135.491, -171.931); (-135.369, -136.244); (-108.551, -185.335); (-155.689, -159.563); (-158.019, -139.997); (-178.351, NA); (-130.033, -131.453); (-130.4, -128.065); (NA, -173.944); (-199.537, -208.286); (-171.129, -141.653); (-144.684, -128.506); (-157.331, -174.296); (-161.25, -122.913); (-194.853, -148.95); (-184.039, -83.218); (-100.519, -147.823); (-160.395, NA); (-109.877, -187.794); (-130.906, -114.443); (-172.584, -146.455); (-203.736, -174.973); (-98.893, -108.375); (-126.059, -172.227); (-144.93, -199.092); (-165.564, NA); (-138.398, -123.084); (NA, -184.882); (-234.163, -111.826); (-188.612, -138.542); (NA, -158.449); (-155.805, -156.92); (-191.165, -152.546); (-197.453, -176.825); (-173.634, -170.843); (-172.605, -168.667); (-160.873, -126.11); (-190.225, -170.229); (-149.667, -132.897); (-157.191, -149.562); (-165.689, -178.878); (-156.725, -189.328); (-114.787, NA); (-119.408, -127.44); (-152.09, -158.071); (-185.13, -168.875); (-124.985, -164.608); (-149.437, -150.703); (-165.668, -151.831); (-121.266, NA); (-165.192, -117.263); (-111.794, -150.796); (NA, -180.478); (-126.524, -146.629); (-160.371, -158.34); (-155.153, NA); (-114.043, -181.417); (NA, -157.939); (-167.823, -164.38); (-153.068, -180.277); (-196.64, -153.317); (-171.852, -156.708); (-121.631, -135.335); (-193.257, -124.17); (NA, -148.544); (-143.781, -115.777); (-156.901, -148.36); (-150.25, NA); (-156.881, -129.439); (-192.216, -154.506); (-158.263, -187.301); (-163.899, -140.697); (-173.411, -163.619); (-187.182, -110.525); (NA, -157.498); (NA, -194.494); (-127.452, -211.864); (-106.425, NA); (-104.917, -171.497); (-111.142, NA); (-142.866, -163.407); (-189.017, -174.446); (-136.368, NA); (-167.332, -144.178); (-145.601, -155.85); (-153.626, -90.861); (-151.916, -158.759); (-169.151, -121.104); (-142.967, -118.166); (-104.499, NA); (-145.582, -135.673); (-151.966, -125.859); (-177.418, -145.067); (-202.059, -186.102); (-122.2, -120.311); (-185.807, -129.329); (-149.525, -176.557); (-115.868, -122.966); (-151.091, -201.466); (-124.62, -146.383); (NA, -105.329); (-166.647, -141.906); (-154.52, NA); (-116.088, -143.585); (-175.783, -128.663); (-172.555, NA); (-188.051, -193.345); (-119.612, -135.115); (-189.482, -200.818); (-155.975, -129.086); (-140.359, -132.182); (NA, -217.857); (-155.51, -125.426); (-137.212, -169.906); (-140.201, -163.328); (-131.168, -192.921); (-189.599, -155.876); (-141.161, NA); (-186.086, -146.938); (-175.102, -178.516); (-126.059, -117.799); (-199.634, -168.117); (-149.544, -146.684); (-150.509, -146.56); (-139.353, -163.501); (-115.095, -159.429); (NA, -172.768); (-109.021, NA); (-172.726, -135.953); (-170.115, -172.592); (-135.417, -186.833); (-182.898, -143.638)"
	variant_task3 = input('varik?\n1-2?\n')
	lvl_1 = input('lvl 1?\n')
	lvl_2 = input('lvl 2?\n')
	worksheet = workbook.add_worksheet()
	task3(worksheet, mass, variant_task3, lvl_1, lvl_2)
	workbook.close()


main()
