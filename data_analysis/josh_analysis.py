import pandas
import matplotlib.pyplot as plt
import numpy as np
import re

from util import *

def grouped_bar_method_vs_num_interactions(df):
	def get_data_dict():
		return {
			'match': list(),
			'create': list(),
			'change': list()
		}

	data = dict()

	fil = dict()
	fil['regexr'] = [('context', re.compile(r"explain."))]
	fil['regexper'] = [('context', re.compile(r"automata."))]
	fil['grex'] = [('context', re.compile(r"grex."))]
	filter_match = [('questionName', re.compile(r"string."))]
	filter_create = [('questionName', re.compile(r"create."))]
	filter_update = [('questionName', re.compile(r"update."))]

	for method in ['regexr', 'regexper', 'grex']:
		data[method] = get_data_dict()
		method_filter = fil[method]

		data[method]['match'] = get_data(df, method_filter + filter_match, 'numUserNewDataToTool', reduce_to_150_conversion_func)
		data[method]['create'] = get_data(df, method_filter + filter_create, 'numUserNewDataToTool', reduce_to_150_conversion_func)
		data[method]['change'] = get_data(df, method_filter + filter_update, 'numUserNewDataToTool', reduce_to_150_conversion_func)
		data[method]['match'] = round(np.mean(data[method]['match']), 2)
		data[method]['create'] = round(np.mean(data[method]['create']), 2)
		data[method]['change'] = round(np.mean(data[method]['change']), 2)


	labels = ['Write a Matching String', 'Create a Regex', 'Change a Regex']
	task_regexr = [data['regexr']['match'], data['regexr']['create'], data['regexr']['change']]
	task_regexper = [data['regexper']['match'], data['regexper']['create'], data['regexper']['change']]
	task_grex = [data['grex']['match'], data['grex']['create'], data['grex']['change']]

	x = np.arange(len(labels)) * 5 # the label locations
	width = 1  # the width of the bars

	fig, ax = plt.subplots()
	rects_regexr   = ax.bar(x - width, task_regexr, width, label='Regexr')
	rects_regexper = ax.bar(x, task_regexper, width, label='Regexper')
	rects_grex     = ax.bar(x + width, task_grex, width, label='Grex')

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Average Number of Interactions')
	ax.set_title('')
	ax.set_xticks(x, labels)
	ax.legend(loc='best')

	padding = 1
	ax.bar_label(rects_regexr, padding=padding)
	ax.bar_label(rects_regexper, padding=padding)
	ax.bar_label(rects_grex, padding=padding)

	fig.tight_layout()

	plt.show()

def grouped_bar_method_vs_time(df):
	def get_data_dict():
		return {
			'match': list(),
			'create': list(),
			'change': list()
		}

	data = dict()

	fil = dict()
	fil['control'] = [('context', re.compile(r"control."))]
	fil['regexr'] = [('context', re.compile(r"explain."))]
	fil['regexper'] = [('context', re.compile(r"automata."))]
	fil['grex'] = [('context', re.compile(r"grex."))]
	filter_match = [('questionName', re.compile(r"string."))]
	filter_create = [('questionName', re.compile(r"create."))]
	filter_update = [('questionName', re.compile(r"update."))]

	for method in ['control', 'regexr', 'regexper', 'grex']:
		data[method] = get_data_dict()
		method_filter = fil[method]

		data[method]['match'] = get_data(df, method_filter + filter_match, 'timeToComplete', reduce_to_150_conversion_func)
		data[method]['create'] = get_data(df, method_filter + filter_create, 'timeToComplete', reduce_to_150_conversion_func)
		data[method]['change'] = get_data(df, method_filter + filter_update, 'timeToComplete', reduce_to_150_conversion_func)
		data[method]['match'] = round(np.mean(data[method]['match']), 1)
		data[method]['create'] = round(np.mean(data[method]['create']), 1)
		data[method]['change'] = round(np.mean(data[method]['change']), 1)


	labels = ['Write a Matching String', 'Create a Regex', 'Change a Regex']
	task_times_control = [data['control']['match'], data['control']['create'], data['control']['change']]
	task_times_regexr = [data['regexr']['match'], data['regexr']['create'], data['regexr']['change']]
	task_times_regexper = [data['regexper']['match'], data['regexper']['create'], data['regexper']['change']]
	task_times_grex = [data['grex']['match'], data['grex']['create'], data['grex']['change']]

	x = np.arange(len(labels)) * 5 # the label locations
	width = 1  # the width of the bars

	fig, ax = plt.subplots()
	rects_control  = ax.bar(x - (3 * width / 2), task_times_control, width, label='Control')
	rects_regexr   = ax.bar(x - (1 * width / 2), task_times_regexr, width, label='Regexr')
	rects_regexper = ax.bar(x + (1 * width / 2), task_times_regexper, width, label='Regexper')
	rects_grex     = ax.bar(x + (3 * width / 2), task_times_grex, width, label='Grex')

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Average Time (s)')
	ax.set_title('')
	ax.set_xticks(x, labels)
	ax.legend(loc='best')

	padding = 1
	ax.bar_label(rects_control, padding=padding)
	ax.bar_label(rects_regexr, padding=padding)
	ax.bar_label(rects_regexper, padding=padding)
	ax.bar_label(rects_grex, padding=padding)

	fig.tight_layout()

	plt.show()

def flips_to_cheat_sheet_vs_num_interactions(df):
	methods = ['regexr', 'regexper', 'grex']
	def get_data_dict():
		return {
			'num_flips': list(),
			'num_new_data': list()
		}

	def clean_row(row):
		num_flips = row['numFlipsToCheatSheet']
		num_new_data = row['numUserNewDataToTool']
		num_flips = discard_non_int_conversion_func(num_flips)
		num_new_data = discard_non_int_conversion_func(num_new_data)

		if num_flips is None or num_new_data is None:
			return None
		else:
			return (num_new_data, num_flips)

	fil = dict()
	fil['regexr'] = [('context', re.compile(r"explain."))]
	fil['regexper'] = [('context', re.compile(r"automata."))]
	fil['grex'] = [('context', re.compile(r"grex."))]
	
	data = dict()
	for method in methods:
		data[method] = get_data_dict()

		rows = get_rows(df, fil[method])

		for i, row in enumerate(rows):
			fixed_row = clean_row(row)
			if fixed_row is None:
				pass
			else:
				data[method]['num_new_data'].append(fixed_row[0])
				data[method]['num_flips'].append(fixed_row[1])


	fig, ax = plt.subplots()

	for method in methods:
		xs = data[method]['num_new_data']
		ys = data[method]['num_flips']
		ax.plot(xs, ys, 'o')

	ax.legend(methods)
	ax.set_xlabel('Number of Interactions')
	ax.set_ylabel('Number of Cheat Sheet Usages')

	plt.show()



def main():
	df = pandas.read_csv('survey_data.csv')
	fil = [('questionName', re.compile(r"string."))]
	#print(get_data(df, fil, 'numUserNewDataToTool', conversion_func=discard_non_int_conversion_func))
	
	fil = [('questionName', re.compile(r"create."))]
	#print(get_data(df, fil, 'numUserNewDataToTool', conversion_func=discard_non_int_conversion_func))

	grouped_bar_method_vs_num_interactions(df)
	grouped_bar_method_vs_time(df)
	flips_to_cheat_sheet_vs_num_interactions(df)



if __name__ == "__main__":
	main()

