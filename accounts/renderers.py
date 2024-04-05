from rest_framework import renderers
import json

class UserRenderer(renderers.JSONOpenAPIRenderer):
    charset='utf-8'
    def render(self, data, media_type=None, renderer_context=None):
        response=''
        if 'ErrorDetail' in str(data):
            response=json.dumps({'errors':data})
        else:
            response=json.dumps(data)    
        return super().render(response, media_type='application/json', renderer_context=renderer_context)