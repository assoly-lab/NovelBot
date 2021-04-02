import requests
from bs4 import BeautifulSoup as bs
import os
import time
import smtplib
import concurrent.futures
# import multiprocessing

def getNovels(url,className):
    novels = {}
    page = requests.get(url)
    if page.status_code == 200 :
        soup = bs(page.content,"html.parser")

        novel_sections = soup.find_all(class_=className)
        for section in novel_sections:
            novel_title =section.find("a")
            novels.update({novel_title["title"]:novel_title["href"]})
            
    else:
        print("couldn't get the page")
    return novels



def novelsManager(old_novels,url,className):
    newely_added_novels = {}
    time.sleep(120)
    new_novels = getNovels(url,className)
    if old_novels.keys() == new_novels.keys():
        print("both dict match , no new novels")
    else:
        for i,j in zip(old_novels.keys(),new_novels.keys()):
            if i != j :
                newely_added_novels.update({j : new_novels[j]})
            else:
                pass
    return newely_added_novels




def sendEmail(novels):
    #sawb chi email bach t3od tsift bih
    EmailAddr = "test@gmail.com"
    password ="password"
    addrs = ["E-mail li bghiti tsift lih,ila kano kter mn wahd zido 7dah"]
    if novels:
        if len(novels.keys()) > 1 :
            subject = "there are {} novels.\n".format(len(novels.keys()))
            for novel,novel_link in zip(novels.keys(),novels.values()):
                body +=f"[{novel}] the link to it is:  {novel_link}\n"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as account :
                    account.login(EmailAddr,password)
                    msg = f"Subject: {subject} \n \n {body}"
                    account.sendmail(from_addr=EmailAddr,to_addrs=addrs,msg=msg)
        else:
            subject ="there is 1 new novel !"
            body = "[{}] the link to it is: {}".format(list(novels.keys())[0],list(novels.values())[0])
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as account :
                account.login(EmailAddr,password)
                msg = f"Subject: {subject} \n \n {body}"
                account.sendmail(from_addr=EmailAddr,to_addrs=addrs,msg=msg)

oldNovels = {}
def mainFunc(url,className):
    global oldNovels
    if oldNovels:
        newelyAdded = novelsManager(oldNovels,url,className)
        newNovels = getNovels(url,className)
        sendEmail(newelyAdded)
        oldNovels = newNovels
    else:
        newNovels = getNovels(url,className)
        newelyAdded = novelsManager(newNovels,url,className)
        sendEmail(newelyAdded)
        oldNovels = newNovels
urls_classes = {
    "https://supernovel.net/novel/?m_orderby=new-manga":"item-thumb",
    "https://www.asurascans.com/manga?status=&type=&order=latest":"bsx",
}

# for process,url,className in zip(len(urls_classes.keys()),urls_classes.keys(),urls_classes.values()):
#     p = 

# p1 = multiprocessing.Process(target=mainFunc,args=["https://supernovel.net/novel/?m_orderby=new-manga","item-thumb"])
# p2 = multiprocessing.Process(target=mainFunc,args=["https://www.asurascans.com/manga?status=&type=&order=latest","bsx"])

# if __name__ =="__main__":
#     start = time.perf_counter()
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     finish = time.perf_counter()
#     print(f"finished in {start - finish } seconds")
threads = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    t1 = executor.submit(mainFunc,"https://supernovel.net/novel/?m_orderby=new-manga","item-thumb")
    t2 = executor.submit(mainFunc,"https://www.asurascans.com/manga?status=&type=&order=latest","bsx")
    t1.result()
    t2.result()


