'''!
  TODO: Write this dockstring!
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
        print("test")
        time.sleep(delay) #some commands may take seconds to execute.
        print("test")
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

def send_startup():
    """! Send the commands in the 'startup.txt' file.
    This function sends a block of gCode prior to executing the main loop and 
    without processing the replies. It is meant for testing various
    configurations of the startup GCode option in CURA.
    
    It should be called exactly once prior to begining main loop. 
    """
    start = open('startup.txt')
    for line in start:
        send_serial(line)
    
    print("startup")
    
def run_probing():
    print("run probing")
    
def send_shutdown():
    """! send the specified end-of-program g-code. 
    """
    print("disconnect")
    
def display_heat(data):
    """! Geneates and displays a heat map of the bed's height data.
    The map will be displayed with the G30 values set relative to the
    smallest value. 
    @param data an n by n array of the z offsets to be displayed.
    """
    print("display heat")



if __name__ == "__main__":
    get_args()
    send_startup()
    data = run_probing()
    send_shutdown()
    display_heat(data)
    
