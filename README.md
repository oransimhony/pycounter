# PyCounter

PyCounter is a script I wrote for counting lines and files in directories.

PyCounter can provide metrics for your projects.

## Motivation

At times I want to know how many lines I already wrote in the project,
but I don't want to go through the hassle of counting each and every file so I wrote this small script to help me ✨

## Installation

Execute this on your preffered terminal.

```sh
git clone https://github.com/oransimhony/pycounter.git
cd pycounter
```

And now you are ready to go!

## Usage

```sh
python counter.py --help

Usage: counter.py [options]

Options:
  -h, --help            show this help message and exit
  -p PATH, --path=PATH  Choose path for the counter to run on
  -v, --verbose         Print the names of the scanned files and directories
  -e, --extensions      Sort lines by file extensions
  -z, --include-zero    Include files with zero lines
  -g, --graph           Graph the results **(Experimental Feature)**
```

If you don't specify a path, the path defaults to current directory

## Ignoring files and directories

Like .gitignore, you can use .countignore to specify names of directories and files you don't want to be scanned.

## Examples

Examples with this directory

```sh
python counter.py

You have 395 lines across 4 files

python counter.py -e

--------------------------------------------------------------------------------
LANGUAGE                               FILES                               LINES
--------------------------------------------------------------------------------
Python                                     1                                 314
Markdown                                   1                                  57
License                                    1                                  21
Count Ignore                               1                                   3
--------------------------------------------------------------------------------
SUM                                        4                                 395
--------------------------------------------------------------------------------
```

## Credits

[AlDanial's cloc](https://github.com/AlDanial/cloc) for some language names based on file extensions and ideas for the styling of the output

## Authors

* **Oran Simhony** - [oransimhony](https://github.com/oransimhony)
