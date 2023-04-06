from Task.NetworkTask import NetworkTask,TaskMessage,VisitConfig
from Task.BigTask import BigTask,Task

class AuthorVedioListTask(NetworkTask):
    def __init__(self) -> None:
        self.url = 'https://api.bilibili.com/x/space/wbi/arc/search?mid={}&ps=&tid=&pn=&keyword=&order=pubdate&platform=web&web_location=&order_avoided=true&w_rid=&wts='
        self.visitUrl= 'JSON://data/list/vlist/'
    def init(self, message: TaskMessage) -> VisitConfig:
        id = message.getData('AuthorId')
        visiturl = self.url.format(id)
        # print(visiturl)
        return VisitConfig.Builder()\
        .addWayUrl("Vedios",self.visitUrl)\
        .setWebUrl(visiturl)\
        .getWay()\
        .build()
    
    def execute(self, visitResult, message: TaskMessage) -> TaskMessage:
        result = visitResult['Vedios']
        message.setData('Vedio',result)
        return message


# print(message.getData('Vedio'))
#TODO: 我们是否需要所有的评论

class VedioCommitTask(NetworkTask):
    def __init__(self):
        self.url = 'https://api.bilibili.com/x/v2/reply/main?csrf=&mode=3&next={}&oid={}&plat=&seek_rpid=&type=1'
        self.visitUrl = 'JSON://data/replies/'
        super().__init__()
    def init(self, message: TaskMessage) -> VisitConfig:
        id = message.getData('aid')
        page = message.getData('page')
        # print('dic'*10,message.getDic())
        
        # print('id'*10,id)
        self.aid = id
        self.page = page
        visiturl = self.url.format(page,id)
        return VisitConfig.Builder()\
        .addWayUrl("repley",self.visitUrl)\
        .setWebUrl(visiturl)\
        .getWay()\
        .setDelayTime(1)\
        .build()
    
    def execute(self, visitResult, message: TaskMessage) -> TaskMessage:
        # print(visitResult)
        res = []
        for commit in visitResult['repley']:
            if commit.get('replies',None) is not None:
                followCommit = commit.get('replies')
                for x in followCommit:
                    res.append(self.executeCommit(x))
            res.append(self.executeCommit(commit))
        # print('res'*20,res)
        message.setData('commits',res)
        return message
    def executeCommit(self,data):
        
        t = {}
        t ['aid'] = self.aid
        t['content'] = data['content']['message']
        t['like'] = data['like']
        t['pageno'] = self.page
        return t

def collectResult( message: TaskMessage):
    res = []
    for msg in message.getData('commits'):
            current = msg['commits']
            res.extend(current)
    return res

def generaorNPageMessage(aid,Maxpage):
    t = TaskMessage()
    res = [ {'page':pageno,'aid':aid}  for pageno in range(1,Maxpage+1)]
    t.setData('Vedio',res)
    return t

# # message = TaskMessage()
# Vedio = {'aid':55887397}
# # message.setData('Vedio',Vedio)
# message = TaskMessage()
# message.setData('AuthorId',14387720)
# result=  AuthorVedioListTask().run(message)
# Videos = result.getData('Vedio')

# result = []
# for vedio in Videos:
#     message = generaorNPageMessage(vedio['aid'],5)
#     task = BigTask(VedioCommitTask(),'Vedio','commits')
#     x = task.run(message)
#     res = collectResult(x)
#     result.extend(res)
# print(result)

# exit()


# x = task.run(result)
# res = collectTask().run(x)
# print(len(res.getData('resultComments')))