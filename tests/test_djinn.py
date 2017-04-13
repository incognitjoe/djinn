import os

from falcon import testing

from djinn import DJinn


class TestDJinn(testing.TestCase):
    basefolder = os.path.dirname(os.path.realpath(__file__))
    successfulresult = {'status': u'SUCCESS', 'success': True, 'repository': 'jenkinsfile-test', 'run_id': u'7',
                        'timestamp': 1491143071036, 'project': 'TEST', 'id': 'jenkinsfile-test7'}
    failedresult = {'status': u'FAILED', 'error_type': u'hudson.AbortException', 'success': False,
                    'repository': 'jenkinsfile-test', 'run_id': u'6', 'timestamp': 1491143013685,
                    'error_message': u'Oops.', 'stage_failed': u'Setup', 'project': 'TEST', 'id': 'jenkinsfile-test6'}
    failedresult2 = {'status': u'FAILED', 'error_type': u'hudson.AbortException', 'success': False,
                     'repository': 'jenkinsfile-test', 'run_id': u'5', 'timestamp': 1491143013620,
                     'error_message': u'Oops.', 'stage_failed': u'Deploy', 'project': 'TEST', 'id': 'jenkinsfile-test5'}

    @classmethod
    def setUpClass(cls):
        cls.djinn = DJinn(jenkinsurl='http://admin:103b194e4c57eeda91333e6e51c4f40e@localhost:8080',
                          dburl='sqlite:///')
        cls.djinn.db.insert_result_batch([cls.successfulresult, cls.failedresult, cls.failedresult2])

    def setUp(self):
        super(TestDJinn, self).setUp()
        self.app = self.djinn.create_api()

    def test_heatmap(self):
        expected_heatmap = {u'x': [u'Setup', u'Deploy'], u'y': [u'TEST'], u'z': [[1, 1]]}
        result = self.simulate_get('/heatmap/')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json, expected_heatmap)

    def test_heatmap_for_project(self):
        result = self.simulate_get('/heatmap/TEST/')
        self.assertEqual(result.status_code, 501)
