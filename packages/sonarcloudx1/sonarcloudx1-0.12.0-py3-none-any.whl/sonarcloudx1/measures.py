import logging
logging.basicConfig(level=logging.INFO)
from sonarcloudx1.abstract import AbstractSonar

class Measure(AbstractSonar):
    def __init__(self,personal_access_token, organization):
        super(Measure,self).__init__(personal_access_token=personal_access_token, organization=organization)
    
    def get_by_component_function(self, component_id,**kwargs):
        results = []
        function = kwargs["function"]
        try:
            #search_measures_history
            results = self.sonar.measures.get_component_with_specified_measures(component=component_id,
                                                                                fields="metrics,periods",
                                                                                  metricKeys="lines,ncloc,complexity,code_smells,bugs,vulnerabilities,duplicated_lines_density,violations")

            function (data=results, topic=kwargs["topic"], extra_data=kwargs["extra_data"])

        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__) 
    
    def get_by_project_function(self, project_id,**kwargs):
        results = []
        function = kwargs["function"]
        try:
            
            results = self.sonar.measures.get_component_with_specified_measures(component=project_id,
                                                                                fields="metrics,periods",
                                                    
                                                                                  metricKeys="lines,ncloc,complexity,code_smells,bugs,vulnerabilities,duplicated_lines_density,violations")

            function (data=results, topic=kwargs["topic"], extra_data=kwargs["extra_data"])

        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__) 
