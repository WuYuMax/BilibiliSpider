from utils import *

# vedios,comments = GetAuthorComments(14387720,10)

# writeToCSV(vedios,'./result/vedios.csv')
# writeToCSV(comments,'./result/x.csv')
comments = GetCommentsByAvid(269578092,10)
writeToCSV(comments,'./result/test3.csv')
