from git import Repo
from time import sleep

class githubManagementClass():
    def pushTextFile():
        repo = Repo(".")

        while(True):
            sleep(650);
            repo.git.add('./output/twsOrderOutput.txt');
            repo.git.commit(m='Update text file')
            repo.git.push()