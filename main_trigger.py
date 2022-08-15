import time

# This method forces the service to start at times multiple of 5

def start_rightTime(methodCall):

    wrongTime = True
    while(wrongTime is True):
        date = time.localtime()
        minutes = date.tm_min
        seconds = date.tm_sec

        try:
            str_min = str(minutes)[1]
        except:
            str_min = str(minutes)[0]

        str_sec = str(seconds)
        
        if(int(str_min) == 0 or int(str_min) == 5):
            if(int(str_sec) == 0):
                methodCall()
                wrongTime = False
        time.sleep(1) 