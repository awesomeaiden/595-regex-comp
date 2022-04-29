import pandas
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
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

		data[method]['match'] = get_data(df, method_filter + filter_match, 'numUserNewDataToTool', remove_over_150_conversion_func)
		data[method]['create'] = get_data(df, method_filter + filter_create, 'numUserNewDataToTool', remove_over_150_conversion_func)
		data[method]['change'] = get_data(df, method_filter + filter_update, 'numUserNewDataToTool', remove_over_150_conversion_func)
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
	fig.subplots_adjust(left=0.08, bottom=0.074, right=0.97, top=0.94, wspace=0.21, hspace=0.264)
	rects_regexr   = ax.bar(x - width, task_regexr, width, label='Regexr')
	rects_regexper = ax.bar(x, task_regexper, width, label='Regexper')
	rects_grex     = ax.bar(x + width, task_grex, width, label='Grex')

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Average Number of Interactions')
	ax.set_title('')
	ax.set_xticks(x, labels)
	ax.legend(loc='best')

	ax.bar_label(rects_regexr, fmt="")
	ax.bar_label(rects_regexper, fmt="")
	ax.bar_label(rects_grex, fmt="")

	fig.tight_layout()

	#plt.show()
	plt.savefig('plots/grouped_bar_method_vs_interactions.png')

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
	fig.subplots_adjust(left=0.08, bottom=0.074, right=0.97, top=0.94, wspace=0.21, hspace=0.264)
	rects_control  = ax.bar(x - (3 * width / 2), task_times_control, width, label='Control')
	rects_regexr   = ax.bar(x - (1 * width / 2), task_times_regexr, width, label='Regexr')
	rects_regexper = ax.bar(x + (1 * width / 2), task_times_regexper, width, label='Regexper')
	rects_grex     = ax.bar(x + (3 * width / 2), task_times_grex, width, label='Grex')

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Average Time (s)')
	ax.set_xticks(x, labels)
	ax.legend(loc='best')

	ax.bar_label(rects_control, fmt="")
	ax.bar_label(rects_regexr, fmt="")
	ax.bar_label(rects_regexper, fmt="")
	ax.bar_label(rects_grex, fmt="")

	fig.tight_layout()

	#plt.show()
	plt.savefig('plots/grouped_bar_method_vs_time.png')


def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

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

	def plot_circles(xs, ys, axis, **kwargs):
		sizes = np.zeros((max(xs)+1, max(ys)+1))
		sizes[0][0] = 1
		for i, x in enumerate(xs):
			sizes[x][ys[i]] += 1

		for i in range(len(sizes)):
			for j in range(len(sizes[i])):
				if sizes[i][j] > 0:
					circle = plt.Circle((i, j), sizes[i][j]*.05, **kwargs)
					axis.add_patch(circle)


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


	fig, ax = plt.subplots(2, 2, figsize=(10, 8))
	fig.subplots_adjust(left=0.08, bottom=0.074, right=0.97, top=0.94, wspace=0.21, hspace=0.264)

	axis = ax[1][1]
	axis.plot([0, 0], [-99, 99], '-', color='0.6', label='_nolegend_')
	axis.plot([-99, 99], [0, 0], '-', color='0.6', label='_nolegend_')
	axis.set_xlabel('Number of Interactions')
	axis.set_ylabel('Number Times Looked\nat Cheat Sheet')
	axis.set_title('All')
	axis.set_xlim(-1, 7.3)
	axis.set_ylim(-1, 9)

	std=1.0
	axis = ax[0][0]
	xs = np.array(data['regexr']['num_new_data'])
	ys = np.array(data['regexr']['num_flips'])
	plot_circles(xs, ys, axis)
	axis.plot(xs, ys, '.', color='#1f77b4')
	confidence_ellipse(xs, ys, axis, n_std=std, edgecolor='#1f77b4', linestyle='--')
	confidence_ellipse(xs, ys, ax[1][1], n_std=std, edgecolor='#1f77b4', linestyle='--')
	axis.set_title('Regexr')
	axis.set_xlabel('Number of Interactions')
	axis.set_ylabel('Number Times Looked\nat Cheat Sheet')
	axis.set_xlim(-1, 9)
	axis.set_ylim(-1, 9)

	axis = ax[0][1]
	xs = np.array(data['regexper']['num_new_data'])
	ys = np.array(data['regexper']['num_flips'])
	plot_circles(xs, ys, axis, color='#ff7f0e')
	confidence_ellipse(xs, ys, axis, n_std=std, edgecolor='#ff7f0e', linestyle='--')
	confidence_ellipse(xs, ys, ax[1][1], n_std=std, edgecolor='#ff7f0e', linestyle='--')
	axis.set_title('Regexper')
	axis.set_xlabel('Number of Interactions')
	axis.set_ylabel('Number Times Looked\nat Cheat Sheet')
	axis.set_xlim(-1, 9)
	axis.set_ylim(-1, 9)

	axis = ax[1][0]
	xs = np.array(data['grex']['num_new_data'])
	ys = np.array(data['grex']['num_flips'])
	plot_circles(xs, ys, axis, color='#2ca02c')
	confidence_ellipse(xs, ys, axis, n_std=std, edgecolor='#2ca02c', linestyle='--')
	confidence_ellipse(xs, ys, ax[1][1], n_std=std, edgecolor='#2ca02c', linestyle='--')
	axis.set_title('Grex')
	axis.set_xlabel('Number of Interactions')
	axis.set_ylabel('Number Times Looked\nat Cheat Sheet')
	axis.set_xlim(-1, 9)
	axis.set_ylim(-1, 9)

	ax[1][1].legend(['Regexr', 'Regexper', 'Grex'])

	#plt.show()
	plt.savefig('plots/cheat_sheet_vs_num_interactions.png')

def other_stats(df):
	fil = dict()
	fil['control'] = [('context', re.compile(r"control."))]
	fil['regexr'] = [('context', re.compile(r"explain."))]
	fil['regexper'] = [('context', re.compile(r"automata."))]
	fil['grex'] = [('context', re.compile(r"grex."))]

	filter_match = [('questionName', re.compile(r"string."))]
	filter_create = [('questionName', re.compile(r"create."))]
	filter_update = [('questionName', re.compile(r"update."))]

	data = get_data(df, fil['regexper']+filter_match, 'numUserNewDataToTool')
	print(data)
	print(len(data))

def main():
	df = pandas.read_csv('survey_data.csv')
	
	#grouped_bar_method_vs_num_interactions(df)
	#grouped_bar_method_vs_time(df)
	flips_to_cheat_sheet_vs_num_interactions(df)

	#other_stats(df)


if __name__ == "__main__":
	main()

