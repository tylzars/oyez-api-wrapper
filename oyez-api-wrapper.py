import requests
import json
import re
from six import string_types

class court_case:
    # Get court case and JSON data
    def __init__(self, term, docket):
        if not term and not docket:
            raise ValueError("Term/Docket# must be provided. Term/Docket# can be obtained by Oyez case file.")

        if (term and not isinstance(term, string_types)) and (docket and not isinstance(docket, string_types)):
            raise TypeError("Term/Docket# parameter must be a string value")

        self.term = term
        self.docket = docket
        
        try: 
            response = requests.get(f"https://api.oyez.org/cases/{self.term}/{self.docket}")
            self.json_data = response.json()
        except:
            raise exception("Weblink incorrect or inacessable!")
        
    # Get all judges that were on the case
    def get_case_judges(self):
        return_list = []
        number_of_judges = len(self.json_data["decisions"][0]["votes"])
        
        for person in range(number_of_judges):
            half = self.json_data["decisions"][0]["votes"][person]["member"]["name"]
            return_list.append(half)
        
        return return_list
    
    # Case facts with or without out HTML tags included
    def get_case_facts(self, html = False):
        if html:
            return_list = self.json_data["facts_of_the_case"]
        elif not self.json_data["facts_of_the_case"]: 
            return_list = "Facts of the case not present!"
        else:
            return_list = re.sub('<[^<]+?>', '', self.json_data["facts_of_the_case"])
        
        return return_list
    
    # Saves the JSON to the current directory (pretty-printed)
    def download_court_json(self, file_location):
        local_json_file = open(f"oyez_{self.term}_{self.docket}.json", 'w')
        
        local_json_file.write(json.dumps(self.json_data, indent=4))
        
        local_json_file.close()
    
    # Return dictionary of judges and their decision
    def get_judge_decisions(self):
        return_list = {}
        number_of_judges = len(self.json_data["decisions"][0]["votes"])
        
        for person in range(number_of_judges):
            name = self.json_data["decisions"][0]["votes"][person]["member"]["name"]
            vote = self.json_data["decisions"][0]["votes"][person]["vote"]
            return_list.update({name: vote})
        return return_list
    
    # Get the final ruling of a case
    def get_ruling(self):
        majority_vote = self.json_data["decisions"][0]["majority_vote"]
        minority_vote = self.json_data["decisions"][0]["minority_vote"]
        winning_party = self.json_data["decisions"][0]["winning_party"]
        decision_type = self.json_data["decisions"][0]["decision_type"]
        ruling_href = self.json_data["decisions"][0]["href"]
        
        return (majority_vote, minority_vote, winning_party, decision_type, ruling_href)
    
    # Get basic information about case and parties
    def get_basic_info(self):
        case_name = self.json_data["name"]
        first_party = self.json_data["first_party"]
        second_party = self.json_data["second_party"]
        
        return (case_name, first_party, second_party)
    
    # Get legal question
    def get_legal_question(self, html = False):
        if html:
            question = self.json_data["question"]
        elif not self.json_data["question"]:
            question = "Legal Question Not Present"
        else: 
            question = re.sub('<[^<]+?>', '', self.json_data["question"])
        
        return question
    
    # Get legal question
    def get_conclusion(self, html = False):
        if html:
            court_conclusion = self.json_data["conclusion"]
        elif not self.json_data["conclusion"]:
            court_conclusion = "Conclusion Not Present"
        else: 
            court_conclusion = re.sub('<[^<]+?>', '', self.json_data["conclusion"])
        
        return court_conclusion
    
    # Return the lower court
    def get_lower_court(self):
        lower_court = self.json_data["lower_court"]["name"]
        
        if not self.json_data["lower_court"]["name"]:
            lower_court = "Lower Court Not Present"
        
        return lower_court
    
    # Return title and links to audio pieces provided
    def get_audio_links(self):
        if not self.json_data["oral_argument_audio"]:
            audio_links = "Oral Arguements Not Present!"
        else:
            len_audio_links = len(self.json_data["oral_argument_audio"])
            audio_links = {}
            
            for item in range(len_audio_links):
                link = self.json_data["oral_argument_audio"][item]["href"]
                title = self.json_data["oral_argument_audio"][item]["title"]
                audio_links.update({title: link})
        
        return audio_links
