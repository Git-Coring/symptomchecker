import PriaidDiagnosisClient
import random
import config
import sys
import os
import json
import string
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
    

    def _writeHeaderMessage(self, message):
        print("---------------------------------------------")
        print(message)
        print("---------------------------------------------")


    def _writeRawOutput(self, methodName, data):
        print("")
        if self._printRawOutput: 
            print("+++++++++++++++++++++++++++++++++++++++++++++")
            print("Response from method {0}: ".format(methodName))
            print(json.dumps(data))
            print("+++++++++++++++++++++++++++++++++++++++++++++")

  
    def _loadBodyLocations(self):
        bodyLocations = self._diagnosisClient.loadBodyLocations()
        self._writeRawOutput("loadBodyLocations", bodyLocations)


        if not bodyLocations:
            raise Exception("Empty body locations results")
        
        self._writeHeaderMessage("Body locations:")    
        
        for bodyLocation in bodyLocations:
            BodyName = google(bodyLocation["Name"],to_language='ko')
            print("{0}".format(BodyName))
            print("{0}".format(bodyLocation["Name"]))
            


        
        bodyLct = google(main(),to_language='en').lower()  

        for bodyLCT in bodyLocations:
            if bodyLct in bodyLCT["Name"].lower():
                selectLocation = bodyLCT

        self._writeHeaderMessage("Selected location: {0}".format(selectLocation["Name"]))
        return  selectLocation["ID"]


    def _loadBodySublocations(self, locId):
        bodySublocations = self._diagnosisClient.loadBodySubLocations(locId)
        self._writeRawOutput("loadBodySubLocations", bodySublocations)

        if not bodySublocations:
            raise Exception("Empty body sublocations results")
    
        for bodySublocation in bodySublocations:
            BodySubName = google(bodySublocation["Name"],to_language='ko')
            print("{0}".format(BodySubName))
            print("{0}".format(bodySublocation["Name"]))
    
    
        bodySlct =  google(main(),to_language='en').lower()
        
        for bodySLCT in bodySublocations:
            if bodySlct in bodySLCT["Name"].lower():
                selectSubLocation = bodySLCT

        self._writeHeaderMessage("Selected Sublocations: {0}".format(selectSubLocation["Name"]))
        return selectSubLocation["ID"]


    def _loadSublocationSymptoms(self, subLocId):
        symptoms = self._diagnosisClient.loadSublocationSymptoms(subLocId, PriaidDiagnosisClient.SelectorStatus.Man)
        self._writeRawOutput("loadSublocationSymptoms", symptoms)

        if not symptoms:
            raise Exception("Empty body sublocations symptoms results")

        self._writeHeaderMessage("Body sublocations symptoms:")

        for symptom in symptoms:
            print(google(symptom["Name"], to_language='ko'))
            print(symptom["Name"])

        # 문장 처리 예외처리 해야됨 
        Symptoms = google(google(input(),to_language='en').lower()
        
        for Symptom in symptoms:
            if Symptoms in Symptom["Name"].lower():
                selectSymptoms = Symptom

        self._writeHeaderMessage("Selected symptom: {0}".format(selectSymptoms["Name"]))

        self._loadRedFlag(selectSymptoms)

        selectedSymptoms = [selectSymptoms]
        return selectedSymptoms


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


    def _loadRedFlag(self, selectedSymptom):
        redFlag = "Symptom {0} has no red flag".format(selectedSymptom["Name"])
            
        if selectedSymptom["HasRedFlag"]:
            redFlag = self._diagnosisClient.loadRedFlag(selectedSymptom["ID"])
            self._writeRawOutput("loadRedFlag", google(redFlag,to_language='ko'))

        self._writeHeaderMessage(redFlag)


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

        proposedSymptomsIds = []
        for proposeSymptom in proposedSymptoms:
            proposedSymptomsIds.append(proposeSymptom["ID"])
            
        self._writeHeaderMessage("Proposed symptoms: {0}".format(",".join(str(x) for x in proposedSymptomsIds)))


diagnosisClientDemo = PriaidDiagnosisClientDemo()
diagnosisClientDemo.simulate()
