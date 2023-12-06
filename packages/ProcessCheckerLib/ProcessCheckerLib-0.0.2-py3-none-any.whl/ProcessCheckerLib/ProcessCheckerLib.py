import requests,os,sys,traceback

def TracebackChecker(Type,value,tb):
    err='Error: '+str(Type)+' '+str(value)+'. '+'line:'+str(traceback.extract_tb(tb)[-1].lineno)
    TBsend=requests.post('http://127.0.0.1:1488/tb',json={'name':os.path.basename(sys.argv[0]),'traceback':err})
def scriptTracker():
    PIDsend=requests.post('http://127.0.0.1:1488/PID',json={'name':os.path.basename(sys.argv[0]),'pid':str(os.getpid())})
    sys.excepthook = TracebackChecker
    sys.unraisablehook = TracebackChecker
