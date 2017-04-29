from uuid import uuid4

from hypothesis import given, settings
from hypothesis.strategies import lists, integers, text, characters
from unittest import TestCase

from djinn.analysis import gen_heatmap_with_strategy, projects_stage_inner_groupby

""" Generate random upper case letter strings. """
strings = text(characters(min_codepoint=66, max_codepoint=90)).map(lambda s: s.strip()).filter(
    lambda s: len(s) > 0)

""" Generate a list of lists of equal sizes. """
rectangle_lists = integers(min_value=5, max_value=10).flatmap(
    lambda n: lists(lists(integers(min_value=5, max_value=10), min_size=n, max_size=n)))


def gen_data_from_z(z):
    data = []
    y_len = len(z)
    x_len = 0 if y_len == 0 else len(z[0])
    projects = [uuid4() for _ in range(y_len)]
    stages = [uuid4() for _ in range(x_len)]
    for pidx, project in enumerate(projects):
        for sidx, stage in enumerate(stages):
            failures = z[pidx][sidx]
            repo = strings.example()
            for _ in range(failures):
                data.append(MockPipelineRun(stage_failed=stage, project=project, repository=repo))
    return data, z, stages, projects


class TestAnalysisService(TestCase):
    @given(rectangle_lists)
    @settings(max_examples=100)
    def test_transform(self, given_z):
        """
        Given a known value for z, generate the data that would give this z,
        transform the data and check that the z value from the transformed data 
        matches the given z value.
        :param given_z: the generated z value.       
        """
        data, z, x, y = gen_data_from_z(given_z)
        actual = gen_heatmap_with_strategy(projects_stage_inner_groupby, data)
        self.assertEquals(sort_nested(given_z), sort_nested(actual['z']))


class MockPipelineRun:
    def __init__(self, stage_failed, project, repository):
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


def sort_nested(list_of_lists):
    """
    Sort lists of lists.
    :param list_of_lists: a list of lists.
    :return: a sorted list of lists, where the nested lists 
        are also sorted.
    """
    return sorted(map(lambda item: sorted(item), list_of_lists))
