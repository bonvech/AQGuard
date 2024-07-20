from aq_device import AQGuard_device
import time
import telebot

import telebot_config


try:
    device = AQGuard_device()

    ##  start connection
    if device.connect() == 1:
        text = "Connect error"
        device.print_message(text, '\n')
        exit("Connect error")

    while True:
        
        ##  request all params
        try:
            device.request_all()
            #device.write_to_bot("AQGuard: OK")
        except Exception as error:
            text = f"AQGuard Error in request  {device.IPname}!! {error}"
            print(f"\n\n Error in request {device.IPname}!! {error} \n")
            device.write_to_bot(text)
        
        time.sleep(58)

except Exception as error:
    text = f"Final AQGuard Error: {device.IPname}: {error}"
    device.write_to_bot(text)
    #bot = telebot.TeleBot(telebot_config.token, parse_mode=None)
    #bot.send_message(telebot_config.channel, text)



#device.request('<getVal40;64;61;>')  #\r\n')
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
## disconnect
#device.unconnect()
