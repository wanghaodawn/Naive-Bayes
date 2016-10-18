
import sys
from sys import argv
import math

# Count the overall unique words
global Vocabulary, dic_vocabulary
Vocabulary = 0
dic_vocabulary = {}

# Count the number and possibility of lib or con documents
global num_lib_doc, num_con_doc, p_lib_doc, p_con_doc
num_lib_doc = 0
num_con_doc = 0
p_con_doc = 0.0
p_lib_doc = 0.0

# Check whether a word appears and the value is the number of occurance
global dic_lib_train, dic_con_train
dic_lib_train = {} 
dic_con_train = {}

# Count the overall amout of words in con and lib
global N_con_words, N_lib_words
N_lib_words = 0
N_con_words = 0



def main():

	# Declare global variables
	global Vocabulary, num_lib_doc, num_con_doc, dic_lib_train, dic_con_train
	global p_lib_doc, p_con_doc, N_con_words, N_lib_words

	# 1st argv is this python filename, 2nd argv is train, 3rd argv is test
	# Might misssing 3rd argv

	# Get file names
	train_file_name = sys.argv[1]

	# Read training data
	read_train_data(train_file_name)

	if (num_lib_doc + num_con_doc) == 0:
		print("Number of both lib and con is 0!")
		exit(-1)

	p_lib_doc = math.log(num_lib_doc * 1.0 / (num_lib_doc + num_con_doc))
	p_con_doc = math.log(num_con_doc * 1.0 / (num_lib_doc + num_con_doc))

	# Get the overall number of dics
	for key in dic_con_train:
		N_con_words += dic_con_train[key]
	for key in dic_lib_train:
		N_lib_words += dic_lib_train[key]

	# print(N_con_words)
	# print(N_lib_words)
	# print(dic_lib_train)
	# print(dic_con_train)
	# print(len(dic_lib_train.keys()))
	# print(Vocabulary)

	# Change the value of dics from number to possibilities
	# To make it easier to compute, just save the log value
	non_con = math.log(1.0) - math.log(N_con_words + Vocabulary)
	for key in dic_vocabulary:
		if dic_con_train.has_key(key):
			dic_con_train[key] = math.log(dic_con_train[key] + 1.0) - math.log(N_con_words + Vocabulary)
		else:
			dic_con_train[key] = non_con
		# print(key + ": " + str(dic_new_con[key]))
	non_lib = math.log(1.0) - math.log(N_lib_words + Vocabulary)
	for key in dic_vocabulary:
		if dic_lib_train.has_key(key):
			dic_lib_train[key] = math.log(dic_lib_train[key] + 1.0) - math.log(N_lib_words + Vocabulary)
		else:
			dic_lib_train[key] = non_lib

	# Get the top 20 words and print
	i = 0
	for key in sorted(dic_lib_train, key = dic_lib_train.get, reverse = True):
		if i < 20:
			temp = math.exp(dic_lib_train[key])
			temp = round(temp, 4)
			print(key + " " + str(temp))
			i += 1
		else:
			break

	print("")

	i = 0
	for key in sorted(dic_con_train, key = dic_con_train.get, reverse = True):
		if i < 20:
			temp = math.exp(dic_con_train[key])
			temp = round(temp, 4)
			print(key + " " + str(temp))
			i += 1
		else:
			break




# read drom training data
def read_train_data(filename):

	# Declare global variables
	global num_con_doc, num_lib_doc

	f = open(filename, 'r')
	
	while 1:
		line = str(f.readline()).strip()
		if not line:
			break

		# If the filename contains lib
		if line.find("lib") != -1:
			num_lib_doc += 1
			read_train_file(line, 0)
		
		# If the filename contains con
		elif line.find("con") != -1:
			num_con_doc += 1
			read_train_file(line, 1)

		# Illegal filename, continue
		else:
			continue



# Read files, if option == 0, then means it is reading lib training data
# 			  if option == 1, then means it is reading con training data
def read_train_file(filename, option):

	# Declare global variables
	global dic_lib_train, dic_con_train, Vocabulary, dic_vocabulary

	f = open(filename, 'r')

	while 1:
		line = str(f.readline()).strip()
		if not line:
			break

		line = line.lower()

		# Update vocabulary and its dictionary
		if not dic_vocabulary.has_key(line):
			dic_vocabulary[line] = 1
			Vocabulary += 1

		# Reading training lib data now
		if option == 0:
			if not dic_lib_train.has_key(line):
				dic_lib_train[line] = 1
			else:
				dic_lib_train[line] = dic_lib_train[line] + 1

		# Reading training con data now
		elif option == 1:
			if not dic_con_train.has_key(line):
				dic_con_train[line] = 1
			else:
				dic_con_train[line] = dic_con_train[line] + 1

		# Illegal option
		else:
			print("ERROR: Illegal option in read_lib_file")
			exit(-1)



if __name__ == "__main__":
	main()
