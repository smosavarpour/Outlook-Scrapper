import pandas as pd

inboxList = {
        'Ticket#': [0,1,2],
        'From': [0,0,0],
        'Subject': [0,0,0],
        'Date': [0,0,0],
        'Read': [0,0,0],
        'Body':[0,0,0]
    }


df = pd.DataFrame(inboxList)
df1 = pd.DataFrame(df['From'])

print(df1)
