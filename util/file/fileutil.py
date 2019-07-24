import os
class FileUtil(object):

    @classmethod
    def getProjectObsPath(self):
        projectObsPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return projectObsPath

if __name__ == '__main__':
    print(FileUtil.getProjectObsPath())