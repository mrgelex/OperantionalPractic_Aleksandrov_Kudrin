import subprocess
def runserver():
    subprocess.run(['python', 'inter\manage.py', 'runserver'])
if __name__ == '__main__':
    runserver()