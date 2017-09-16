import os
import sys
import traceback
from datetime import datetime

root_directory = "."
directories_to_compare = []
file_extension_to_directory_mapping = {}

expected_arguments = ["-m", "-c"]
expected_options = ["--pnr", "--ocli"]


def get_file_names(root_directory):
	file_names = []
	for path, directories, files in os.walk(root_directory):
		#print("path:", path, "\ndirectories:", directories, "\nfiles:", files, "\n")
		for file in files:
			#print(os.path.join(path, file) + "\n")
			file_names.append(os.path.join(path, file))
	return file_names

def move_files_based_on_extension(files, file_extension_to_directory_mapping):
	for file in files:
		#print(file)
		file_name, file_extension = os.path.splitext(file)
		file_extension = file_extension.replace(".", "")
		#print(file_name)
		#print(file_extension.replace(".", ""))

		if file_extension in file_extension_to_directory_mapping:
			#print("Found ya!!!")
			file_extension_to_directory_mapping[file_extension]
			#print(os.path.join(file_extension_to_directory_mapping[file_extension], os.path.basename(file)))
			os.rename(file, os.path.join(file_extension_to_directory_mapping[file_extension], os.path.basename(file)))
		else:
			#print("Not what we want!")
			if "default_folder" in file_extension_to_directory_mapping:
				#print("default_folder set")
				os.rename(file, os.path.join(file_extension_to_directory_mapping["default_folder"], os.path.basename(file)))

def print_manual():
	manual = []
	with open("manual.txt") as f:
		manual = f.readlines()

	for line in manual:
		print(line)

def write_results_to_file(results, result_is_list = False):
	#output_file_name = os.path.basename(source_directory) + "_" + os.path.basename(destination_directory) + "_" + str(datetime.now()) + ".txt"
	output_file_name = str(datetime.now()) + ".txt"
	f = open(output_file_name, "w")

	for result in results:
		if result_is_list:
			f.write(result[0] + "  <=>  " + result[1] + "\n")
		else:
			f.write(results + "\n")
	f.close()

def print_results(results, result_is_list = False):
	for result in results:
		if result_is_list:
			print(result[0] + "  <=>  " + result[1])
		else:
			print(result)


def check_file_repetition(source_directory, destination_directory, print_not_repeated = False, output_to_file = True):
	source_directory_files = get_file_names(source_directory)
	destination_directory_files = get_file_names(destination_directory)

	repeated_files = []
	unique_files = []

	for origin_file in source_directory_files:
		repeated = False

		for destination_file in destination_directory_files:
			#print(origin_file, destination_file)
			origin_file_basename = os.path.basename(origin_file)
			destination_file_basename = os.path.basename(destination_file)
			#print(origin_file_basename, destination_file_basename)
			if origin_file_basename == destination_file_basename:
				#print("Repeated")
				repeated_files.append([origin_file, destination_file])
				repeated = True
		
		if not repeated:
			unique_files.append(origin_file)

	if output_to_file:
		if print_not_repeated:
			write_results_to_file(unique_files)
		else:
			write_results_to_file(repeated_files, True)
	else: 
		if print_not_repeated:
			print_results(unique_files)
		else:
			print_results(repeated_files, True)


def contains_valid_argument(expected_arguments, arguments):
	return not set(expected_arguments).isdisjoint(arguments)

def set_file_extension_to_directory_mapping_from_arg_string(arg_string):
	# format: "pdf:/home/auser/dir1/?docx,pptx:/home/auser/dir2/"
	mapping_strings_list = arg_string.split("?")
	#print(mapping_strings_list)
	for mapping_strings in mapping_strings_list:
		extensions_dir_list = mapping_strings.split(":")
		extenstions = extensions_dir_list[0].split(",")
		directory = extensions_dir_list[1]
		#print(mapping_strings, extensions_dir_list, extenstions, directory)
		for extension in extenstions:
			#print(extension)
			file_extension_to_directory_mapping[extension] = directory


# TODO
if contains_valid_argument(expected_arguments, sys.argv):
	try:
		args = sys.argv
		for arg_pos in range(len(args)):
			arg = args[arg_pos]
			if arg == "-m":
				#print("Moviiiing!!!")
				root_directory = args[arg_pos + 1]
				set_file_extension_to_directory_mapping_from_arg_string(args[arg_pos + 2])
				#print(file_extension_to_directory_mapping)
				move_files_based_on_extension(get_file_names(root_directory), file_extension_to_directory_mapping)
			elif arg == "-c":
				root_directory = args[arg_pos + 1]
				# format: /home/auser/dir1/?/home/auser/dir2/
				directories_to_compare = args[arg_pos + 2].split("?")
				print_not_repeated = True if "--pnr" in args else False
				output_to_file = False if "--ocli" in args else True
				for destination_directory in directories_to_compare:
					check_file_repetition(root_directory, destination_directory, print_not_repeated, output_to_file)
	except:
		#print("There was an error: ", sys.exc_info()[0])
		traceback.print_exc()
else:
	print_manual()










