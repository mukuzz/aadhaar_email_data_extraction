class AadhaarAuthenticationMail:
    def __init__(self, Auth_Modality=None,Date=None,Time=None,AUA_Name=None,UIDAI_Response_Code=None,AUA_Transaction_ID=None,Authentication_Response=None,UIDAI_Error_Code=None):
        self.Auth_Modality = Auth_Modality
        self.Date = Date
        self.Time = Time
        self.AUA_Name = AUA_Name
        self.UIDAI_Response_Code = UIDAI_Response_Code
        self.AUA_Transaction_ID = AUA_Transaction_ID
        self.Authentication_Response = Authentication_Response
        self.UIDAI_Error_Code = UIDAI_Error_Code

    def __str__(self):
        response = ''
        attrs = ['Auth_Modality','Date','Time','AUA_Name','UIDAI_Response_Code','AUA_Transaction_ID','Authentication_Response','UIDAI_Error_Code']
        for attr in attrs:
            attr_value = getattr(self, attr)
            if attr_value != None:
                response += attr_value
            response += ','
        return response[:-1]

    def isClean(self):
        return self.Auth_Modality != None and self.Date != None \
            and self.Time != None and self.AUA_Name != None \
            and self.UIDAI_Response_Code != None \
            and self.Authentication_Response != None