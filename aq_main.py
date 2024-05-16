from aq_device import AQGuard_device
import time
#from ae33_plot_figures import *


device = AQGuard_device()

##  start connection
if device.connect() == 1:
    text = "Connect error"
    device.print_message(text, '\n')
    exit("Connect error")


#device.request('<getVal40;64;61;>')  #\r\n')
#device.request('<getVal40;64;61;>')  #\r\n')

while True:
    try:
        device.request_all()
    except Exception as error:
        print(f"\n\nError in request!! {error}\n")
    time.sleep(58)

#request = f"<getVal{';'.join(str(n) for n in range(110, 174))}>"
#device.request(request) 

#device.request('<getHis0;400;>') 
#device.request('<getHis1;400;>') 
#device.request('<getHis2;400;>') 
#device.request('<getHis3;400;>') 

##  close connection
print("\n==========  close connection =========================")
#device.request('CLOSE', 0, 0)
device.unconnect()
