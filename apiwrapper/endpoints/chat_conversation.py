from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.user import User


class ChatConversation(Endpoint):

    __endpoint_chat_conversation = "chat-conversation"
    __endpoint_chat_conversation_message = "message"
    __endpoint_chat_conversation_attachment = "attachment"
    __endpoint_chat_conversation_attachment_content = "content"

    @classmethod
    def _get_base_endpoint(cls, user_id, chat_id=None):
        endpoint = User._get_base_endpoint(user_id)
        endpoint += "/%s" % cls.__endpoint_chat_conversation
        if chat_id is not None:
            endpoint += "/%d" % chat_id
        return endpoint

    # Chat Conversation Logic
    def get_all_chat_conversations_for_user(self, user_id):
        endpoint = self._get_base_endpoint(user_id)

        return self._make_get_request(endpoint)

    def get_chat_conversation_by_id(self, user_id, chat_id):
        endpoint = self._get_base_endpoint(user_id, chat_id)

        return self._make_get_request(endpoint)

    # Message Logic
    def get_all_messages_for_chat_conversation(self, user_id, chat_id):
        endpoint = self._get_base_endpoint(user_id, chat_id)
        endpoint += "/%s" % (
            self.__endpoint_chat_conversation_message
        )

        return self._make_get_request(endpoint)

    # Attachment Logic
    def get_chat_attachment_by_id(self, user_id, chat_id, attachment_id):
        endpoint = self._get_base_endpoint(user_id, chat_id)
        endpoint += "/%s/%d" % (
            self.__endpoint_chat_conversation_attachment,
            attachment_id
        )

        return self._make_get_request(endpoint)

    def get_content_of_chat_attachment(self, user_id, chat_id, attachment_id):
        endpoint = self._get_base_endpoint(user_id, chat_id)
        endpoint += "/%s/%d/%s" % (
            self.__endpoint_chat_conversation_attachment,
            attachment_id,
            self.__endpoint_chat_conversation_attachment_content
        )

        return self._make_get_request(endpoint)
