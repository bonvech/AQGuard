## you need to install 
# pip install pandas
# pip install openpyxl==3.0.9
# pip install pyTelegramBotAPI

import sys
import socket
import time
import datetime
from   datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os
# for bot
import telebot
import telebot_config



## ----------------------------------------------------------------
##  
## ----------------------------------------------------------------
def select_year_month(datastring):
    return datastring.split()[0][-4:] + '_' + datastring[3:5]


## ----------------------------------------------------------------
##  
## ----------------------------------------------------------------
def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return hostname, local_ip



############################################################################
############################################################################
class AQGuard_device:
    def __init__(self):

        ## for data files
        self.yy = '0'        ##  year for filename of raw file
        self.mm = '0'        ## month for filename of raw file
        self.yy_D = '0'      ##  year for filename of D-file
        self.mm_D = '0'      ## month for filename of D-file 
        self.datadir = ''   ## work directory name
        self.xlsfilename = ''      ## exl file name
        self.csvfilename = ''      ## csv file name
        self.file_raw = None       ## file for raw data
        self.file_format_D = None  ## file for raw data
        self.file_header = ''
        self.head = ''
        self.device_name = 'AQ'    ##

        self.run_mode = 0
        self.logdirname  = ""
        self.logfilename = "AQ_log.txt"  ## file to write log messages
        self.rawdirname  = "raw"

        self.buff = ''
        self.info = ''
        self.IPname = '192.168.1.71'
        self.IsConnected = 1
        self.Port = 56789  ## port number
        self.sock = None  ## socket
        self.xlscolumns = ['Datetime', 'BC1', 'BC2', 'BC3', 'BC4', 'BC5', 'BC6', 'BC7', 'BB(%)']

        if 'ix' in os.name:
            self.sep = '/'  ## -- path separator for LINIX
        else:
            self.sep = '\\' ## -- path separator for Windows

        ## --- run functions ---
        self.fill_header() ## to develop data files
        self.read_config_file()
        self.print_params()
        self.prepare_dirs()


    ## ----------------------------------------------------------------
    ##  Print message to logfile
    ## ----------------------------------------------------------------
    def print_message(self, message, end=''):
        print(message)
        if message[-1] != '\n' and end != '\n':
            message += '\n'
        self.logfilename = self.logdirname + "_".join(["_".join(str(datetime.now()).split('-')[:2]), self.device_name,  'log.txt'])
        with open(self.logfilename,'a') as flog:
            flog.write(f"{datetime.now()}:  {message}{end}")


    ## ----------------------------------------------------------------
    ##  write message to bot
    ## ----------------------------------------------------------------
    def write_to_bot(self, text):
        try:
            hostname, local_ip = get_local_ip()
            text = f"{hostname} ({local_ip}): {text}"
            
            bot = telebot.TeleBot(telebot_config.token, parse_mode=None)
            bot.send_message(telebot_config.channel, text)
        except Exception as err:
            ##  напечатать строку ошибки
            text = f": ERROR in writing to bot: {err}"
            self.print_message(text)  ## write to log file


    ############################################################################
    ############################################################################
    def fill_header(self):
        self.head = "Date(yyyy/MM/dd); Time(hh:mm:ss); Timebase; RefCh1; Sen1Ch1; Sen2Ch1; RefCh2; Sen1Ch2; Sen2Ch2; RefCh3; Sen1Ch3; Sen2Ch3; RefCh4; Sen1Ch4; Sen2Ch4; RefCh5; Sen1Ch5; Sen2Ch5; RefCh6; Sen1Ch6; Sen2Ch6; RefCh7; Sen1Ch7; Sen2Ch7; Flow1; Flow2; FlowC; Pressure(Pa); Temperature(°C); BB(%); ContTemp; SupplyTemp; Status; ContStatus; DetectStatus; LedStatus; ValveStatus; LedTemp; BC11; BC12; BC1; BC21; BC22; BC2; BC31; BC32; BC3; BC41; BC42; BC4; BC51; BC52; BC5; BC61; BC62; BC6; BC71; BC72; BC7; K1; K2; K3; K4; K5; K6; K7; TapeAdvCount; "
        if self.device_name == '':
            print("\n\nfill_header:  WARNING! Name of the device is unknown!!!!!\n")
        self.file_header = (
            "AETHALOMETER\n" +
            "Serial number = " +
            self.device_name +  # "AE33-S08-01006" +
            "\n" + 
            "Application version = 1.6.7.0\nNumber of channels = 7\n\n" + 
            self.head + "\n\n\n")


    ############################################################################
    ## read config file
    ############################################################################
    def read_config_file(self):
        # read file
        try:
            import aq_config as config
        except Exception as err:
            ##  напечатать строку ошибки
            text = f": ERROR in reading config: {err}"
            print(text)
            print(f"\n!!! read_config_file Error!! Check configuration file 'ae33_config' in  \n\n")
            return -1
                  
        self.IPname = config.IP
        self.Port   = config.Port
        
        self.datadir = config.Datadir.strip()
        self.datadir = self.sep.join(self.datadir.split("/"))
        ##  add separator to end of dirname
        if self.datadir[-1] != self.sep:
            #print('add sep', self.datadir)
            self.datadir += self.sep
        
        if not self.device_name:        
            self.device_name = config.device_name
            self.fill_header()

        self.write_config_file()


    ############################################################################
    ## read config file "PATHFILES.CNF"
    ############################################################################
    def read_path_file(self):
        # check file
        config_file = "aq_config.py"
        try:
            f = open(config_file)
            params = [x.replace('\n','') for x in f.readlines() if x[0] != '#']
            f.close()
        except:
            print(f"\n\n Error!! No config file {config_file}\n\n")
            return -1

        for param in params:
            if "RUN" in param:
                self.run_mode = int(param.split('=')[1])
            elif "IP" in param:
                self.IPname = param.split('=')[1].split()[0]
                self.Port   = int(param.split('=')[1].split()[1])
            else:
                self.datadir = param
                ##  add separator to end of dirname
                if self.datadir[-1] != self.sep:
                    print('add sep', self.datadir)
                    self.datadir += self.sep
                

    ############################################################################
    ##  check and create dirs for data 
    ############################################################################
    def prepare_dirs(self):
        if not os.path.isdir(self.datadir):
            os.makedirs(self.datadir)
        
        path = self.datadir + 'raw' + self.sep
        if not os.path.isdir(path):
            os.makedirs(path)

        path = self.datadir + 'ddat' + self.sep
        if not os.path.isdir(path):
            os.makedirs(path)

        path = self.datadir + 'table' + self.sep
        if not os.path.isdir(path):
            os.makedirs(path)

        path = self.datadir + 'log' + self.sep
        if not os.path.isdir(path):
            os.makedirs(path)
        self.logdirname = path


    ############################################################################
    ############################################################################
    def write_config_file(self):
        #f = open("PATHFILES.CNF.bak", 'w')
        f = open("ae33_config.bak", 'w')
        f.write(f'#\n Device name')
        f.write(f'device_name= "{self.device_name}"\n')
        f.write( "#\n# Directory for DATA:\n#\n")
        f.write(f'Datadir = "{self.datadir}"\n')
        f.write( "#\n# AE33:   IP address and Port:\n#\n")
        f.write(f'IP = "{self.IPname}"\n') 
        f.write(f"Port = {self.Port}\n")
        f.write( "#\n# AE33:  Last Records:\n#\n")
        f.write( "#\n")
        f.close()


    ############################################################################
    ############################################################################
    def print_params(self):
        print(f"device_name = ", self.device_name)
        print(f"IP = ",       self.IPname)
        print(f"Port = ",     self.Port)
        print(f"datadir = ",  self.datadir)


    ############################################################################
    ############################################################################
    def connect(self):
        #text = "=====  connect ======\n"
        #self.print_message(text)
        errcode = 0

        ## --- create socket
        #socket.socket(family='AF_INET', type='SOCK_STREAM', proto=0, fileno=None)
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM | socket.SOCK_NONBLOCK)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock = socket.socket()

        ## --- connect to server
        try:
            self.sock.connect((self.IPname, self.Port))
            text = f'AQGuard: socket connected to {self.IPname}'
            self.print_message(text, '\n')
        except Exception as e:  #TimeoutError:
            errcode = 1
            text = f"Message: error <<{e}>>: {self.device_name} on address {self.IPname} does not responde"
            ## write to logfile
            self.print_message(text, '\n')
            ## write to bot
            self.write_to_bot(text)
               
        return errcode


    ############################################################################
    ############################################################################
    def unconnect(self):
        ##  socket.shutdown(self.sock, SHUT_RD|SHUT_WR)
        self.sock.close()


    ############################################################################
    ### send command to device, read answer and operate with it
    ### \return 0 - OK
    ###         1 - command CLOSE
    ###         2 - error in receive data
    ###         3 - error in send data
    ############################################################################
    def request(self, command):
        command += '\r\n'
        #print(f"{command}", end='')
        print(f"request {datetime.now()}")

        ## --- send command ---
        time.sleep(1)
        bbytes = self.sock.send(command.encode())

        ## проверить, что все отправилось
        if bbytes != len(command):
            print(f"request: Error in sending data!! to {self.IPname}")
            return 3             
        #print('sent ', bbytes, 'bytes to the socket')

        if "CLOSE" in command:
            return 1

        ## --- 10 attempts to read buffer
        attempts = 0
        buf = ''
        self.sock.settimeout(60) # установка таймаута
        while(len(buf) == 0 and attempts < 10):
            time.sleep(1)
            attempts += 1
            buf = self.sock.recv(65536)
            if len(buf) == 0:
                print('not data,  buf lenght=', len(buf), ' attempt=', attempts)
            else:
                #print('qq, read buf(bbytes)=', len(buf))
                #print(buf)
                pass

        if attempts >= 10:
            print("request: Error in receive")
            self.sock.unconnect()
            return 2

        ##  --- parse buffer
        buf = buf.decode("UTF-8").strip()
        #self.print_message(buf)
        #self.print_message(buf)
        if self.check_answer():
            return 4

        self.buff = buf
        
        ### --- operate with command
        if "sendVal" in buf:
            self.write_data_to_raw_file(self.buff)
            
        ### --- write to csv file
        #convert_raw_file_to_csv(self.rawfilename)

        return 0


    ############################################################################
    ############################################################################
    def request_all(self):
        chans = ([0,1,2,3,4,5,6,  23,24,26,27,35,36,40,41,42,43,44,45,46,47,48,
                  50,51,52,53,54,55,56,  60,61,62,63,64,65,  77,78,110] + list(range(110, 174)))
                  #50,51,52,53,54,55,56,  60,61,62,63,64,65,  77,78,110] + list(range(100, 190)))
        request = f"<getVal{';'.join(str(n) for n in chans)}>"
        self.request(request) 


    ############################################################################
    ############################################################################
    def write_data_to_raw_file(self, message):
        ttime = datetime.now()
        self.rawfilename = self.datadir + self.sep + self.rawdirname + self.sep + "_".join(["_".join(str(datetime.now()).split('-')[:2]), self.device_name,  'raw.txt'])
        message = message.replace("<sendVal", "").replace(">", ";")
        with open(self.rawfilename, 'a') as flog:
            flog.write(f"{str(ttime)[:19]}; {int(datetime.timestamp(ttime))}; {message}\n")


    ############################################################################
    ############################################################################
    def check_answer(self):
        return 0


    ############################################################################
    ############################################################################
    def extract_device_name(self):
        buff = self.buff.split("\r\n")
        self.device_name = [x.split()[2] for x in buff if "serialnumb" in x][0]
        text = f'Device name: {self.device_name}'
        self.print_message(text, '\n')
        self.fill_header()


    ############################################################################
    ############################################################################
    def parse_raw_data(self):
        print('raw data:  ')
        if len(self.buff) < 10:
            return
        self.buff = self.buff.replace("AE33>","")
        print(self.buff)

        #mm, dd, yy = self.buff.split("|")[2][:10].split('/')
        mm, dd, yy = self.buff.split("|")[2].split(" ")[0].split('/')
        print('m, dd, yy = ',mm,dd,yy)
        if mm != self.mm or yy != self.yy:
            filename = self.datadir + self.sep + 'raw' + self.sep + filename
            print(filename)
            if self.file_raw:
                self.file_raw.close()
            self.file_raw = open(filename, "a")
        self.file_raw.write(self.buff+'\n')
            #self.file_raw.write('\n')

        self.file_raw.flush()
        self.mm = mm
        self.yy = yy







 
    ############################################################################
    ############################################################################
    def read_dataframe_from_csv_file(self, csvfilename): ## xlsfilename
        #columns = ['Date', 'Time (Moscow)', 'BC1', 'BC2', 'BC3', 'BC4', 'BC5', 'BC6',
        #    'BC7', 'BB(%)', 'BCbb', 'BCff', 'Date.1', 'Time (Moscow).1']
        columns = self.xlscolumns
        create_new = False

        try:
            ## read csv file to dataframe
            datum = pd.read_csv(csvfilename)
            #print(datum)
            print(csvfilename, "read, df: ", datum.shape)
            print(datum.head(2))
            if datum.shape[1] != len(columns) + 2:
                text = f"WARNING!!! File {csvfilename} has old format, is ignoring!!!"
                self.print_message(text, '\n')

                point = csvfilename.rfind('.')
                os.rename(csvfilename, csvfilename[:point] + "_old" +  csvfilename[point:])
                create_new = True
        except:
            create_new = True

        if create_new:
            # create new dummy dataframe
            datum = pd.DataFrame(columns=columns)
            text = "Can not open file: " + csvfilename + "  Empty dummy dataframe created"
            self.print_message(text, '\n')

        return datum


    ############################################################################
    ############################################################################
    def read_dataframe_from_excel_file(self, xlsfilename):
        #columns = ['Date', 'Time (Moscow)', 'BC1', 'BC2', 'BC3', 'BC4', 'BC5', 'BC6',
        #    'BC7', 'BB(%)', 'BCbb', 'BCff', 'Date.1', 'Time (Moscow).1']
        columns = self.xlscolumns
        create_new = False

        try:
            ## read excel file to dataframe
            ## need to make "pip install openpyxl==3.0.9" if there are problems with excel file reading
            datum = pd.read_excel(xlsfilename)
            print(xlsfilename, "read, df: ", datum.shape)
            print(datum.head(2))
            if datum.shape[1] != len(columns) + 2:
                text = f"WARNING!!! File {xlsfilename} has old format, is ignoring!!!"
                self.print_message(text, '\n')

                point = xlsfilename.rfind('.')
                os.rename(xlsfilename, xlsfilename[:point] + "_old" +  xlsfilename[point:])
                create_new = True
        except:
            create_new = True

        if create_new:
            # create new dummy dataframe
            datum = pd.DataFrame(columns=columns)
            text = "Can not open file: " + xlsfilename + "  Empty dummy dataframe created"
            self.print_message(text, '\n')

        return datum




 







############################################################################
############################################################################
def select_year_month(datastring):
    return "_".join([x for x in datastring.split()[0].split('.')[2:0:-1]])
    #return "_".join([x for x in datastring.split()[0].split('/')[:2]])
    #return datastring.split('/')[0] + '_' + datastring.split('/')[1]
