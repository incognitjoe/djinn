from mock import Mock, MagicMock
from unittest import TestCase

from djinn.analysis import AnalysisService, AnalysisData, transform_for_heatmap, projects_stage_inner_groupby, \
    repos_stage_inner_groupby
from djinn.database.entity import PipelineRun


class TestAnalysisService(TestCase):
    def test_get_failures_heatmap_data(self):
        # Arrange
        data = [PipelineRun()]
        mock_analysis = Mock()
        mock_pipeline_results = MagicMock(return_value=data)
        service = AnalysisService()

        # Act
        service.get_failures_heatmap_data(mock_analysis, mock_pipeline_results)

        # Assert
        mock_analysis.assert_called_once()


class TestAnalysis(TestCase):
    def test_transform_for_projects_heatmap(self):
        data = [AnalysisData("run tests", "TestProject", "something"),
                AnalysisData("run tests", "TestProject", "something"),
                AnalysisData("re-verify env", "TestProject", "something-else"),
                AnalysisData("re-verify env", "TestProject", "something-else"),
                AnalysisData("re-verify env", "AnotherProject", "something-else")]
        expected_heatmap_data = {"z": [[2, 2], [0, 1]],
                                 "y": ["TestProject", "AnotherProject"],
                                 "x": ["run tests", "re-verify env"]}

        self.assertEquals(transform_for_heatmap(projects_stage_inner_groupby)(data), expected_heatmap_data)

    def test_transform_for_repos_heatmap(self):
        data = [AnalysisData("run tests", "TestProject", "something"),
                AnalysisData("run tests", "TestProject", "something"),
                AnalysisData("re-verify env", "TestProject", "something-else"),
                AnalysisData("re-verify env", "TestProject", "something-else"),
                AnalysisData("re-verify env", "AnotherProject", "something-else")]
        expected_heatmap_data = {"z": [[2, 0], [0, 3]],
                                 "y": ["something", "something-else"],
                                 "x": ["run tests", "re-verify env"]}
        self.assertEquals(transform_for_heatmap(repos_stage_inner_groupby)(data), expected_heatmap_data)
