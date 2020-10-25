# Printerbot Bed Visualizer

![Image of script output](/pics/with_bed_leveling.png)

A python script for visualizing the surface geometry of a printerbot's bed using
the onboard capacitive sensor. It will most likely also work for plenty of other
printers provided you tweak the settings a bit. 

If requested this script will apply the printer's G29 compensation, allowing
you to see how effective the automatic bed leveling is. 

Also included is a simple fixture for mounting a dial indicator to the 
capacitive sensor. However, I found the onboard capacitive sensor to be
repeatable to within +- 0.25 thou, so I would stick with that unless you are 
worried it is failing. 

### installation
I use ubuntu and have only somewhat tested the executable under windows. I
recommend running the script as a python script under ubuntu, but it should
work as an executable under windows as well.


#### Executable Install (windows)
Clone the repo to a machine running windows. You can do this by clicking on the 
green "Code" button in the upper right-hand side of this screen. 

The meshscan.exe was automatically generated using pyinstaller. 

#### Full Install (ubuntu)
Clone the repo to a machine running ubuntu. It may also run under windows but
I have never tried it. Feel free to start an issue if you run into trouble. 
Then install the dependencies below.  

```
pip3 install matplotlib
pip3 install numpy
pip3 install pyserial
```
 
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

After completing the installation (above) the script can be run from the 
command line as follows. Your arguments (below) may be different depending on 
what exactly you want to do. 
 
__Run as a python script__
```
python3 meshscan.py -v -x 150 -y 150 -s 10 -l -p /dev/ttyACM0 
```

__Run as a windows executable__
```
#TODO: put something reasonable here
```

Unless your system is very similar to mine you may need to change the port and 
baud rate arguments. The baud rate is a product of the firmware installed on 
your printer, and the comport is a product of the order in which devices are
connected to your computer. Both can be found in your g-code sender. A good
default comport for ubuntu is '/dev/ttyACM0' and a good default guess for 
windows is 'COM0'.

#### Reading the plot

The heat map is annotated with the "height" of each probe point relative to the 
lowest position probed. When using the script in G29 compatability mode, the 
"height" used is given by [measured bed height] - [bed compensation offset]. 
This means that areas that read as higher (more yellow) on the chart will tend
to have a nozel closer to the bed and areas that read lower (more blue) will
tend to have the nozel farther from the bed. 

In general, a difference of more then about .05 is probobly cause for concern. 

#### Command Line Arguments


|Parameter                     | Default | Description |
| :----------------------------|:--------|:------------|
| -v, verbose                  | False   | prints out extra info.|
| -l, leveling                 | False    | Apply compatability with G29 height compensation (doubles run time). 
| -b, baud                     | 250000  | baud rate for serial transmission. (firmware specific)|
| -p, port                     | /dev/ttyACM0 | COMPORT to use for communicating with the printer.|
| -x, x_limit                  | 150     | size of area to scan in mm. |
| -y, y_limit                  | 150     | size of area to scan in mm. |
| -s, step                     | 25      | linear spacing along each axis between probe locations in mm. 
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

