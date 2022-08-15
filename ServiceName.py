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

    _svc_name_ = "Name that will show under de service tree on Task Manager" # Note: the .exe has the name of the  .py file, this doesn't change it
    _svc_display_name_ = "Name that will show on Services window"
    _svc_description_ = "Description on Services window"

    # Constructor of the windows service
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    # Called when the service is asked to start
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.isrunning = True

        # Start main according to schedule
        main_trigger.start_rightTime(self.main)
    
    # Called when the service is asked to stop
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.isrunning = False
        win32event.SetEvent(self.hWaitStop)

    # Main function (run logic here)
    def main(self):

        try:
            # This will keep your service running
            while self.isrunning:           

                # Sleep 5 min then run again (example)
                time.sleep(300 - (time.time() % 300))
        except Exception as e:
            logging.info(str(e))

# Checks if module is main and sys args to handle with command prompt functionalities (install, update, remove)
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ServiceName)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ServiceName)