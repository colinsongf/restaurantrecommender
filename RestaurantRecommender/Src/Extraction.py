'''
Created on Apr 24, 2013

@author: Kathy
'''
import sys, traceback, ast, json

class Extraction:
    #Constructor
    def __init__(self, userFile, busFile):
        self.users = dict()  #stores the information on the users
        self.businesses = dict()  #stores the information on the businesses
        self.fileoffset = 0  #used for retrieving the reviews from the dataset
        self.userFilename = userFile  #stores the filename for the file containing the user info
        self.busFilename = busFile  #stores the filename for the file containing the business info
    
    #Extract the necessary information on the users and restaurants
    def extractInfo(self):
        f = open('tmpNFvucr', 'r')
    
        #read each line in the file to retrieve the necessary info
        for lcurr in f:        
            line = json.loads(lcurr)  #convert the string into a dictionary object
            
            if line['type'] == "user":
                #add the user to the list if they are not already in it
                if line['user_id'] not in self.users:
                    self.users.update({line['user_id']: dict()})
                    self.users[line['user_id']].update({'name': line['name'], 'reviews': [], 'businesses': []})      
            #if the entry is about a user's review
            if line['type'] == "review":
                #add each restaurant the user has visited to that user's list    
                if line['business_id'] not in self.users[line['user_id']]['businesses']:
                    self.users[line['user_id']]['businesses'].append('business_id')
                if line['review_id'] not in self.users[line['user_id']]['reviews']:
                    self.users[line['user_id']]['reviews'].append('review_id')
            #if the entry is about a restaurant
            elif line['type'] == "business":
                #add every unique business along with some information on them
                if line['business_id'] not in self.businesses:
                    self.businesses.update({line['business_id']: dict()})
                    self.businesses[line['business_id']].update({'name': line['name'], 'state': line['state'], 'city': line['city'], 'categories': line['categories'] })      
        f.close()

        #Store the dictionaries as json objects
        with open(self.userFilename, 'w') as outfile:
            json.dump(self.users, outfile)
        with open(self.busFilename, 'w') as outfile:
            json.dump(self.businesses, outfile)      

    #Obtain the next review entry from the dataset
    def nextReview(self):
        f = open('tmpNFvucr', 'r')
        
        #skip to the middle of the file according to the offset and obtain the entry
        f.seek(self.fileoffset)
        tline = f.readline().strip()
        while tline == "":
            tline = f.readline().strip() 
        currLine = json.loads(tline)  #convert the string into a dictionary object
        
        #ignore all the entries about just the users
        while currLine['type'] == "user":
            currLine = ast.literal_eval(f.readline())
        
        #return an empty dictionary if there are no more reviews in the dataset
        if currLine['type'] == "business":
            currLine = {}
            self.fileoffset = 0  #reset the offset into the file back to the beginning
        #otherwise adjust the offset into the file for the next read  
        else:
            self.fileoffset = f.tell() - 1
        
        f.close()
        return currLine
