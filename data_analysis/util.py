import pandas
import numpy as np
import re


def discard_non_int_conversion_func(data_pt):
	try:
		data_pt = int(data_pt)
	except ValueError:
		data_pt = None

	return data_pt

def reduce_to_150_conversion_func(data_pt):
	data_pt = discard_non_int_conversion_func(data_pt)

	if data_pt is None or data_pt >= 150:
		return None

	data_pt = min(150, data_pt)

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

def get_rows(df, filters):
	rows = list()
	for index, row in df.iterrows():
		if matches_filter(row, filters):
			rows.append(row)

	return rows