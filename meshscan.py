'''!
  TODO: Write this dockstring!
  TODO: Intelegent transit delay times?
'''
import sys
import getopt
import serial
import time

VERBOSE = False 
PRINTER_PORT = '/dev/ttyACM0' #A reasonable default. 
BAUD_RATE = 250000


def send_serial(msg, delay = 0.01):
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
        resp = ser.read(100)
        worked = True
    except serial.SerialException as e:
        print("SERIAL ERROR WHILE SENDIGN: " +str(e))
        resp = ''
    if VERBOSE: print(resp)
    return(resp, worked)
    
    
def get_args():
    global VERBOSE
    args = sys.argv[1:]
    opts_short = "vp:b:"
    opts_long = ["verbose","port=","baud="]
    opts, args = getopt.getopt(args,opts_short, opts_long)
    for opt, arg in opts:
        if opt in ("-v", "verbose"):
            VERBOSE = True
            print("Using verbose output mode")
        elif opt in ("-p", "port"):
            print("setting comport to: " + arg)
        elif pot in ("-b", "baud="):
            BAUD_RATE = args
    if VERBOSE: print(opts)

def send_file(name):
    """! Send the commands in the specified file.
    This function sends a block of g-code without delay between commands. This 
    is useful for things like sending startup or shutdown commands but may not
    be suitable for more complex tasks like sending actual operatinal code. 

    @param name the name of the file to send.  
    """
    try:
        start = open(name)
        for line in start:
            send_serial(line)
        start.close()
    except IOError as e:
       print("ERROR READING FILE: " + str(e))
    
def probe_location(x, y, f = 6000,  delay = 2):
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
    send_serial("G90\n") #Set to absolute coordinates.
    send_serial("G0  F{} X{} Y{}\n".format(f, x, y)) #move to position.
    time.sleep(delay)
    # Find the z offset.
    res, error = send_serial("G30\n", 1)
    if error:
        temp =  res.find(b'endstops') 
        res = res[temp:]
        val = float(res[res.find(b'Z:')+2:])
        return(val)
    else:
        return(0) # Not a great default, but there you go. 

     
def run_probing(lim_x, lim_y, spacing):
    print("run probing")
    values = [] 
    for i in range(0, lim_x, spacing):  
        row = []
        for j in range(0, lim_y, spacing):
            row.append(probe_location(lim_x, lim_y)
        values.append(row)
    print(values) 

def display_heat(data):
    """! Geneates and displays a heat map of the bed's height data.
    The map will be displayed with the G30 values set relative to the
    smallest value. 
    @param data an n by n array of the z offsets to be displayed.
    """
    print("display heat")



if __name__ == "__main__":
    get_args()
    send_file('startup.txt')
    time.sleep(20)
    data = run_probing()
    send_file('shutdown.txt')
    display_heat(data)
    
