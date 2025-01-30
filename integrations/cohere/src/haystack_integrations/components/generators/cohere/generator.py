# SPDX-FileCopyrightText: 2023-present deepset GmbH <info@deepset.ai>
#
# SPDX-License-Identifier: Apache-2.0
import logging
from typing import Any, Callable, Dict, List, Optional

from haystack import component
from haystack.dataclasses import ChatMessage
from haystack.utils import Secret

from .chat.chat_generator import CohereChatGenerator

logger = logging.getLogger(__name__)


@component
class CohereGenerator(CohereChatGenerator):
    """Generates text using Cohere's models through Cohere's `generate` endpoint.

    NOTE: Cohere discontinued the `generate` API, so this generator is a mere wrapper
    around `CohereChatGenerator` provided for backward compatibility.

    ### Usage example

    ```python
    from haystack_integrations.components.generators.cohere import CohereGenerator

    generator = CohereGenerator(api_key="test-api-key")
    generator.run(prompt="What's the capital of France?")
    ```
    """

    def __init__(
        self,
        api_key: Secret = Secret.from_env_var(["COHERE_API_KEY", "CO_API_KEY"]),
        model: str = "command-r",
        streaming_callback: Optional[Callable] = None,
        api_base_url: Optional[str] = None,
        **kwargs,
    ):
        """
        Instantiates a `CohereGenerator` component.

        :param api_key: Cohere API key.
        :param model: Cohere model to use for generation.
        :param streaming_callback: Callback function that is called when a new token is received from the stream.
            The callback function accepts [StreamingChunk](https://docs.haystack.deepset.ai/docs/data-classes#streamingchunk)
            as an argument.
        :param api_base_url: Cohere base URL.
        :param **kwargs: Additional arguments passed to the model. These arguments are specific to the model.
            You can check them in model's documentation.
        """

        # Note we have to call super() like this because of the way components are dynamically built with the decorator
        super(CohereGenerator, self).__init__(api_key, model, streaming_callback, api_base_url, None, **kwargs)  # noqa

    @component.output_types(replies=List[str], meta=List[Dict[str, Any]])
    def run(self, prompt: str):
        """
        Queries the LLM with the prompts to produce replies.

        :param prompt: the prompt to be sent to the generative model.
        :returns: A dictionary with the following keys:
            - `replies`: A list of replies generated by the model.
            - `meta`: Information about the request.
        """
        chat_message = ChatMessage.from_user(prompt)
        # Note we have to call super() like this because of the way components are dynamically built with the decorator
        results = super(CohereGenerator, self).run([chat_message])  # noqa
        return {"replies": [results["replies"][0].text], "meta": [results["replies"][0].meta]}
