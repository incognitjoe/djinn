from unittest import TestCase

from djinn.analysis import AnalysisService, AnalysisData, projects_stage_inner_groupby, \
    repos_stage_inner_groupby


class TestAnalysisService(TestCase):
    def test_transform_for_projects_heatmap(self):
        service = AnalysisService()
        data = [MockPipelineRun("run tests", "TestProject", "something"),
                MockPipelineRun("run tests", "TestProject", "something"),
                MockPipelineRun("re-verify env", "TestProject", "something-else"),
                MockPipelineRun("re-verify env", "TestProject", "something-else"),
                MockPipelineRun("re-verify env", "AnotherProject", "something-else")]
        expected_heatmap_data = {"z": [[2, 2], [0, 1]],
                                 "y": ["TestProject", "AnotherProject"],
                                 "x": ["run tests", "re-verify env"]}
        self.assertEquals(service.get_failures_heatmap_data(projects_stage_inner_groupby, data), expected_heatmap_data)

    def test_transform_for_repos_heatmap(self):
        service = AnalysisService()
        data = [MockPipelineRun("run tests", "TestProject", "something"),
                MockPipelineRun("run tests", "TestProject", "something"),
                MockPipelineRun("re-verify env", "TestProject", "something-else"),
                MockPipelineRun("re-verify env", "TestProject", "something-else"),
                MockPipelineRun("re-verify env", "AnotherProject", "something-else")]
        expected_heatmap_data = {"z": [[2, 0], [0, 3]],
                                 "y": ["something", "something-else"],
                                 "x": ["run tests", "re-verify env"]}
        self.assertEquals(service.get_failures_heatmap_data(repos_stage_inner_groupby, data), expected_heatmap_data)


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
