'''!
  TODO: Write this dockstring!
'''

VERBOSE = True 
PRINTER_PORT = 'dev\ttyUSB0' #A reasonable default. 

def send_serial(msg):
    """! Sends a string over serial to the printer. 
    This function connects to the robot, sends the specified string, and then 
    disconnects from the printer. Note that comport exceptions are caught and 
    displayed without stopping the program. That means commands may be missed!
    
    Note: PRINTER_PORT must be set to the correct comport prior to calling this
          function. Otherwise it really won't do much of anything. 
    @param msg string to send to 3D printer. 
    """
    global VERBOSE
    global PRINTER_PORT
    if VERBOSE: print("sending: " + msg)
    
    
def get_args():
    print("managing command line args")

def send_startup():
    print("startup")
    
def run_probing():
    print("run probing")
    
def disconnect():
    """! Safely shuts down the pyserial object. 
    """
    print("disconnect")
    
def display_heat(data):
    """! Geneates and displays a heat map of the bed's height data.
    The map will be displayed with the G30 values set relative to the
    smallest value. 
    @param data an n by n array of the z offsets to be displayed.
    """
    print("display heat")



if __name__ = "__main__":
    get_args()
    send_startup()
    data = run_probing()
    send_shutdown()
    display_heat(data)
    