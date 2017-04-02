from database import PipelineResults
from jenkins import DJenkins
from djinnutils.loggers import get_named_logger


class Djinn(object):
    def __init__(self, jenkinsurl=None, dburl=None):
        """
        Initialize connections to Jenkins and a persistence layer.
        :param jenkinsurl: URL containing basic auth used for queries, e.g. http://admin:apitoken@localhost
        :param dburl: database connection string, e.g. sqlite:///jenkinsdata.db
        """
        self.logger = get_named_logger('Djinn')
        self.dj = DJenkins(url=jenkinsurl, logger=self.logger)
        self.db = PipelineResults(connection_url=dburl, echo=False)

    def get_all_pipeline_results_and_save_to_db(self, pipelinebranch):
        """
        Fetch all repository pipeline data and write to database.
        :param pipelinebranch: branch name used for pipelines.
        :return: None
        """
        pipelines = self.dj.get_pipeline_history_for_all_repos(pipelinebranch=pipelinebranch)
        self.db.insert_result_batch(pipelines)
