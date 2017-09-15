import os
import sys
from datetime import datetime

root_directory = "."
directories_to_compare = []
file_extension_to_directory_mapping = {}

expected_arguments = ["-m", "-c"]
expected_options = ["--pnr", "--ocli"]


def get_file_names(root_directory):
	files = []
	for path, directories, files in os.walk(root_directory):
		#print("path:", path, "\ndirectories:", directories, "\nfiles:", files, "\n")
		for file in files:
			#print(os.path.join(path, file) + "\n")
			files.append(os.path.join(path, file))
	return files

def move_files_based_on_extension(files, file_extension_to_directory_mapping):
	for file in files:
		file_name, file_extension = os.path.splitext(file) 

		if file_extension in file_extension_to_directory_mapping:
			os.rename(file, os.path.join(file_extension_to_directory_mapping[file_extension], file_name))
		else:
			if "default_folder" in file_extension_to_directory_mapping:
				os.rename(file, os.path.join(file_extension_to_directory_mapping["default_folder"], file_name))

def print_manual():
	manual = []
	with open("manual.txt") as f:
		manual = f.readlines()

	for line in manual:
		print(line + "\n")

def write_results_to_file(source_directory, destination_directory, results):
	output_file_name = os.path.basename(source_directory) + "_" + os.path.basename(destination_directory) + "_" + str(datetime.now()) + ".txt"
	f.open(output_file_name)

	for result in results:
		f.write(results + "\n")
	f.close()


def check_file_repetition(source_directory, destination_directory, print_not_repeated = False, output_to_file = True):
	source_directory_files = get_file_names(source_directory)
	destination_directory_files = get_file_names(destination_directory)

	results = []

	for file in source_directory_files:
		if file in destination_directory_files and not print_not_repeated:
			results.append(file)
		else file not in destination_directory_files and print_not_repeated:
			results.append(file)

	if output_to_file:
		write_results_to_file(results)
	else: 
		for result in results:
			print(result + "\n")


def contains_valid_argument(expected_arguments, arguments):
	return not set(expected_arguments).isdisjoint(arguments)

def set_file_extension_to_directory_mapping_from_arg_string(arg_string):
	# format: "pdf:/home/auser/dir1/;docx,pptx:/home/auser/dir2/"
	mapping_strings_list = arg_string.split(";")
	for mapping_strings in mapping_strings_list:
		extensions_dir_list = mapping_strings.split(":")
		extenstions = extensions_dir_list[0].split(",")
		directory = extensions_dir_list[1]
		for extension in extenstions:
			file_extension_to_directory_mapping[extension] = directory


# TODO
if contains_valid_argument(expected_arguments, sys.argv):
	try:
		args = sys.argv
		for arg_pos in range(len(args)):
			arg = args[arg_pos]
			if arg == "-m":
				root_directory = args[arg_pos + 1]
				set_file_extension_to_directory_mapping_from_arg_string(args[arg_pos + 2])
				move_files_based_on_extension(get_file_names(root_directory), file_extension_to_directory_mapping)
			elif arg == "-c":
				root_directory = args[arg_pos + 1]
				# formt: /home/auser/dir1/;/home/auser/dir2/
				directories_to_compare = args[arg_pos + 2].split(";")
				print_not_repeated = True if "--pnr" in args else False
				output_to_file = False if "--ocli" in args else True
				for destination_directory in directories_to_compare:
					check_file_repetition(source_directory, destination_directory, print_not_repeated, output_to_file)
	except:
		print("There was an error: ", sys.exc_info()[0])
else:
	print_manual()










