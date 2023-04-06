from Tasks.AuthorVedioListTask import *
from Task.BigTask import BigTask
import pandas as pd
import tqdm


def GetCommentsByAvid(avid,maxPage):

    result = []

    message = generaorNPageMessage(avid,maxPage)
    task = BigTask(VedioCommitTask(),'Vedio','commits')
    x = task.run(message)
    res = collectResult(x)
    result.extend(res)
    comments = pd.DataFrame.from_records(result)
    return comments

def GetAuthorComments(aid,maxPage):
    message = TaskMessage()
    message.setData('AuthorId',aid)
    result=  AuthorVedioListTask().run(message)
    # print(result.getDic())
    Videos = result.getData('Vedio')

    result = []
    vedios = pd.DataFrame.from_records(Videos)
    vedios = vedios[['aid','title']]

    for vedio in tqdm.tqdm(Videos):
        message = generaorNPageMessage(vedio['aid'],maxPage)
        task = BigTask(VedioCommitTask(),'Vedio','commits')
        x = task.run(message)
        res = collectResult(x)
        # print(len(res),res)
        result.extend(res)


    comments = pd.DataFrame.from_records(result)
    return vedios,comments

def writeToCSV(df,path=''):
    df.to_csv(path,mode='w+',encoding='utf_8_sig',index=False)
