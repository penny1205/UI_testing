from util.unittest.unittestutil import UnitTestUtil
from util.report.reporting import ReportUtil
from util.file.fileutil import FileUtil
from util.mail.sendmail import SendMail
from util.config.yaml.readyaml import ReadYaml

import time

if __name__ == '__main__':
    try:
        time.sleep(10)
        config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
        bvtcases = UnitTestUtil().discover_pattern(FileUtil.getProjectObsPath() + '/testcase/', '*.py')

        ReportUtil().generate_report(bvtcases, config['email_title'] + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), 'qa testing report', FileUtil.getProjectObsPath() + '/report/report.html')
        reader = open(FileUtil.getProjectObsPath() + '/report/report.html', 'rb')
        mail_body = reader.read()
        reader.close()
        SendMail().send_mail(config['email_receiver'],
                             config['email_sender'], config['email_sender_pwd'],config['email_host'],
                             config['email_title'] + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), mail_body,
                             {FileUtil.getProjectObsPath() + '/report/report.html'})
        print('BctCase run success!')
    except Exception:
        print('BctCase run fail!')
        raise
