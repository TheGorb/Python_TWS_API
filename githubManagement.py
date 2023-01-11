from git import Repo
from time import sleep

class githubManagementClass():
    def pushTextFile():
        repo = Repo("TWSOutput/")

        while(True):
            repo.git.add('/TWSOutput/twsOrderOutput.txt');
            repo.git.commit(m='Update text file')
            repo.git.push()
            sleep(650);