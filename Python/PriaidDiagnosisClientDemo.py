import PriaidDiagnosisClient
import random
import config
import sys
import os
import json
import string

# import keras 
sys.path.append('C:\Capstone\translators')
sys.path.append('C:\Capstone\speech')
from translators.apis import *
from transcribe_streaming_mic import *
class PriaidDiagnosisClientDemo:
    'Demo class to simulate how to use PriaidDiagnosisClient'

    def __init__(self):
        username = config.username
        password = config.password
        authUrl = config.priaid_authservice_url
        healthUrl = config.priaid_healthservice_url
        language = config.language
        self._printRawOutput = config.pritnRawOutput

        self._diagnosisClient = PriaidDiagnosisClient.DiagnosisClient(username, password, authUrl, language, healthUrl)
    # 시뮬 레이터 코드 Client에서 사용 
    def simulate(self):
        # Load body locations
        selectedLocationID = self._loadBodyLocations()

        # Load body sublocations
        selectedSublocationID = self._loadBodySublocations(selectedLocationID)

        # Load body sublocations symptoms
        selectedSymptoms = self._loadSublocationSymptoms(selectedSublocationID)

        # Load diagnosis
        diagnosis = self._loadDiagnosis(selectedSymptoms)

        # Load specialisations
        self._loadSpecialisations(selectedSymptoms)

        # Load issue info
        for issueId in diagnosis:
            self._loadIssueInfo(issueId)

        # Load proposed symptoms
        self._loadProposedSymptoms(selectedSymptoms)
    
    # 출력 메크로 
    def _writeHeaderMessage(self, message):
        print("---------------------------------------------")
        print(message)
        print("---------------------------------------------")

    # 출력 메크로 
    def _writeRawOutput(self, methodName, data):
        print("")
        if self._printRawOutput: 
            print("+++++++++++++++++++++++++++++++++++++++++++++")
            print("Response from method {0}: ".format(methodName))
            print(json.dumps(data))
            print("+++++++++++++++++++++++++++++++++++++++++++++")

    # 몸의 가장 큰 위치 출력 
    def _loadBodyLocations(self):
        bodyLocation_lists = []
        bodyLocations = self._diagnosisClient.loadBodyLocations()
        self._writeRawOutput("loadBodyLocations", bodyLocations)


        if not bodyLocations:
            raise Exception("Empty body locations results")
        
        self._writeHeaderMessage("Body locations:")    
        i=0
        for bodyLocation in bodyLocations:
            body_lists = bodyLocation["Name"].replace(",","")
            body_lists = body_lists.replace("&","")
            bodyLocation_lists.append(google(body_lists.split(),to_language='ko'))
            print(body_lists)
            print(bodyLocation_lists[i])
            i=i+1

    # 음성 입력 부분 
        #bodyLct =  google(main(),to_language='ko')
        bodyLct = input() #타자로 입력 
        
        i=0
        for bodyLCT in bodyLocation_lists:
            if bodyLCT.find(bodyLct) != -1:
                selectLocation = bodyLocations[i]
                break
            i = i+1

               
        while(True):
            try:
                self._writeHeaderMessage("Selected location: {0}".format(selectLocation["Name"]))
                break
            except UnboundLocalError:
                i=0
                print("Wrong input, Say it again")
                #bodySlct =  google(main(),to_language='ko')
                bodyLct = input()
                for bodyLCT in bodyLocation_lists:
                    if bodyLCT.find(bodyLct) != -1:
                        selectLocation = bodyLocations[i]
                        break
                    i = i+1
                
        return  selectLocation["ID"] # 아이디 값을 전송 
    
    # 몸의 작은 부위 위치 출력
    def _loadBodySublocations(self, locId):
        bodySubLocation_lists = []
        bodySubLocations = self._diagnosisClient.loadBodySubLocations(locId)
        self._writeRawOutput("loadBodySubLocations", bodySubLocations)
        
        if not bodySubLocations:
            raise Exception("Empty body sublocations results")
        
        i=0
        for bodySubLocation in bodySubLocations:
            body_sub_lists = bodySubLocation["Name"].replace(",","")
            body_sub_lists = body_sub_lists.replace("&","") 
            bodySubLocation_lists.append(google(body_sub_lists.split(),to_language='ko'))       
            print(body_sub_lists)
            print(bodySubLocation_lists[i]) 
            i = i+1
           
    # 음성 입력 부분
        #bodySlct =  google(main(),to_language='ko')
        bodySlct = input() #타자로 입력
        
        i=0
        for bodySLCT in bodySubLocation_lists:
            if bodySLCT.find(bodySlct) != -1:
                selectSubLocation = bodySubLocations[i]
                break
            i = i+1
        
        while(True):   
            try:
                self._writeHeaderMessage("Selected Sublocations: {0}".format(selectSubLocation["Name"]))
                break
            except UnboundLocalError:
                i=0
                print("Wrong input, Say it again")
                #bodySlct =  google(main(),to_language='ko')
                bodySlct = input() #타자로 입력 
                for bodySLCT in bodySubLocation_lists:
                    if bodySLCT.find(bodySlct) != -1:
                        selectSubLocation = bodySubLocations[i]
                        break
                    i = i+1
        return selectSubLocation["ID"] # 아이디 값을 전송 

     # 몸의 증상 들 출력
    def _loadSublocationSymptoms(self, subLocId):
        symptoms_list = []
        symptoms = self._diagnosisClient.loadSublocationSymptoms(subLocId, PriaidDiagnosisClient.SelectorStatus.Man)
        self._writeRawOutput("loadSublocationSymptoms", symptoms)

        if not symptoms:
            raise Exception("Empty body sublocations symptoms results")

        self._writeHeaderMessage("Body sublocations symptoms:")

        for symptom in symptoms:
            print(google(symptom["Name"], to_language='ko'))# 증상 한글 출력
            print(symptom["Name"]) # 증상 한글 출력 
            symptoms_list.append(google(symptom["Name"], to_language='ko').replace(" ",""))
        
      
        # 문장 처리 해야됨 # 음성 입력 부분
        #Symptoms = main().replace(" ","") 
        Symptoms = input().replace(" ","")
        i=0
        for Symptom in symptoms_list:
            if Symptom.find(Symptoms) != -1:
                selectSymptoms = symptoms[i]
                break
            i=i+1
        
        while(True):
            try:
                self._writeHeaderMessage("Selected symptom: {0}".format(selectSymptoms["Name"]))
                break
            except UnboundLocalError:
                print("Wrong input, Say it again")
                Symptoms = input().replace(" ","")
                i=0
                for Symptom in symptoms_list:
                    if Symptom.find(Symptoms) != -1:
                        selectSymptoms = symptoms[i]
                        break
                    i=i+1
        self._loadRedFlag(selectSymptoms)

        selectedSymptoms = [selectSymptoms]
        return selectedSymptoms
        
    # 도출된 증상 출력 
    def _loadDiagnosis(self, selectedSymptoms):
        self._writeHeaderMessage("Diagnosis")
        selectedSymptomsIds = []
        for symptom in selectedSymptoms:
            selectedSymptomsIds.append(symptom["ID"])
            
        diagnosis = self._diagnosisClient.loadDiagnosis(selectedSymptomsIds, PriaidDiagnosisClient.Gender.Male, 1988)
        self._writeRawOutput("loadDiagnosis", diagnosis)
        
        if not diagnosis:
            self._writeHeaderMessage("No diagnosis results for symptom {0}".format(selectedSymptoms[0]["Name"]))

        for d in diagnosis:
            specialisations = []
            for specialisation in d["Specialisation"]:
                specialisations.append(specialisation["Name"])
            print("{0} - {1}% \nICD: {2} {3}\nSpecialisations : {4}\n".format(google(d["Issue"]["Name"],to_language='ko'), d["Issue"]["Accuracy"], d["Issue"]["Icd"], d["Issue"]["IcdName"], google(",".join(x for x in specialisations),to_language='ko')))

        diagnosisIds = []
        for diagnose in diagnosis:
            diagnosisIds.append(diagnose["Issue"]["ID"])

        return diagnosisIds

    # 도출된 증상 출력 
    def _loadSpecialisations(self, selectedSymptoms):
        self._writeHeaderMessage("Specialisations")
        selectedSymptomsIds = []

        for symptom in selectedSymptoms:
            selectedSymptomsIds.append(symptom["ID"])

        specialisations = self._diagnosisClient.loadSpecialisations(selectedSymptomsIds, PriaidDiagnosisClient.Gender.Male, 1988)
        self._writeRawOutput("loadSpecialisations", specialisations)
        
        if not specialisations:
            self._writeHeaderMessage("No specialisations for symptom {0}".format(selectedSymptoms[0]["Name"]))
                                                                                                     
        for specialisation in specialisations:
            print("{0} - {1}%".format(google(specialisation["Name"],to_language='ko'), specialisation["Accuracy"]))

    # 도출된 증상 출력
    def _loadRedFlag(self, selectedSymptom):
        redFlag = "Symptom {0} has no red flag".format(selectedSymptom["Name"])
            
        if selectedSymptom["HasRedFlag"]:
            redFlag = self._diagnosisClient.loadRedFlag(selectedSymptom["ID"])
            self._writeRawOutput("loadRedFlag", google(redFlag,to_language='ko'))

        self._writeHeaderMessage(redFlag)

    # 도출된 증상 최종 종합 출력
    def _loadIssueInfo(self, issueId):
        issueInfo = self._diagnosisClient.loadIssueInfo(issueId)
        self._writeRawOutput("issueInfo", issueInfo)
        
        self._writeHeaderMessage("Issue info")
        print("Name: {0}".format((google(issueInfo["Name"], to_language='ko'))))
        print("Professional Name: {0}".format(google(issueInfo["ProfName"], to_language='ko')))
        print("Synonyms: {0}".format(google(issueInfo["Synonyms"], to_language='ko')))
        print("Short Description: {0}".format(google(issueInfo["DescriptionShort"], to_language='ko')))
        print("Description: {0}".format(google(issueInfo["Description"], to_language='ko')))
        print("Medical Condition: {0}".format(google(issueInfo["MedicalCondition"], to_language='ko')))
        print("Treatment Description: {0}".format(google(issueInfo["TreatmentDescription"], to_language='ko')))
        print("Possible symptoms: {0} \n\n".format(google(issueInfo["PossibleSymptoms"], to_language='ko')))


    def _loadProposedSymptoms(self, selectedSymptoms):
        selectedSymptomsIds = []
        for symptom in selectedSymptoms:
            selectedSymptomsIds.append(symptom["ID"])
        
        proposedSymptoms = self._diagnosisClient.loadProposedSymptoms(selectedSymptomsIds, PriaidDiagnosisClient.Gender.Male, 1988)
        self._writeRawOutput("proposedSymptoms", proposedSymptoms)

        if not proposedSymptoms:
            self._writeHeaderMessage("No proposed symptoms for selected symptom {0}".format(selectedSymptoms[0]["Name"]))
            return

        #proposedSymptomsIds = []
        # for proposeSymptom in proposedSymptoms:
        #     proposedSymptomsIds.append(proposeSymptom["ID"])
            
        # self._writeHeaderMessage("Proposed symptoms: {0}".format(",".join(str(x) for x in proposedSymptomsIds)))


diagnosisClientDemo = PriaidDiagnosisClientDemo()
diagnosisClientDemo.simulate()
