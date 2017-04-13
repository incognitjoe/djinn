import json

import falcon


class HeatmapResource(object):
    def __init__(self, analysis_service):
        self.service = analysis_service

    def on_get(self, req, resp, project=None):
        if project is None:
            resp.body = json.dumps(self.service.get_failures_heatmap_data())
            resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps({'Error': 'Not implemented yet.'})
            resp.status = falcon.HTTP_501
