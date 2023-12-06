import logging
logging.basicConfig(level=logging.INFO)
from sonarcloudx1.abstract import AbstractSonar

# Represents a software Project
class Rule(AbstractSonar):
    
    def __init__(self,personal_access_token, organization):
        super(Rule,self).__init__(personal_access_token=personal_access_token,organization=organization)
    
    def get(self, organization, rule_key):
        
        
        try:
            
            return  self.sonar.rules.search_rules(organization=organization,rule_key=rule_key)
        
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__) 