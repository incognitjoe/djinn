from collections import Counter, OrderedDict
from itertools import groupby


class AnalysisService(object):
    def get_failures_heatmap_data(self, analysis_strategy, failures):
        """
        Get the heatmap data for all failures.
        :param analysis_strategy: a function which takes data and groups by a
         key in that data.
        :return: a dictionary of the data for the x, y and z axes of a heatmap.
        """
        data = [AnalysisData(x.stage_failed, x.project, x.repository) for x in failures]
        return _transform_for_heatmap(analysis_strategy)(data)


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


def projects_stage_inner_groupby(stage_data):
    """
    Strategy for transforming raw data into heatmap data mapping projects
    against stages.
    """
    return groupby(stage_data, lambda item: item.project)


def repos_stage_inner_groupby(stage_data):
    """
    Strategy for transforming raw data into heatmap data mapping projects
    against stages.
    """
    return groupby(stage_data, lambda item: item.repo)


def _transform_for_heatmap(inner_groupby):
    """
    Transform data into the format for a plotly heatmap.
    :param data: a list of AnalysisData objects.
    :return: a dictionary of the x, y and z axes.
    """

    def f(data):
        x = []
        y = OrderedDict()
        z = []
        deduped = _dedup(data, inner_groupby)
        for stage, details in deduped.items():
            x.append(stage)
            for inner in details.keys():
                y[inner] = True
        for inner in y.keys():
            z_next = []
            for stage in x:
                failures = deduped.get(stage).get(inner, 0)
                z_next.append(failures)
            z.append(z_next)
        return {"x": x, "y": y.keys(), "z": z}

    return f


def _dedup(data, inner_groupby):
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
        for inner_data_key, inner_data in inner_groupby(stage_data):
            failures = sum(Counter(map(lambda x: x.repo, inner_data)).values())
            item[inner_data_key] = failures
        deduped[stage_name] = item
    return deduped
