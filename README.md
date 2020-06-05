## Brians Epic Build System

### Introduction
#### What is it?
This is a simple build system which will take a project and compile the files which have changed so I don't have to spend lots of time waiting for GCC to recompile everything.

#### Why not use make?
I found that make was too complicated when all I want to do is compile some files quickly.

#### Todo
- [ ] Header file recompile
- [x] Detect new files
- [x] Support for compile templates, eg: `{%COMPILER%} {%ARGS%} {%LIBS%} {%FILES%}`
- [x] Clean source code
- [ ] Add more examples

### How to use
#### BMake files
To get started you will first need to make a `"bmake"` file. This file will be passed to BEBS so it knows what to compile.\
If the file is just called `"bmake"` then BEBS will auto-detect it. BEBS will also auto-detect files with the text "BEBS_FILE" on the first line.

BEBS requires 3 core variables to work demonstrated bellow.
```python
# list of files to be compiled
files = ["main.cpp", "lib/git.cpp", etc...]
# the directory the object files should be put in
builddir = "build/"
# extra libs the project should be compiled with
libs = ["-lgit2"]
```
If you don't want to manually add each file to the list, you can instead define a folder of files.
```python
# %d (or %D) tells bebs that the item in actually a folder that should be listed
files ["main.cpp", "%d lib/"]
exts = ["cpp"]
# when defining a folder, you need to tell bebs what extensions to looks for
# by default bebs will look for C and CPP files so the exts shouldn't usually need to be defined
# it is not recommended you include header extensions in this list
```


[More commands can be found here](#extra-bmake-options)

#### Running the BEBS file
Assuming you have the BMake configured correctly, you should be able to just run
`bebs.py %filename%`
and it will begin to compile your project.

The initial build may take some time however after this, it will only compile the files which have changed. A build cache is placed in the build folder as well as the object files.
#### Warning! ####
Do not remove the build.db file unless you are willing to recompile the whole project. However, if you wish to do this you also have the option of adding `-f` to the run command.

#### Extra bmake options
|                                 |                                                                                 |
|-------------------------------- |---------------------------------------------------------------------------------|
| **output = %filename%**         | -- Will specify an output file                                                  |
| **execute = %command%**         | -- Will specify a command to run after build, such as `./a.out -f -c args4life` |
| **force = True/False**          | -- Force full build every time (wouldn't advise using)                          |
| **compiler = %compiler%**       | -- Specify a compiler to use (defaults to g++)                                  |
| **linker = %linker%**           | -- Specify a linker to use (defaults to g++)                                    |
| **build_args = %args%**         | -- Specify args for the build process to use (should always use -c)             |
| **link_args = %args%**          | -- Specify args for the linking stage                                           |
| **build_template = %template%** | -- Define the structure of the build command, [More info](#templates)           |
| **link_template = %template%**  | -- Define the structure of the link command, [More info](#templates)            |

#### Command line args
|                          |                                                                                 |
|------------------------- |---------------------------------------------------------------------------------|
| **%filename%**           | -- Specify BMake file                                                           |
| **-x %command%**         | -- Will specify a command to run after build, such as `./a.out -f -c args4life` |
| **-o %filename%**        | -- Specify an output file                                                       |
| **-f**                   | -- Force full build                                                             |

#### Templates
Templates are used to tell BEBS how the compile and link commands should be structured. \
Example: \
`build_template = {compiler} {args} {files}` \
`link_template = {linker} {args} {output} {files} {libs}` \
These are the default templates that BEBS will use. There aren't many situations where you would need to define a custom one but the option is available.

### Build and Run
#### Windows
BEBS hasn't been tested on windows however I imagine it should work fine if you set up your path correctly

#### Linux
On linux you can compile the .py file using the following command\
`pyinstaller -F --onefile bebs.py`\
This will require the `pyinstaller` package to be installed.

