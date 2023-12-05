"imports"
from enum import Enum
from message_local.Message import Message
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger
# from api_management_local.api_call import APICallsLocal
# from api_management_local.api_limit import APILimitsLocal


WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_ID = 173
WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_NAME = 'send whatsapp-message-local-python-package'

whatsapp_message_local_python_unit_tests_logger_object = {
    'component_id': WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": "jenya.b@circ.zone"
}
logger = Logger.create_logger(
    object=whatsapp_message_local_python_unit_tests_logger_object)


class Importance(Enum):
    "enum class"
    LOW = 10
    MEDIUM = 20
    HIGH = 30


class WhatsAppMessage(Message):
    "Whatsapp message"
    def __init__(self, body: str, importance: Importance, subject: str = None) -> None:
        super().__init__(body, importance, subject)

    def send(self, recipient: list) -> list:
        logger.start()
        data = {
            "to": recipient,
            "message_type": "text",
            "text": self.body,
            "channel": "whatsapp"
        }
        logger.info("Message sent to " + recipient)
        logger.end()

    def was_read(self) -> bool:
        pass

    def display(self):
        "display message"
        logger.start()
        logger.info(self.body)
        logger.end()

    def _can_send(self) -> bool:
        logger.start()
       # APICallsLocal()._insert_api_call_dict
        logger.end()

    def _after_send_attempt(self) -> None:
        logger.start()
       # APILimitsLocal().get_api_limit_by_api_type_id_external_user_id
        logger.end()
