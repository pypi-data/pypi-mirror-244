from typing import TYPE_CHECKING
from openai.types.chat.completion_create_params import CompletionCreateParamsBase
from nomos.resources.logger import NomosLogger
from nomos.resources.messages.azure_openai import AzureOpenaiMessage, AzureOpenaiParams

from nomos.resources.messages.openai import OpenaiMessage

# Avoids circular import issues with typing
if TYPE_CHECKING:
    from ..client import Nomos


class Message:
    def __init__(self, client: "Nomos"):
        self.client = client

    def openai(self, parameters: CompletionCreateParamsBase) -> OpenaiMessage:
        return OpenaiMessage(
            parameters=parameters,
            nomos_logger=NomosLogger(nomos_api=self.client.nomos_api),
        )

    def azure_openai(self, parameters: AzureOpenaiParams) -> AzureOpenaiMessage:
        return AzureOpenaiMessage(
            parameters=parameters,
            nomos_logger=NomosLogger(nomos_api=self.client.nomos_api),
        )
