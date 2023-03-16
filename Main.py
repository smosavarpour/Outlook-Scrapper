import asyncio
import configparser
from graph import Graph
import pandas as pd
from bs4 import BeautifulSoup
#!!!!!!!!!!!!!!! NEXT STEP: LINE 89
#!!!!!!!!!!!!!!! ALSO, IF EMAIL IS LISTED AS 'NOT READ' IN TTHE SHEET, BUT THEN IS READ LATER ON, IT WILL NOT REMOVE THE UNREAD ONE SINCE ITS NOT TECHINICALLY A DUPLICATE
async def main():
    print('Python Graph Tutorial\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    await greet_user(graph)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit \n' )
        #print('1. Display access token \n')
        print('2. List and pull inbox \n')

        try:
            choice = int(input())
        except ValueError:
            choice = -1

        if choice == 0:
            print('Goodbye...')
        elif choice == 1:
            await display_access_token(graph)
        elif choice == 2:
            await list_inbox(graph)
        else:
            print('Invalid choice!\n')

async def greet_user(graph: Graph):
    user = await graph.get_user()
    if user is not None:
        print('Hello,', user.display_name)
        # For Work/school accounts, email is in mail property
        # Personal accounts, email is in userPrincipalName
        print('Email:', user.mail,'\n')

async def display_access_token(graph: Graph):
    token = await graph.get_user_token()
    print('User token:', token, '\n')

async def list_inbox(graph: Graph):
    message_page = await graph.get_inbox()
    existList = pd.read_excel('Book1.xlsx')#.set_index('Ticket#') 
    #existList.set_index('Ticket#', inplace=True)
    inboxList = {
        'Ticket#': [],
        'From': [],
        'Subject': [],
        'Date': [],
        'Read': [],
        'Body':[]
    }


    if (message_page is not None and message_page.value is not None):
        for currMessage in message_page.value: 
 
            inboxList['Ticket#'].append(0)
            inboxList['From'].append(currMessage.from_.email_address.name)
            inboxList['Subject'].append(currMessage.subject)
            inboxList['Date'].append(currMessage.received_date_time)
            inboxList['Read'].append(int(currMessage.is_read))
            inboxList['Body'].append(get_body(currMessage.body.content))
            type(currMessage.body.content)
    
    print('\nList of pulled emails: \n', pd.DataFrame(inboxList) )

    inboxList = export_prep(inboxList, existList)
    print('After Prep_export: \n',inboxList)

    #inboxListDF = pd.DataFrame(inboxList)
    print('Final list to be exported: \n', inboxList)
    inboxList.to_excel('Book1.xlsx')
    #print('END OF FUNCTION')


def export_prep(inboxList, existList):
    inboxList = pd.DataFrame(data=inboxList)#.set_index('Ticket#')
    inboxList['Date'] = inboxList['Date'].dt.tz_localize(None)
    inboxListDF =  pd.concat([inboxList, existList]).drop_duplicates(subset=['Subject','From','Date'],keep='last')
    return assign_ticket(inboxListDF).set_index('Ticket#')

def assign_ticket(concatList):
    count = len(concatList) - 1
    tickNum = []

    for c in range(count, -1, -1):
        tickNum.append(c)
        
    test = len(concatList['Ticket#'])
    concatList['Ticket#'] = tickNum
    
    """ for x in concatList['From']:
        if concatList["Ticket#"][0] == 0: #cant do this anymore bc 'concatList' gets passed a DataFrame but this line is still treatg it like a dictionary.
            concatList['Ticket#'].pop(0)
        concatList['Ticket#'].append(count)
        count -= 1 """

    return concatList

def get_body(mailBody):
    return BeautifulSoup(mailBody, features="html.parser").get_text()



# RUN MAIN
asyncio.run(main())
