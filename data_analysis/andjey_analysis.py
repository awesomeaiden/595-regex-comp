import pandas
import matplotlib.pyplot as plt
import numpy as np
import re

from util import *


def plot_understanding_groups(df, df_demo):
	groups = ['all', 'advanced', 'beginner']
	methods = ['control', 'regexr', 'regexper', 'grex']

	data = {
		'advanced': dict(),
		'beginner': dict(),
		'all': dict()
	}

	advanced_filter = [('algorithm_experienced_or_beginner', re.compile(r'advanced'))]
	beginner_filter = [('algorithm_experienced_or_beginner', re.compile(r'beginner'))]
	advanced_ids = get_data(df_demo, advanced_filter, 'pID', None)
	beginner_ids = get_data(df_demo, beginner_filter, 'pID', None)
	all_ids = advanced_ids + beginner_ids

	pIDs = {
		'all': all_ids,
		'advanced': advanced_ids,
		'beginner': beginner_ids
	}

	fil = dict()
	fil['control'] = [('context', re.compile(r"control."))]
	fil['regexr'] = [('context', re.compile(r"explain."))]
	fil['regexper'] = [('context', re.compile(r"automata."))]
	fil['grex'] = [('context', re.compile(r"grex."))]

	for group in groups:
		for method in methods:
			method_filter = fil[method]
			understanding_pts = list()
			for pID in pIDs[group]:
				pid_filter = id_filter = [('pID', re.compile("%s" % pID))]
				understanding_pts += get_data(df, method_filter+pid_filter, 'Understanding Metric', discard_non_float_conversion_func)
			
			data[group][method] = np.mean(understanding_pts)

	labels = ['All', 'Advanced', 'Beginner']
	understanding_control = [data[group]['control'] for group in groups]
	understanding_regexr = [data[group]['regexr'] for group in groups]
	understanding_regexper = [data[group]['regexper'] for group in groups]
	understanding_grex = [data[group]['grex'] for group in groups]

	x = np.arange(len(labels)) * 5 # the label locations
	width = 1  # the width of the bars

	fig, ax = plt.subplots()
	fig.subplots_adjust(left=0.08, bottom=0.074, right=0.97, top=0.94, wspace=0.21, hspace=0.264)
	rects_control  = ax.bar(x - (3 * width / 2), understanding_control, width, label='Control')
	rects_regexr   = ax.bar(x - (1 * width / 2), understanding_regexr, width, label='Regexr')
	rects_regexper = ax.bar(x + (1 * width / 2), understanding_regexper, width, label='Regexper')
	rects_grex     = ax.bar(x + (3 * width / 2), understanding_grex, width, label='Grex')

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Understanding Metric')
	ax.set_xticks(x, labels)
	ax.legend(loc='best')

	padding = 1
	ax.bar_label(rects_control, fmt="")
	ax.bar_label(rects_regexr, fmt="")
	ax.bar_label(rects_regexper, fmt="")
	ax.bar_label(rects_grex, fmt="")
	fig.tight_layout()

	plt.savefig('plots/understanding_by_groups.png')


def plot_each_participant_understanding(df):
	methods = ['control', 'regexr', 'regexper', 'grex']
	unique_ids = get_unique_ids(df)

	fil = dict()
	fil['control'] = [('context', re.compile(r"control."))]
	fil['regexr'] = [('context', re.compile(r"explain."))]
	fil['regexper'] = [('context', re.compile(r"automata."))]
	fil['grex'] = [('context', re.compile(r"grex."))]
	
	data = dict()
	for unique_id in unique_ids:
		data[unique_id] = dict()
		id_filter = [('pID', re.compile("%s" % unique_id))]
		
		for method in methods:
			data[unique_id][method] = None
			rows = get_data(df, id_filter + fil[method], 'Understanding Metric', discard_non_float_conversion_func)
			data[unique_id][method] = np.mean(rows)

	# Get control data for each participant ID
	understanding_control = [data[pID]['control'] for pID in unique_ids]
	# Get regexr data for each participant ID
	understanding_regexr = [data[pID]['regexr'] for pID in unique_ids]
	# Get regexper data for each participant ID
	understanding_regexper = [data[pID]['regexper'] for pID in unique_ids]
	# Get grex data for each participant ID
	understanding_grex = [data[pID]['grex'] for pID in unique_ids]

	fig, ax = plt.subplots(figsize=(10, 5))
	
	x = np.arange(len(unique_ids)) * 5 # the label locations
	width = .75  # the width of the bars

	rects_control  = ax.bar(x - (3 * width / 2), understanding_control, width, label='Control')
	rects_regexr   = ax.bar(x - (1 * width / 2), understanding_regexr, width, label='Regexr')
	rects_regexper = ax.bar(x + (1 * width / 2), understanding_regexper, width, label='Regexper')
	rects_grex     = ax.bar(x + (3 * width / 2), understanding_grex, width, label='Grex')

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_xlabel('Participants')
	ax.set_ylabel('Average Understanding')
	ax.legend(loc='best')
	ax.set_xticks([])

	ax.bar_label(rects_control, fmt="")	
	ax.bar_label(rects_regexr, fmt="")
	ax.bar_label(rects_regexper, fmt="")
	ax.bar_label(rects_grex, fmt="")
	
	fig.tight_layout()
	#plt.show()
	plt.savefig("plots/understanding_foreach_participant.png")

def test():
	df = pandas.read_csv('survey_data.csv')
	unique_ids = get_unique_ids(df)
	print(unique_ids[0])
	regex = re.compile("%s" % unique_ids[0])
	print(regex.match('65d47775-44b1-4950-a18d-4193bd2552da'))
	
	id_filter = [('pID', re.compile("%s" % unique_ids[0]))]
	data = get_data(df, id_filter, 'Understanding Metric', discard_non_float_conversion_func)

	print(data)

def main():
	#test()
	df = pandas.read_csv('survey_data.csv')
	df_demo = pandas.read_csv('survey_demographics_data.csv')

	#plot_each_participant_understanding(df)

	plot_understanding_groups(df, df_demo)


if __name__ == "__main__":
	main()

