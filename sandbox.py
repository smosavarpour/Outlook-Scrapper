import pandas as pd

emailDic = { #representing pullEmail
        'Ticket#': [1,2,4],
        'From': ['sam','brad','jay'],
        'Subject': [1,2,3],
        'Date': [4,5,3],
        'Read': [7,8,3]
    }

listDic = { #representing existList
        'Ticket#': [1,2,3],
        'From': ['sam','brad', 'log'],
        'Subject': [1,2,3],
        'Date': [4,5,6],
        'Read': [7,8,9]
    }
    

emailDic = pd.DataFrame(emailDic)
listDic = pd.DataFrame(listDic)
maxCount = len(emailDic) + len(listDic)
print(maxCount)
count = len(pd.concat([listDic, emailDic]).drop_duplicates())
print(count)



maxCount -= count
print(maxCount)