import pandas
import matplotlib.pyplot as plt
import numpy as np
import re

TASK_TYPE_CREATE_STR = 1
TASK_TYPE_CREATE_REGEX = 2
TASK_TYPE_UPDATE_REGEX = 2

def discard_non_int_conversion_func(data_pt):
	try:
		data_pt = int(data_pt)
	except ValueError:
		data_pt = None

	return data_pt

def matches_filter(row, filters):
	for fil in filters:
		if fil[1].match(row[fil[0]]) is None:
			return False
	return True

def get_data(df, filters, output_column, conversion_func=None):
	data = list()
	for index, row in df.iterrows():
		if matches_filter(row, filters):
			data_pt = row[output_column]
			if conversion_func is not None:
				data_pt = conversion_func(data_pt)

			if data_pt is not None:
				data.append(data_pt)

	return data

def grouped_bar_method_vs_time(df):
	def get_data_dict():
		return {
			'match_str': list(),
			'create_regex': list(),
			'change_regex': list()
		}

	data = dict()
	data['control'] = get_data_dict()
	data['regexr'] = get_data_dict()
	data['regexper'] = get_data_dict()
	data['grex'] = get_data_dict()

	labels = ['Write a Matching String', 'Create a Regex', 'Change a Regex']
	task_times_control = [20, 34, 30]
	task_times_regexr = [25, 32, 34]
	task_times_regexper = [32, 28, 25]
	task_times_grex = [22, 35, 30]

	x = np.arange(len(labels)) * 5 + 3 # the label locations
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




def main():
	df = pandas.read_csv('survey_data.csv')
	fil = [('questionName', re.compile(r"string."))]
	print(get_data(df, fil, 'numUserNewDataToTool', conversion_func=discard_non_int_conversion_func))

	grouped_bar_method_vs_time(df)




if __name__ == "__main__":
	main()

