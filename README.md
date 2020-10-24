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

#### Executable Install

#### Full Install
Clone the repo to a machine running ubuntu. It may also run under windows but
I have never tried it. Feel free to start an issue if you run into trouble.  

#### Dial indicator
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

#### Command Line Arguments


|Parameter                     | Default | Description |
| :----------------------------|:--------|:------------|
| -v, verbose                  | False   | prints out extra info|
| -b, baud                     | 250000  | baud rate for serial |
| -p, port                     | /dev/ttyACM0 | Comport that printer is on |
| -x, x_limit                  | 150     | size of area to scan in mm |
| -y, y_limit                  | 150     | size of area to scan in mm |
| -s, step                     

#### Start and end files 
Place your machine's startup g-code into the startup.txt file. This will be run
prior to the scan. Use this to run any commands (say homing or bed leveing) run
prior to printing. If you are copying over code from cura's printer settings
take care to REMOVE any that relate to the extruder. 

Do the same thing for your machine's ending g-code. This won't impact the scan
results, but you may find it convenient to have it home or zero after use. 

The comment handeling is very much an afterthought so if you run into trouble 
consider removing all of the comments from your startup and shutdown scripts.
Also, if either of these files takes longer then ~20s to execute you may need to
tweak that in code. (It's unlikely though)

### Issues
If you run into problems using this code, or need help adapting it to another 
printer please create a github issue and we'll get it sorted out. 

