#### About this example
This example shows how mutliple files can be compiled and linked using BEBS\
This example uses a main header file called `global.h` to share functions.

#### BMake
Here is the bmake file
```python
# BEBS_FILE #
files = ["main.cpp", "inc/second.cpp", "inc/third.cpp"]
builddir = "build/"
libs = [""]
```
#### BEBS_FILE header
The first line isn't exactly needed however it is a good example of how to use the BEBS_FILE tag\
The file can be called whatever you want aslong as the first line contains `BEBS_FILE`

#### BMake content
- The second line defines the files which will be compiled
- The third line defines the folder which the object and cache files will be added to
- The final line is for defining extra libs to compile. However, there aren't any in this example

The example will default to `a.out` as an output file because one was not defined in the `bmake` file.\
As seen in the documentation, if you want to add a custom output file you can add the line\
`output = "myexe"`