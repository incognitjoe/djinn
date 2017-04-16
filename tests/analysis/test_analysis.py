from unittest import TestCase

from mock import Mock, MagicMock

from djinn.analysis import Analysis, AnalysisService, AnalysisData, ProjectStageAnalysis
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
        mock_analysis.transform_for_heatmap.assert_called_once()


class TestAnalysis(TestCase):
    def setUp(self):
        self.analysis = ProjectStageAnalysis()

    def test_transform_for_heatmap(self):
        data = [AnalysisData("run tests", "TestProject", "something"),
                AnalysisData("run tests", "TestProject", "something"),
                AnalysisData("re-verify env", "TestProject", "something-else"),
                AnalysisData("re-verify env", "TestProject", "something-else"),
                AnalysisData("re-verify env", "AnotherProject", "something-else")]
        expected_heatmap_data = {"z": [[2, 2], [0, 1]],
                                 "y": ["TestProject", "AnotherProject"],
                                 "x": ["run tests", "re-verify env"]}

        self.assertEquals(self.analysis.transform_for_heatmap(data), expected_heatmap_data)
