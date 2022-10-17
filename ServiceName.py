import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import logging
import sys

import main_trigger
import time

logging.basicConfig(filename='C:\PATH\service.log', format='[%(asctime)s] | %(levelname)s: %(message)s', level=logging.INFO)

class ServiceName(win32serviceutil.ServiceFramework):

    _exe_name_ = "Name of .exe file"
    _svc_name_ = "Name that will show under de service tree on Task Manager" # Note: the .exe has the name of the  .py file, this doesn't change it
    _svc_display_name_ = "Name that will show on Services window"
    _svc_description_ = "Description on Services window"

    # Constructor of the windows service
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        # socket.setdefaulttimeout(60)

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        
        # Logs service start to Event Viewer
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        
        # Sets running to True (just so we can use it in main)
        self.isrunning = True

        # Start main according to schedule
        main_trigger.start_rightTime(self.main)
    
    def SvcStop(self):
        """
        Called when the service is asked to stop
        """ 
        # Logs service stop to Event Viewer
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, ''))
        
        # Sets running to False (just so we can use it in main)
        self.isrunning = False
        
        # win32event.SetEvent(self.hWaitStop)

    def main(self):
        """
        Service main logic here
        """
        try:
            # This will keep service running
            while self.isrunning:           

                # Sleep 5 min then run again (example)
                time.sleep(300 - (time.time() % 300))
        except Exception as e:
            logging.info(str(e))

# __main__ block 
if __name__ == '__main__':
    
    # sys args to handle with command prompt functionalities (install, update, remove)
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ServiceName)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ServiceName)