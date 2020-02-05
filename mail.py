from models import AadhaarAuthenticationMail
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
import re

class Mail:

    def __init__(self, uri):
        self.uri = uri

    def getData(self):
        
        def getAuthModality(data):
            test = 'using'
            found = False
            for d in data:
                if found:
                    text = d.text.strip()
                    if text[:1] == '"' and text[-1:] == '"':
                        text = text[1:-1].strip()
                    return text
                if re.search(test, str(d)):
                    found = True

        def getDate(data):
            test = re.compile(r'[0-9]{2}/[0-9]{2}/[0-9]{4}')
            for d in data:
                search_res = re.search(test, str(d))
                if search_res:
                    text = search_res.group(0)
                    return text

        def getTime(data):
            test = re.compile(r'[0-9]{2}:[0-9]{2}:[0-9]{2}')
            for d in data:
                search_res = re.search(test, str(d))
                if search_res:
                    text = search_res.group(0)
                    return text

        def getAUAName(data):
            test = 'deployed by'
            found = False
            for d in data:
                if found:
                    text = d.text.strip()
                    if text[:1] == '"' and text[-1:] == '"':
                        text = text[1:-1].strip()
                    return text
                if re.search(test, str(d)):
                    found = True

        def getUIDAIResponseCode(data):
            test = 'Response code'
            for d in data:
                if re.search(test, str(d)):
                    text = d.text.strip()
                    text = text[14:].strip()
                    return text

        def getAuthenticationResponse(data):
            for d in data:
                if re.search('success', str(d)):
                    text = 'Success'
                    return text
                if re.search('fail', str(d)):
                    text = 'Failure'
                    return text

        def getDataMethod1(soup):
            data = AadhaarAuthenticationMail()
            temp = [x for x in soup.find(id='demo').next_siblings]
            # The gernerator object soup.find(id='demo').next_siblings
            # loses items which have been iterated through
            # So created a list to iterte multiple times
            data.Auth_Modality = getAuthModality(temp)
            data.Date = getDate(temp)
            data.Time = getTime(temp)
            data.AUA_Name = getAUAName(temp)
            data.UIDAI_Response_Code = getUIDAIResponseCode(temp)
            data.Authentication_Response = getAuthenticationResponse(temp)
            return data

        def getDataMethod2(soup):
            data = AadhaarAuthenticationMail()
            temp1 = [x for x in soup.find(id='demo').next_siblings]
            temp2 = [x for x in soup.body.next_siblings]
            data.Auth_Modality = getAuthModality(temp1)
            data.Date = getDate(temp1)
            data.Time = getTime(temp1)
            data.AUA_Name = getAUAName(temp2)
            data.UIDAI_Response_Code = getUIDAIResponseCode(temp2)
            data.Authentication_Response = getAuthenticationResponse(temp1)
            return data

        with open(self.uri, 'rb') as file:
            msg = BytesParser(policy=policy.default).parse(file)
        msg_body = msg.get_body(preferencelist=('plain', 'html'))
        soup = BeautifulSoup(msg_body.get_content(), 'html.parser')
        method1data = getDataMethod1(soup)
        print('Data extracted method1: ', vars(method1data))
        if method1data.isClean():
            return method1data
        else:
            print("Data Not clean")
        method2data = getDataMethod2(soup)
        print('Data extracted method2: ', vars(method2data))
        if method2data.isClean():
            return method2data
        else:
            print("Data Not clean")