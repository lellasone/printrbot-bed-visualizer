# Printerbot Bed Visualizer

A python script for visualizing the surface geometry of a printerbot's bed using
the onboard capacitive sensor. It will most likely also work for plenty of other
printers provided you tweak the settings a bit. 

Also included is a simple fixture for mounting a dial indicator to the 
capacitive sensor. 

Note: I found the onboard capacitive sensor to be
repeatable to within +- 0.25 thou, so I would stick with that unless you are 
worried it is failing. 

### installation

#### Visualizer script
Clone the repo to a machine running ubuntu.   

#### Dial Indicator
The included STL is suitable for use with a shars dial dial indicator with a 
3/8 shoulder. The screws are 4-40x5/8 and the knuts are .24in edge to edge,
although the corresponding M3 hardware may work with some persuasion. The part 
is not settings sensative and can be printed with standard .8mm walls and 25% 
infill. The included STL will print both halfs of the clamp in one print and
they can then be pried appart with a knife. 
The mount is designed in solidworks and can be eddited in any solidworks more
recent then 2017. You may also have some luck with onshape (which is free and 
quite good) although I have not tried it for this particular part. 

### Usage

Place your machine's startup g-code into the startup.txt file. This will be run
prior to the scan. Note that the parser is not comment aware so the file needs
to be composed of exactly one command per line with no comments and no blank
lines. This step is very important because if your startup commands here do not
match what you send from CURA (or the sender of your choice) then the results
may not match what your printer experences in use. 

Do the same thing for your machine's ending g-code. This won't impact the scan
results, but you may find it convenient to have it home or zero after use. 


### Issues
If you run into problems using this code, or need help adapting it to another 
printer please create a github issue and we'll get it sorted out. 

