from google.cloud import dialogflowcx as cx
from google.protobuf.json_format import ParseDict
from google.protobuf.json_format import MessageToDict

# 2023-12-01
# - Dialogflow CX WebhookRequest object has changed with breaking changes
# - addition of "query" helper method to work through incoming payloads created.

# 2023-10-28
# - Replacement of self.request with self.__message to represent the proto message
# - Addition of __getattr__ which fetches from the self.__message now

class WebhookRequest:
    
    def __init__(self, body: dict):
        self.__message = cx.WebhookRequest()
        # When a webhook comes in as JSON, we use ParseDict to convert JSON to Protobuf
        ParseDict(body, self.__message._pb, ignore_unknown_fields=True)
        self.__origin = None
    
    def __getattr__(self, name: str):
        # Looks up attributes from the request proto message
        return getattr(self.__message, name)

    # Helper properties.  These class properties make basic access easier
    @property
    def tag(self):
        return self.__message.fulfillment_info.tag

    @property
    def session(self):
        return self.__message.session_info.session

    @property
    def session_id(self):
        return self.session.split('/')[-1]

    @property
    def session_parameters(self):
        return MessageToDict(
            self.__message.session_info._pb, 
            including_default_value_fields=True
        ).get('parameters')
        
    @property
    def query(self):
        r = self.__message
        
        # q is for query, o is for origin
        q, o = '', ''
        if r.text:
            q = r.text
            o = 'text'
        elif r.trigger_event:
            q = r.trigger_intent
            o = 'trigger_intent'
        elif r.transcript:
            q = r.transcript
            o = 'transcript'
        elif r.trigger_event:
            q = r.trigger_event
            o = 'trigger_event'
        elif r.dtmf_digits:
            q = r.dtmf_digits
            o = 'dtmf_digits'
        else:
            ...
        
        self.__origin = o
        return q
    
    @property
    def origin(self):
        return self.__origin

    # JSON Encoding methods.  These are primarily for testing and logging.
    def to_dict(self):
        return MessageToDict(self.__message._pb, including_default_value_fields=True)

    @property
    def as_dict(self):
        return self.to_dict()
