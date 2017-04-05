from unittest import TestCase

from mock import Mock, MagicMock

from djinn.analysis import Analysis, AnalysisService, AnalysisData
from djinn.database.entity import PipelineRun


class Matcher(object):
    def __init__(self, some_obj):
        self.some_obj = some_obj

    def __eq__(self, other):
        return self.some_obj.compare(other)


class TestAnalysisService(TestCase):
    def test_get_failures_heatmap_data(self):
        # Arrange
        data = [PipelineRun()]
        mock_analysis = Mock()
        mock_pipeline_results = Mock()
        mock_pipeline_results.get_all_failures = MagicMock(return_value=data)
        service = AnalysisService(mock_analysis, mock_pipeline_results)

        # Act
        service.get_failures_heatmap_data()

        # Assert
        mock_analysis.transform_for_heatmap.assert_called_once()


class TestAnalysis(TestCase):
    def setUp(self):
        self.analysis = Analysis()

    def test_transform_for_heatmap(self):
        data = [AnalysisData("run tests", "CommunityParser", "something"),
                AnalysisData("run tests", "CommunityParser", "something"),
                AnalysisData("remove previous version and re-verify cit", "CommunityParser", "something-else"),
                AnalysisData("remove previous version and re-verify cit", "CommunityParser", "something-else"),
                AnalysisData("remove previous version and re-verify cit", "GSTP", "something-else")]
        expected_heatmap_data = {"z": [[2, 2], [0, 1]],
                                 "y": ["CommunityParser", "GSTP"],
                                 "x": ["run tests", "remove previous version and re-verify cit"]}

        self.assertEquals(self.analysis.transform_for_heatmap(data), expected_heatmap_data)
