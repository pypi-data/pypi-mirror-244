"imports"
import os
import vonage
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger
from api_management_local.api_management_local import APIManagmentLocal
from src.whatsappmessage import WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_ID
from src.whatsappmessage import WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_NAME
from dotenv import load_dotenv

whatsapp_message_local_python_unit_tests_logger_object = {
    'component_id': WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": "jenya.b@circ.zone"
}

logger = Logger.create_logger(
    object=whatsapp_message_local_python_unit_tests_logger_object)
WHATSAPP_MESSAGE_VONAGE_API_TYPE_ID = 9
load_dotenv()


class VonageWhatsAppMessagesLocal(vonage.Messages):
    "Vonage whatsapp message"
    def __init__(self, default_from_number: str, to_number: str) -> None:
        self.api_key = os.getenv("VONAGE_API_KEY")
        self.api_secret = os.getenv("VONAGE_API_SECRET")
        self.default_from_number = default_from_number
        self.to_number = to_number
        self.url = "https://messages-sandbox.nexmo.com/v1/messages"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def send(self, person_id: int, message: str) -> None:
        "send message use vonage api"
        logger.start("send message to phone by id ", object={
                     "profile_id": person_id, 'message': message})
        data = {
            "from": self.default_from_number,
            "to": self.to_number,
            "message_type": "text",
            "text": message,
            "channel": "whatsapp"
        }
        APIManagmentLocal()
        logger.end()
