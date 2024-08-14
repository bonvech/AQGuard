from aq_device  import AQGuard_device
from aq_convert import *
import time
import telebot

import telebot_config


try:
    device = AQGuard_device()

    convert_period = 20  ## min to renovate csv file
    convert = 0
    while True:
        time.sleep(58)

        ##  start connection
        if device.connect() == 1:  ##  if error
            text = "Connect error"
            device.print_message(text, '\n')
            device.write_to_bot(text)
            continue
            #exit("Connect error")

        ##  request all params
        try:
            device.request_all()
            #device.write_to_bot("AQGuard: OK")
        except Exception as error:
            text = f"AQGuard Error in request  {device.IPname}!! {error}"
            print(f"\n\n {text} \n")
            device.write_to_bot(text)

        ##  disconnect
        device.unconnect()
        
        ##  convert raw file to csv every {convert_period} seconds
        convert = (convert + 1) % convert_period
        if not convert:
            try:
                print("convert")
                convert_raw_file_to_csv(device.rawfilename)
            except Exception as error:
                text = f"AQGuard Error: convert: {error}"
                device.write_to_bot(text)

except Exception as error:
    text = f"Final AQGuard Error: {error}. \n Programm TERMINATED. Start it again."
    device.write_to_bot(text)


#device.request('<getVal40;64;61;>')  #\r\n')
#device.request('<getHis0;400;>') 
#device.request('<getHis1;400;>') 
#device.request('<getHis2;400;>') 
#device.request('<getHis3;400;>') 
