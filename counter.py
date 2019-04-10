from os import listdir
from os.path import isdir, isfile, join
from optparse import OptionParser
import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


def get_name(extension):
    if extension == 'js' or extension == 'es6':
        return "JavaScript"
    elif extension == 'jsx':
        return "JSX"
    elif extension == 'json':
        return "JSON"
    elif extension == 'html':
        return "HTML"
    elif extension == 'css':
        return "CSS"
    elif extension == 'md':
        return "Markdown"
    elif extension == 'java':
        return "Java"
    elif extension == 'ts' or extension == 'tsx':
        return "TypeScript"
    elif extension == 'h':
        return "C Header"
    elif extension == 'hpp':
        return "C++ Header"
    elif extension == 'xml':
        return "XML"
    elif extension == 'cpp':
        return "C++"
    elif extension == 'c' or extension == 'ec' or extension == 'pgc':
        return "C"
    elif extension == 'sh':
        return "Bourne Shell"
    elif extension == 'bash':
        return "Bourne Again Shell"
    elif extension == 'asm' or extension == 'S' or extension == 's':
        return "Assembly"
    elif extension == 'py' or extension == 'pyw':
        return "Python"
    elif extension == 'rs':
        return "Rust"
    elif extension == 'rb':
        return "Ruby"
    elif extension == 'm':
        return "Objective C"
    elif extension == 'mm':
        return "Objective C++"
    elif extension == 'cs':
        return "C#"
    elif extension == 'txt':
        return "Text"
    elif extension == 'yml' or extension == 'yaml':
        return "YAML"
    elif extension == 'bat' or extension == 'BAT' or extension == 'BTM' or extension == 'btm' \
            or extension == 'cmd' or extension == 'CMD':
        return "DOS Batch"
    elif extension == 'def':
        return "Windows Module Definition"
    elif extension == 'Makefile' or extension == 'mk' or extension == 'am' or extension == 'gnumakefile'\
            or extension == 'Gnumakefile' or extension == 'makefile':
        return "make"
    elif extension == 'dart':
        return "Dart"
    elif extension == 'swift':
        return "Swift"
    elif extension == 'pro':
        return "ProGuard"
    elif extension == 'json5':
        return "JSON5"
    elif extension == 'coffee':
        return "CoffeeScript"
    elif extension == 'kt' or extension == 'kts':
        return "Kotlin"
    elif extension == 'gitignore':
        return "Git Ignore"
    elif extension == 'watchmanconfig':
        return "Watchman Config"
    elif extension == 'plist':
        return "Property List"
    elif extension == 'webmanifest':
        return "Web App Manifest"
    elif extension == 'countignore':
        return "Count Ignore"
    elif extension == 'LICENSE':
        return "License"
    else:
        return extension.upper() + " File"


def get_ignore_list():
    try:
        with open(".countignore", "r") as f:
            return [line.strip() for line in f.readlines() if line.strip() != ""]
    except Exception as e:
        return []


def count_lines(filename):
    file_lines = 0
    try:
        with open(filename, "r") as f:
            for _ in f.readlines():
                file_lines += 1
    except Exception as e:
        # print(e)
        pass
    return file_lines


def get_directories(base_path):
    dirs = []
    try:
        for directory in listdir(base_path):
            if isdir(join(base_path, directory)):
                dirs.append(join(base_path, directory))
        return dirs
    except FileNotFoundError:
        print("Error: Path not found.", file=sys.stderr)
        exit(1)
    except Exception as e:
        return []


def read_directories(directories_list, ignores, verbose, zero):
    num_lines, num_files = 0, 0
    for directory in directories_list:
        sub_directories = get_directories(directory)
        for ignore_name in ignores:
            sub_directories = [directory for directory in sub_directories if ignore_name not in directory]
        sub_lines, sub_files = read_directories(sub_directories, ignore_list, verbose, zero)
        num_lines += sub_lines
        num_files += sub_files
        try:
            files = [file for file in listdir(directory) if isfile(join(directory, file))]
            for ignore_name in ignores:
                files = [file for file in files if ignore_name not in file]
        except PermissionError:
            print("Cannot read files in {}".format(directory))
            if 'n' in input("Continue? [y/n]").lower():
                exit(2)
            else:
                files = []
        except Exception as e:
            print(e)
            files = []

        results = []
        for file in files:
            results.append((file, count_lines(join(directory, file))))

        if results:
            max_lines = len(str(max([result[1] for result in results])) + " lines")
            longest_file_name = max([len(filename) for filename in files])
            if zero:
                num_files += sum([1 for _ in results])
            else:
                num_files += sum([1 for result in results if zero or result[1] != 0])
            num_lines += sum([result[1] for result in results])

            if verbose:
                header = "-" * int((longest_file_name + max_lines + 5) / 2)
                print(header, end=" ")
                print(directory, end=" ")
                print(header)
                for result in results:
                    padding = " " * (len(header) * 2 + len(directory) + 2
                                     - len("{}: {} lines".format(result[0], result[1])))
                    print("{}: {}{} lines".format(result[0], padding, result[1]))
                print("\n")
    return num_lines, num_files


def read_directories_ext(directories_list, ignores, verbose, extensions, zero):
    num_lines, num_files = 0, 0
    for directory in directories_list:
        sub_directories = get_directories(directory)
        for ignore_name in ignores:
            sub_directories = [directory for directory in sub_directories if ignore_name not in directory]
        sub_lines, sub_files = read_directories_ext(sub_directories, ignore_list, verbose, extensions, zero)
        num_lines += sub_lines
        num_files += sub_files
        try:
            files = [file for file in listdir(directory) if isfile(join(directory, file))]
            for ignore_name in ignores:
                files = [file for file in files if ignore_name not in file]
        except Exception as e:
            print(e)
            files = []

        results = []
        for file in files:
            results.append((file, count_lines(join(directory, file))))

        if results:
            max_lines = len(str(max([result[1] for result in results])) + " lines")
            longest_file_name = max([len(filename) for filename in files])
            if zero:
                num_files += sum([1 for _ in results])
            else:
                num_files += sum([1 for result in results if zero or result[1] != 0])
            num_lines += sum([result[1] for result in results])

            for result in results:
                ext = result[0].split('.')[-1]

                if ext in extensions:
                    extensions[ext][0] += result[1]
                    extensions[ext][1] += 1
                else:
                    extensions[ext] = [result[1], 1]

            if verbose:
                header = "-" * int((longest_file_name + max_lines + 5) / 2)
                print(header, end=" ")
                print(directory, end=" ")
                print(header)
                for result in results:
                    padding = " " * (len(header) * 2 + len(directory) + 2
                                     - len("{}: {} lines".format(result[0], result[1])))
                    print("{}: {}{} lines".format(result[0], padding, result[1]))
                print("\n")
    return num_lines, num_files


def print_totals(total_lines, total_files):
    print("You have {} lines across {} files".format(total_lines, total_files))


def print_totals_ext(extensions, total_lines, total_files, zero):
    if zero:
        extensions = sorted([ext for ext in extensions.items()], key=lambda x: x[1][0], reverse=True)
    else:
        extensions = sorted([ext for ext in extensions.items() if ext[1][0] != 0], key=lambda x: x[1][0], reverse=True)

    if options.graph:
        extension_names = [get_name(extension[0]) for extension in extensions]
        extension_lines = [extension[1][0] for extension in extensions]
        extension_files = [extension[1][1] for extension in extensions]
        extension_names.reverse()
        extension_lines.reverse()
        extension_files.reverse()

        y_pos = np.arange(len(extension_names))

        plt.subplot(221)
        plt.bar(y_pos, extension_lines)
        plt.xticks(y_pos, extension_names)
        plt.ylabel('Lines')
        plt.title('Lines per extension')

        plt.subplot(224)
        plt.bar(y_pos, extension_files)
        plt.xticks(y_pos, extension_files)
        plt.ylabel('Files')
        plt.title('Files per extension')

        plt.show()
    else:
        line_width = 80
        print("-" * line_width)
        header_padding = " " * int((line_width - len("LANGUAGE  FILES LINES")) / 2)
        print("LANGUAGE {} FILES {} LINES".format(header_padding, header_padding))
        print("-" * line_width)
        for extension in extensions:
            padding = " " * (len("LANGUAGE {} FILES".format(header_padding)) - len(get_name(extension[0]))
                             - len(str(extension[1][1])) - 2)
            rest = " " * (line_width -
                          len("{} {}  {}".format(get_name(extension[0]), padding, extension[1][1], extension[1][0]))
                          - len(str(extension[1][0])) - 1)
            print("{} {} {} {} {}".format(get_name(extension[0]), padding, extension[1][1], rest, extension[1][0]))

        print("-" * line_width)
        padding = " " * (len("LANGUAGE {} FILES".format(header_padding)) - len("SUM")
                         - len(str(total_files)) - 2)
        rest = " " * (line_width -
                      len("{} {}  {}".format("SUM", padding, total_files, total_lines))
                      - len(str(total_lines)) - 1)
        print("{} {} {} {} {}".format("SUM", padding, total_files, rest, total_lines))
        print("-" * line_width)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", "--path", action="store", dest="path", default=".",
                      help="Choose path for the counter to run on")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                      help="Print the names of the scanned files and directories")
    parser.add_option("-e", "--extensions", action="store_true", dest="ext", default=False,
                      help="Sort lines by file extensions")
    parser.add_option("-z", "--include-zero", action="store_true", dest="zero", default=False,
                      help="Include files with zero lines")
    parser.add_option("-g", "--graph", action="store_true", dest="graph", default=False,
                      help="Graph the results **(Experimental Feature)**")
    options, args = parser.parse_args()
    ignore_list = get_ignore_list()
    path = options.path
    # directories = get_directories(path)
    directories = [path]
    for ignore in ignore_list:
        directories = [directory for directory in directories if ignore not in directory]
    if not options.ext:
        number_of_lines, number_of_files = read_directories(directories, ignore_list, options.verbose, options.zero)
        print_totals(number_of_lines, number_of_files)
    else:
        extensions = {}
        number_of_lines, number_of_files = read_directories_ext(directories, ignore_list, options.verbose, extensions,
                                                                options.zero)
        print_totals_ext(extensions, number_of_lines, number_of_files, options.zero)
