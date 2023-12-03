from google.cloud import dialogflowcx as cx

from google.protobuf.json_format import MessageToDict

# 2023-12-01
# - Added comments and docstrings as necessary.

class WebhookResponse:
    
    def __init__(self):
        # Initialize a WebhookResponse object with no messages
        self.__message: cx.WebhookResponse = cx.WebhookResponse(
            fulfillment_response=self.FulfillmentResponse(messages=[])
        )

    def __getattr__(self, name: str):
        # Looks up attributes from the request proto message
        return getattr(self.__message, name)

    @property
    def FulfillmentResponse(self):
        return cx.WebhookResponse.FulfillmentResponse

    @property
    def ResponseMessage(self):
        return cx.ResponseMessage

    @property
    def Text(self):
        return cx.ResponseMessage.Text

    @property
    def ConversationSuccess(self):
        return cx.ResponseMessage.ConversationSuccess

    @property
    def OutputAudioText(self):
        return cx.ResponseMessage.OutputAudioText

    @property
    def LiveAgentHandoff(self):
        return cx.ResponseMessage.LiveAgentHandoff

    @property
    def EndInteraction(self):
        return cx.ResponseMessage.EndInteraction

    @property
    def PlayAudio(self):
        return cx.ResponseMessage.PlayAudio

    @property
    def MixedAudio(self):
        return cx.ResponseMessage.MixedAudio

    @property
    def TelephonyTransferCall(self):
        return cx.ResponseMessage.TelephonyTransferCall

    @property
    def fulfillment_response(self):
        return self.__message.fulfillment_response

    def add_response(self, response_message: cx.ResponseMessage):
        self.fulfillment_response.messages.append(response_message)
        return self

    def add_text_response(self, *texts, channel=""):
        text = self.Text(text=texts)
        response_message = self.ResponseMessage(text=text, channel=channel)
        self.add_response(response_message)
        return self
    
    def add_conversation_success(self, metadata: dict, channel=""):
        conversation_success = self.ConversationSuccess(metadata=metadata)
        response_message = self.ResponseMessage(conversation_success=conversation_success, channel=channel)
        self.add_response(response_message)
        return self        

    def add_payload_response(self, payload: dict, channel=""):
        # ResponseMessage instantiation with value of Payload handles this automatically
        # This is the "mapping" interface; no need for Struct and ParseDict
        response_message = self.ResponseMessage(payload=payload, channel=channel)
        self.add_response(response_message)
        return self

    def add_ssml_response(self, ssml: str, channel=""):
        output_audio_text = self.OutputAudioText(ssml=ssml)
        response_message = cx.ResponseMessage(output_audio_text=output_audio_text, channel=channel)
        self.add_response(response_message)
        return self
    
    def add_live_agent_handoff(self, metadata: dict, channel=""):
        live_agent_handoff = self.LiveAgentHandoff(metadata=metadata)
        response_message = cx.ResponseMessage(live_agent_handoff=live_agent_handoff, channel=channel)
        self.add_response(response_message)
        return self

    def add_telephony_transfer_call(self, phone_number: str, channel=""):
        telephony_transfer_call = self.TelephonyTransferCall(phone_number=phone_number)
        response_message = cx.ResponseMessage(telephony_transfer_call=telephony_transfer_call, channel=channel)
        self.add_response(response_message)
        return self

    def add_session_parameters(self, parameters: dict):
        session_info = cx.SessionInfo(parameters=parameters)
        self.__message.session_info = session_info
        return self    

    # JSON Encoding methods.  These are primarily for testing and logging.
    def to_dict(self):
        return MessageToDict(self.__message._pb, including_default_value_fields=True)
    
    @property
    def as_dict(self):
        return self.to_dict()

