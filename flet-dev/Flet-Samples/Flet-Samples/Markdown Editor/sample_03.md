# Python���� ���� Windows ���� �� ����?
������ Python �� pywin32 ���̺귯���� ���� Windows ���� ���ø����̼��� ������ ���Դϴ�.

`sample_service.py`
``` py
import win32serviceutil
import win32service
import win32event
import time

class SampleService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SampleService"
    _svc_display_name_ = "Sample Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        while True:
            time.sleep(30)
            rc = win32event.WaitForSingleObject(self.hWaitStop, 0)
            if rc == win32event.WAIT_OBJECT_0:
                break

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(SampleService)
```

�� ������ ��׶��忡�� ����ǰ� �Ϻ� �۾��� �ֱ������� �����ϴ� �⺻ Windows ���񽺸� �����մϴ�. �� ���񽺴� �ٸ� Windows ���񽺿� ���������� ����, ����, ��ġ �� ������ �� �ֽ��ϴ�. ������ ��Ȯ�� ������ SvcDoRun �޼����� ���� �����Ͽ� ����� ������ �� �ֽ��ϴ�.

### Python���� ���� Windows ���� �� ������ �ۼ��ϰ� �����ϴ� ����� �����Դϱ�?
Python���� ���� Windows ���� ���ø����̼��� �ۼ��ϰ� �����Ϸ��� ���� �ܰ踦 �����ʽÿ�.

1. pywin32 ���̺귯�� ��ġ: �͹̳ο��� ���� ����� �����Ͽ� pip�� ����Ͽ� ���̺귯���� ��ġ�� �� �ֽ��ϴ�.

   ``` cmd
   pip install pywin32
   ```

2. Python ��ũ��Ʈ �����: �ؽ�Ʈ �����⸦ ���� sample_service.py��� �� ������ ����ϴ�. ���� �亯���� ������ ���� ���񽺿� ���� �ڵ带 �� ���Ͽ� �����Ͽ� �ٿ��ֽ��ϴ�.

3. ������ �����ϰ� �ݽ��ϴ�.

4. ���� ��ġ: �͹̳��� ���� sample_service.py ������ ���Ե� ���͸��� �̵��� �� ���� ����� �����մϴ�.

   ``` cmd
   python sample_service.py install
   ```

5. ���� ����: ���񽺸� �����Ϸ��� ���� ����� �����մϴ�.
   ``` cmd
   python sample_service.py start
   ```

6. ���񽺰� ���� ������ Ȯ��: Windows �˻� ǥ���ٿ� 'Services'�� �Է��ϰ� 'service' ����� Ŭ���Ͽ� �׼����� �� �ִ� Windows���� ���� �����ڸ� ���� ���񽺰� ���� ������ Ȯ���� �� �ֽ��ϴ�. ���� �����ڿ��� 'Sample Service'�� ã�� ���°� '���� ��'���� Ȯ���մϴ�.

7. ���� ����: ���񽺸� �����Ϸ��� ���� ����� �����մϴ�.
   ``` cmd
   python sample_service.py stop
   ```

8. ���� ����: ���񽺸� �����Ϸ��� ���� ����� �����մϴ�.
   ``` cmd
   python sample_service.py remove
   ```

����: ���񽺸� ��ġ�ϰ� �����Ϸ��� �͹̳��� �����ڷ� �����ؾ� �� �� �ֽ��ϴ�.



