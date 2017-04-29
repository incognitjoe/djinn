from hypothesis import given, settings
from hypothesis.strategies import composite, lists, integers, text, characters
from unittest import TestCase

from djinn.analysis import gen_heatmap_with_strategy, projects_stage_inner_groupby

""" Generate random upper case letter strings. """
strings = text(characters(min_codepoint=66, max_codepoint=90)).map(lambda s: s.strip()).filter(lambda s: len(s) > 0)

""" Generate a list of lists of equal sizes. """
rectangle_lists = integers(min_value=5, max_value=100).flatmap(
    lambda n: lists(lists(integers(min_value=5, max_value=100), min_size=n, max_size=n)))


@composite
def mock_pipeline_runs(draw):
    """
    Generate a MockPipelineRun
    :param draw: method to draw an instance of a generator. 
    :return: a MockPipelineRun
    """
    stage = draw(strings)
    project = draw(strings)
    repo = draw(strings)
    return MockPipelineRun(stage_failed=stage, project=project, repository=repo)


def gen_data_from_z(z):
    data = []
    y_len = len(z)
    x_len = 0 if y_len == 0 else len(z[0])
    projects = [strings.example() for _ in range(y_len)]
    stages = [strings.example() for _ in range(x_len)]
    for pidx, project in enumerate(projects):
        for sidx, stage in enumerate(stages):
            failures = z[pidx][sidx]
            repo = strings.example()
            for _ in range(failures):
                data.append(MockPipelineRun(stage_failed=stage, project=project, repository=repo))
    return data, z


class TestAnalysisService(TestCase):
    @given(rectangle_lists)
    @settings(max_examples=100)
    def test_transform(self, l):
        data, expected = gen_data_from_z(l)
        actual = gen_heatmap_with_strategy(projects_stage_inner_groupby, data)
        self.assertEquals(sort_nested(l), sort_nested(actual['z']))


class MockPipelineRun(dict):
    def __init__(self, stage_failed, project, repository):
        dict.__init__(self, stage_failed=stage_failed, project=project, repository=repository)
        self._stage_failed = stage_failed
        self._project = project
        self._repository = repository

    @property
    def stage_failed(self):
        return self._stage_failed

    @property
    def project(self):
        return self._project

    @property
    def repository(self):
        return self._repository

    def __str__(self):
        return str(self.stage_failed) + " " + str(self.project)


def sort_nested(list_of_lists):
    """
    Sort lists of lists.
    :param list_of_lists: a list of lists.
    :return: a sorted list of lists, where the nested lists 
        are also sorted.
    """
    return sorted(map(lambda item: sorted(item), list_of_lists))
