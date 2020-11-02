'''! 
    This script repeatedly height-probes a 3D printer's bed and generates a
    heat map of how far each probe height is from the lowest probe point found. 
    The script will repeatedly release and re-aquire ownership of the commport,
    so this most likely will not work with programs like cura running.
      
    The default settings are largely suitable for a printerbot simple metal,
    but the script should work for most printers with a height probe given the
    proper arguments.   

    args:
        -v, verbose:      sets the script to output more internal details. 
        -l, leveling:     sets the script to run in G29 compatablility mode. 
        -m, modern_marlin sets compatability for modernmarlin firmware. 
        -b, baud=:        sets the serial buad rate. 
        -p, port=:        sets the comport. 
        -x, x_limit=:     how large an area in x to probe over. 
        -y, y_limit=:     how large an area in y to probe over. 
        -s, step=:        how far in each axis to move between probings. 
'''
import sys
import getopt
import serial
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# global params, many of these are also set by get_args()
VERBOSE = False 
PRINTER_PORT = '/dev/ttyACM0' #A reasonable default. 
BAUD_RATE = 250000
X_LIM = 150 #default x size in pritner units (ussually mm)
Y_LIM = 150 #default y size in printer units (ussually mm)
SPACING = 25 #default distance between points. 
FEED = 4000
LEVELING = False
PROBE_HEIGHT = 4
PROBE_DELAY  = 2 # How long to wait during a G30 operation. This is dependent
                 # ont he probe height and firmware revision. 
MODERN_MARLIN = False
STEPS_PER_UNIT_Z = 2020 #this really isn't going to be correct without tuning. 


def send_serial(msg, delay = 0.01, expected_len = 150):
    """! Sends a string over serial to the printer. 
    This function connects to the robot, sends the specified string, and then 
    disconnects from the printer. Note that comport exceptions are caught and 
    displayed without stopping the program. That means commands may be missed!
    
    Note: PRINTER_PORT must be set to the correct comport prior to calling this
          function. Otherwise it really won't do much of anything. 
    @param msg string to send to 3D printer.
    @pram delay time to wait (in seconds) between sending a message and reading
                the reply. The default is fine for settings or move commands,
                but may be too short for quiries that involve movement.
    @param expected_len how many bytes to wait for on read
    @returns the serial responce if any and a bool to indicate if an error
             occured while executing. 
    """
    global VERBOSE
    global PRINTER_PORT
    if VERBOSE: print("sending: " + msg)
    worked = False
    try: 
        ser = serial.Serial(PRINTER_PORT,timeout=1)
        ser.write(bytes(msg, 'ascii'))
        time.sleep(delay) #some commands may take seconds to execute.
        resp = ser.read(expected_len)
        worked = True
    except serial.SerialException as e:
        print("SERIAL ERROR WHILE SENDIGN: " +str(e))
        resp = ''
    if VERBOSE: print(resp)
    return(resp, worked)
    
    
def get_args():
    """! This function reads in and processes the command line arguments. 
    Does what it says on the tin. If you are planning to use command line args
    then this should be called first so the various globals can be set. 
    """
    global VERBOSE
    global BAUD_RATE
    global X_LIM
    global Y_LIM
    global SPACING
    global PRINTER_PORT
    global LEVELING
    global PROBE_DELAY
    global MODERN_MARLIN
    args = sys.argv[1:]
    opts_short = "vp:b:x:y:s:lm"
    opts_long = ["verbose","port=","baud=",
                 "x_limit=", "y_limit=","step=","leveling","modern_marlin"]
    try: 
        opts, args = getopt.getopt(args,opts_short, opts_long)
        for opt, arg in opts:
            if opt in ("-v", "verbose"):
                VERBOSE = True
                print("Using verbose output mode")
            elif opt in ("-p", "port"):
                PRINTER_PORT = arg 
            elif opt in ("-b", "baud="):
                BAUD_RATE = int(arg)
            elif opt in ("-x", "x_limit="):
                X_LIM = int(arg)
            elif opt in ("-y", "y_limit="):
                Y_LIM = int(arg)
            elif opt in ("-s", "step="):
                SPACING = int(arg)
            elif opt in ("-l", "leveling"):
                LEVELING = True
            elif opt in ("-m", "modern_marlin"):
                PROBE_DELAY = 6
                MODERN_MARLIN = True
                print(("WARNING: Marlin firmware may be unable to probe extreme "
                       "edges of the printbed. Consider reducing the x and y "
                       "dimensions of the probe area and increasing the step "
                       "size if edge saturation occurs."))
        if VERBOSE: print(opts)

    except getopt.GetoptError as e:
        print("Argument Error: " + str(e))
        print("valid arguments include: " + str(opts_long))
        print("!!!exiting program now!!!")
        quit()
    
def send_file(name):
    """! Send the commands in the specified file.
    This function sends a block of g-code without delay between commands. This 
    is useful for things like sending startup or shutdown commands but may not
    be suitable for more complex tasks like sending actual operatinal code. 

    It's a tossup whether this catches comments and blank space correctly.

    @param name the name of the file to send.  
    """
    try:
        start = open(name)
        for line in start:
            # Handle comments (sorta)
            send = line[:line.find(';')]
            if send[-1] != '\n':  send = send + "\n"
            # Send the data. 
            send_serial(send)
        start.close()
    except IOError as e:
       print("ERROR READING FILE: " + str(e))
def taste_leveling(x, y, f = 4000,  delay = 2):
    """! This function returns the current amount of leveling compensation.  
    This is useful for building up a scan of the offset applied by the printer
    to it's actual coordinates during printing. Note that calling G30 will 
    eliminate any leveling and this will just return the absolute coordinates.
    

    If the LEVELING global variable is set to false then this function just
    returns zero.
     
    The default move delay is suitable for medium-length moves, but may need
    to be extended for large printer beds. 
    @param x absolute axis location. 
    @param y absolute axis location. 
    @param f in printer units (ussually mm/m)
    @returns z distance above actual coordiantes that the printer would travel
               to during printing. 
    """
    global VERBOSE
    global LEVELING
    if LEVELING:
        if VERBOSE: print("*** Starting Taste ***")
        move_delay(x, y, f, delay)
        
        # Get the m114 string and extract the absolute z position.
        m114, error = send_serial("M114\n", 0.1)
        if error:
            zm114 = m114[m114.find(b'Z:')+2:] # strip to the first Z 
            zzm114 = zm114[zm114.find(b'Z:')+2:zm114.find(b'\n')] # extract the second Z
            
            # Marlin returns value in steps rather then units. 
            if MODERN_MARLIN:
                return(float(zzm114)/STEPS_PER_UNIT_Z)
            else:
                return(float(zzm114)) 
        else: 
            return(0) # Not a great default, but there you go. 
    else:
        return(0) #create an empty offset map. 
   
def probe_location(x, y, f = 4000,  delay = 2):
    """! Move the print head to the specified location and probe bed height.
    This function moves the print head to the specified location in absolute
    coordinates without altering the z-height. It then probes the bed height
    and returns that value. 

    The default move delay is suitable for medium-length moves, but may need
    to be extended for large printer beds. 
    @param x absolute axis location. 
    @param y absolute axis location. 
    @param f in printer units (ussually mm/m)
    @returns z height at which bed was detected.
    """
    global VERBOSE
    global PROBE_HEIGHT
    global PROBE_DELAY
    global MODERN_MARLIN
    if VERBOSE: print("*** Starting Probe ***")
    move_delay(x, y, f, delay, z=PROBE_HEIGHT)
    
    res, error = send_serial("G30\n", PROBE_DELAY)
    if error:
        # handle different string config between firmware versions these pretty
        # much have to be hand crafted for each version. 
        if MODERN_MARLIN:
            if len(res) < 10:
                # Weird known bug in marlin relating to M851 settings. 
                print("WARNING: Unable to probe this location, setting height 0")
                val = 0
            else:   
                res = res[res.find(b'Z:') + 2:]
                end = res.find(b'\n')
                val = float(res[:end])
        else:
            temp =  res.find(b'endstops') 
            res = res[temp:]
            val = float(res[res.find(b'Z:')+2:])
        return(val) 
    else: 
        return(0) # Not a great default, but there you go.  

def move_delay(x, y, f, delay, z = 0):
    """! Makes an absolute move to a position and then waits the delay.
    This function wrapps a G0 command with a delay command. It is useful
    for general purpose moves. A G90 command is used to set the coordinates
    to absolute prior to execution. 
    @param x float indicating desired location. 
    @param y float indicating desired location.
    @param f feedrate (ussually in mm/m)
    @param delay how long to wait in seconds. 
    """ 
    send_serial("G90\n") #Set to absolute coordinates.
    send_serial("G0  F{} X{} Y{} Z{}\n".format(f, x, y, z), delay) #move to position.
                               
def run_probing(lim_x, lim_y, spacing, leveling = False):
    """! Main testing loop of the program, this executes probes each location.
    Executes a printer height probe at each location specified by the operating
    area and spacing paramiter. This function can also be used to get the
    actual offset map of G29 bed leveling.  
    @param lim_y y dimension of the area to test. 
    @param lim_x x dimension of the area to test. 
    @param seperation along each axis of probe locations.
    @param leveling sets the function to return the leveling compensation map
                    rather then the bed height map. 
    @returns array containing the read z value at each test location. 
    """ 
    global VERBOSE 
    global FEED 
    if VERBOSE: print("run probing")
     
    values = [] # Move to zero zero before starting.  
    move_delay(0,0,FEED,120*np.sqrt(lim_x**2 + lim_y**2)/FEED)

    offset = spacing/2 #probe in the center of each square
    for i in range(0, lim_x, spacing):  
        row = []
        for j in range(0, lim_y, spacing):
            # Set the move delay based on expected travel distance
            if j == 0: 
                delay = 150*lim_y/FEED
            else:
                delay = 120*spacing/FEED  
            if leveling:
                row.append(taste_leveling(i+offset,
                                          j+offset,
                                          f = FEED,
                                          delay = delay))    
            else:
                row.append(probe_location(i+offset,
                                          j+offset, 
                                          f = FEED, 
                                          delay = delay))
                
            percent = (i*lim_x + j*spacing)/((lim_x)*(lim_y))*100
            print("completion percentage: " + str(round(percent, 1)) + "%")
        values.append(row)
    return(values)

def display_heat(data):
    """! Geneates and displays a heat map of the bed's height data.
    The map will be displayed with the G30 values set relative to the
    smallest value. 
    @param data an n by n numpy array of the z offsets to be displayed.
    """ 
    global Y_LIM
    global SPACING
    global X_LIM
    print(data)
    # Lets condition the data
    mind = np.amin(data)
    data = data-mind # set our lowest value to zero
    data = np.rot90(data) 
    # msc matplot lib stuff 
    a, ax = plt.subplots()
    im = ax.imshow(data)

    #label each square
    for i in range (data.shape[0]):
        for j in range(data.shape[1]):
            ax.text(j, i, np.round(data[i, j],2),
                    ha="center", va="center", color="b")

     
    # Lets set up the axis labels 
    x_lim = X_LIM # Fixes a variable not defined issue. Why? Who knows...
    ax.set_yticks(range(0, int(Y_LIM/SPACING)))
    ax.set_yticklabels(np.flipud(np.arange(0, Y_LIM, SPACING))+SPACING/2)   
    ax.set_xticks(range(0, int(x_lim /SPACING)))
    ax.set_xticklabels(np.arange(0, x_lim, SPACING)+SPACING/2)

    plt.colorbar(im, ax = ax) 
    ax.set_title("3D Printer Flatness Map (mm)")
    ax.set_ylabel("y position (mm)")
    ax.set_xlabel("x position (mm)")
    plt.show()
    

def get_conversion():
    """ Get the steps per unit from the printer and record that global value. 
    This should probobly be called after the initial startup file is sent to
    ensure the units are correct. 

    Note: something will probobly break if the printer isn't actually in mm.
    """
    global STEPS_PER_UNIT_Z
    global VERBOSE
    (msg, worked)= send_serial("M503\n", expected_len = 500)
    if worked:
        msg = msg[msg.find(b'Steps per unit:')+15:] # strip to unit conversions. 
        msg = msg[msg.find(b'Z')+1:] # strip to z. 
        msg = msg[:msg.find(b'E')] #remove everything after the z value. 
        if VERBOSE: print("Their are {} steps per mm on the Z axis".format(msg))
        STEPS_PER_UNIT_Z = float(msg)
    else:
        print("WARNING: Unable to set steps per mm Z")

if __name__ == "__main__":
    get_args()
    get_conversion()
    send_file('startup.txt')
    time.sleep(30)
    offset = run_probing(X_LIM, Y_LIM, SPACING, leveling = True)
    data = run_probing(X_LIM, Y_LIM, SPACING)
    send_file('shutdown.txt')
    display_heat(np.array(data)-np.array(offset))
    
