from uuid import uuid4

from hypothesis import given, settings
from hypothesis.strategies import lists, integers, text, characters
from unittest import TestCase

from djinn.analysis import gen_heatmap_with_strategy, projects_stage_inner_groupby

""" Generate random upper case letter strings. """
strings = text(characters(min_codepoint=66, max_codepoint=90)).map(lambda s: s.strip()).filter(
    lambda s: len(s) > 0)

""" Generate a list of lists of equal sizes. """
rectangle_lists = integers(min_value=2, max_value=50).flatmap(
    lambda n: lists(lists(integers(min_value=2, max_value=30), min_size=n, max_size=n)))


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
    def test_transform_grouping_by_projects(self, given_z):
        """
        Given a known value for z, generate the data that would give this z,
        transform the data and check that the z value from the transformed data 
        matches the given z value.
        :param given_z: the generated z value.       
        """
        data, expected_z, expected_x, expected_y = gen_data_from_z(given_z)
        actual = gen_heatmap_with_strategy(projects_stage_inner_groupby, data)
        expected_failures = build_failure_map(expected_x, expected_y, expected_z)
        actual_failures = build_failure_map(actual['x'], actual['y'], actual['z'])
        self.assertEqual(expected_failures, actual_failures)


def build_failure_map(x, y, z):
    """
    Build a dict mapping the key "projects + stages" to the number 
    of failures.
    :param x: 
    :param y: 
    :param z: 
    :return: the failures map.
    """
    failure_lookup = dict()
    for y_index, x_list in enumerate(z):
        for x_index, failures in enumerate(x_list):
            project = y[y_index]
            stage = x[x_index]
            failure_lookup[str(project) + str(stage)] = failures

    return failure_lookup


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
