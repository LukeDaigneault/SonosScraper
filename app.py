from leboncoin_api_wrapper import Leboncoin
import schedule
import time
import webbrowser
import os.path


lbc = Leboncoin()


def writeFileList(results):
    with open('./lastrun.txt', 'w') as lr:
        for line in results:
            lr.write(line)
            lr.write('\n')


def readFileList():
    fileset = set()
    with open('./lastrun.txt', 'r') as lr:
        for line in lr:
            fileset.add(line.strip('\n'))

    return fileset


def job():

    lbc.searchFor("sonos connect")
    lbc.maxPrice(300)
    results = lbc.execute()
    resultset = set()
    lastrunset = set()

    for ad in results['ads']:
        resultset.add(ad['url'])

    if os.path.isfile('./lastrun.txt'):

        lastrunset = readFileList()

        for newAdd in resultset - lastrunset:
            webbrowser.get('chromium').open_new_tab(newAdd)
        writeFileList(resultset)
    else:
        writeFileList(resultset)


schedule.every(5).minutes.do(job)
job()

while True:
    schedule.run_pending()
    time.sleep(1)
