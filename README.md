# Printerbot Bed Visualizer

![Image of script output](/pics/with_bed_leveling.png)

A python script for visualizing the surface geometry of a printerbot's bed using
the onboard capacitive sensor. It will most likely also work for plenty of other
printers provided you tweak the settings a bit. 

If requested this script will apply the printer's G29 compensation, allowing
you to see how effective the automatic bed leveling is. The script is compatable
with both the stock printerbot firmware and modern_marlin firmware. 

Also included is a simple fixture for mounting a dial indicator to the 
capacitive sensor. However, I found the onboard capacitive sensor to be
repeatable to within +- 0.25 thou, so I would stick with that unless you are 
worried it is failing. 

### Installation
I use ubuntu and have only somewhat tested the executable under windows. I
recommend running the script as a python script under ubuntu, but it should
work as an executable under windows as well. The two executables (windows and 
ubuntu) are updated only periodically. If you need a feature that doesn't seem
to be in the executable version but is in the script feel free to open an issue
or generate your own executable with pyinstaller.


#### Executable Install
 
Comming soon

#### Full Install
Clone the repo to a machine running ubuntu or windows with python 3. Then install
the dependencies below. 

```
git clone git@github.com:lellasone/printrbot-bed-visualizer.git
pip3 install matplotlib
pip3 install numpy
pip3 install pyserial
pip3 install pyinstaller # Optional, only if you plan to make executables
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
python3 meshscan.py -v -x 150 -y 150 -s 25 -l -p /dev/ttyACM0 --start_delay=30 
```

__Run as a ubuntu executable__
```
./meshscan -v -x 150 -y 150 -s 25 -l -p /dev/ttyACM0
```

__Serial Errors__
Unless your system is very similar to mine you may need to change the port and 
baud rate arguments. The baud rate is a product of the firmware installed on 
your printer, and the comport is a product of the order in which devices are
connected to your computer. Both can be found in your g-code sender. A good
default comport for ubuntu is '/dev/ttyACM0' and a good default guess for 
windows is 'COM0'.

__M114 Read Error on Scan Start__
Larger printers may take longer then the default time to execute their startup
script depending on the options used. This can cause an error where the script
begins it's scan while the printer is still leveling the bed. To deal with this
increase the `--start_delay` argument. 

#### Reading the plot

The heat map is annotated with the "height" of each probe point relative to the 
lowest position probed. When using the script in G29 compatability mode, the 
"height" used is given by [measured bed height] - [bed compensation offset]. 
This means that areas that read as higher (more yellow) on the chart will tend
to have a nozel closer to the bed and areas that read lower (more blue) will
tend to have the nozel farther from the bed. 

In general, a difference of more then about .05 is probobly cause for concern. 

__Saturation__

Saturation (large areas of the heatmap returning identical values when you know
that not to be the case) can occur in two cases as follows:

Low valued saturation around the heatmap edges may occur when your firmware has
been set to prevent probe use near the bed edges, or when an offset has been
defined between the probe and the nozzel. These settings are set in firmware and
short of re-flashing the machine there is nothing to be done about it. adjusting
the bed dimensions and step size can remove these areas from your chart if
desired. 

High-valued saturation may occur When there is a really big difference (~ 2mm) 
between different parts of the 
bed, or when you have a large default z offset then parts of the map will 
saturate. To fix this tweak the PROBE_HEIGHT paramiter up, or open an issue.
Note: Areas that saturate may actually be significantly lower then the value on
the chart.
 
#### Command Line Arguments


|Parameter                     | Default | Description |
| :----------------------------|:--------|:------------|
| -v, verbose                  | False   | prints out extra info.|
| -l, leveling                 | False   | Apply compatability with G29 height compensation (doubles run time). 
| -m, modern_marlin            | False   | Sets the scan to run with parsers conpatable with the modern marlin G30 output format.  
| -b, baud                     | 250000  | baud rate for serial transmission. (firmware specific)|
| -p, port                     | /dev/ttyACM0 | COMPORT to use for communicating with the printer.|
| -x, x_limit                  | 150     | size of area to scan in mm. |
| -y, y_limit                  | 150     | size of area to scan in mm. |
| -s, step                     | 25      | linear spacing along each axis between probe locations in mm. 
| -d, start_dela               | 30      | How long to allow the startup script for execution before begining scan.

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

