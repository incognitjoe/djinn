from collections import Counter, OrderedDict
from itertools import groupby
from abc import ABCMeta, abstractmethod


class AnalysisService(object):
    def get_failures_heatmap_data(self, analysis_strategy, failures):
        """
        Get the heatmap data for all failures.
        :return: a dictionary of the data for the x, y and z axes of a heatmap.
        """
        data = [AnalysisData(x.stage_failed, x.project, x.repository) for x in failures]
        return analysis_strategy.transform_for_heatmap(data)


class AnalysisData(object):
    """
    Immutable data object for passing about analysis data.
    """

    def __init__(self, stage, project, repo):
        self._stage = stage
        self._project = project
        self._repo = repo

    @property
    def stage(self):
        return self._stage

    @property
    def project(self):
        return self._project

    @property
    def repo(self):
        return self._repo


class Analysis(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def transform_for_heatmap(self, data):
        pass

    def _dedup(self, data):
        """
        Turn flat list of AnalysisData objects into a nested structure. This
        process deduplicates keys and makes relationships from stages to projects
        easier to reason about.
        :param data: the data to be transformed.
        :return: the transformed data.
        """
        deduped = {}
        data.sort(key=lambda x: x.stage)
        for stage_name, stage_data in groupby(data, lambda x: x.stage):
            item = {}
            for project, project_data in groupby(stage_data, lambda x: x.project):
                failures = sum(Counter(map(lambda x: x.repo, project_data)).values())
                item[project] = failures

            deduped[stage_name] = item
        return deduped


class ProjectStageAnalysis(Analysis):

    def transform_for_heatmap(self, data):
        """
        Transform data into the format for a plotly heatmap.
        :param data: a list of AnalysisData objects.
        :return: a dictionary of the x, y and z axes.
        """
        x = []
        y = OrderedDict()
        z = []
        deduped = self._dedup(data)
        for stage, details in deduped.items():
            x.append(stage)
            for project in details.keys():
                y[project] = True
        for project in y.keys():
            z_next = []
            for stage in x:
                failures = deduped.get(stage).get(project, 0)
                z_next.append(failures)
            z.append(z_next)
        return {"x": x, "y": y.keys(), "z": z}
