import ssl
from dataclasses import asdict
import json
import time
import uuid
from datetime import datetime
from types import TracebackType
from typing import Any, Callable, cast, Union, Dict, Type, Optional
from urllib.parse import urlparse
from websockets.sync.client import connect as ws_connect, ClientConnection
from websockets.uri import parse_uri

from h2ogpte.types import (
    ChatAcknowledgement,
    ChatError,
    ChatMessage,
    ChatRequest,
    ChatResponse,
    PartialChatMessage,
    SessionError,
)


class Session:
    """Create and participate in a chat session.

    This is a live connection to the h2oGPTe server contained to a specific
    chat session on top of a single collection of documents. Users will find all
    questions and responses in this session in a single chat history in the
    UI.

    See Also:
        H2OGPTE.connect: To initialize a session on an existing connection.

    Args:
        address:
                Full URL of the h2oGPTe server to connect to.
        api_key:
                API key for authentication to the h2oGPTe server. Users can generate
                a key by accessing the UI and navigating to the Settings.
        chat_session_id:
                The ID of the chat session the queries should be sent to.

    Examples:

        .. code-block:: python

            # Example 1: Best practice, create a session using the H2OGPTE module
            with h2ogpte.connect(chat_session_id) as session:
                answer1 = session.query('How many paper clips were shipped to Scranton?', timeout=10)
                answer2 = session.query('Did David Brent co-sign the contract with Initech?', timeout=10)

            # Example 2: Connect and disconnect manually
            session = Session(
                address=address,
                api_key=api_key,
                chat_session_id=chat_session_id
            )
            session.connect()
            answer = session.query("Are there any dogs in the documents?")
            session.disconnect()
    """

    def __init__(
        self,
        address: str,
        api_key: str,
        chat_session_id: str,
        system_prompt: str = None,
        pre_prompt_query: str = None,
        prompt_query: str = None,
        rag_type: str = None,
        hyde_no_rag_llm_prompt_extension: str = None,
    ):
        url = urlparse(address)
        scheme = "wss" if url.scheme == "https" else "ws"
        # TODO handle base URLs
        self._address = f"{scheme}://{url.netloc}/ws"
        self._api_key = api_key
        self._chat_session_id = chat_session_id
        self._connection: Optional[ClientConnection] = None
        self.system_prompt = system_prompt
        self.pre_prompt_query = pre_prompt_query
        self.prompt_query = prompt_query
        self.rag_type = rag_type
        self.hyde_no_rag_llm_prompt_extension = hyde_no_rag_llm_prompt_extension

    @property
    def connection(self) -> ClientConnection:
        if not self._connection:
            raise RuntimeError("Session was not properly connect()ed")
        return self._connection

    def connect(self):
        """Connect to an h2oGPTe server.

        This is primarily an internal function used when users create a
        session using `with` from the H2OGPTE.connection() function.
        """
        wsuri = parse_uri(self._address)
        if wsuri.secure:
            context = ssl.SSLContext()
            context.verify_mode = ssl.CERT_NONE
        else:
            context = None
        self._connection = ws_connect(
            self._address,
            additional_headers={"Authorization": f"Bearer {self._api_key}"},
            ssl_context=context,
        )

    def query(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        pre_prompt_query: Optional[str] = None,
        prompt_query: Optional[str] = None,
        pre_prompt_summary: Optional[str] = None,
        prompt_summary: Optional[str] = None,
        llm: Union[str, int, None] = None,
        llm_args: Optional[Dict[str, Any]] = None,
        self_reflection_config: Optional[Dict[str, Any]] = None,
        rag_config: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        callback: Optional[
            Callable[[Union[ChatMessage, PartialChatMessage]], None]
        ] = None,
    ) -> Union[ChatMessage, None]:
        """Retrieval-augmented generation for a query on a collection.

        Finds a collection of chunks relevant to the query using similarity scores. Sends these and any
        additional instructions to an LLM.

        Format of questions or imperatives:

            .. code-block::

                "{pre_prompt_query}\"\"\"
                {similar_context_chunks}
                \"\"\"\\n{prompt_query}{message}"

        Args:
            message:
                Query or instruction from the end user to the LLM.
            system_prompt:
                Text sent to models which support system prompts. Gives the model
                overall context in how to respond. Use `auto` or None for the model default. Defaults
                to '' for no system prompt.
            pre_prompt_query:
                Text that is prepended before the contextual document chunks. The default can be
                customized per environment, but the standard default is :code:`"Pay attention and remember the information
                below, which will help to answer the question or imperative after the context ends.\\\\n"`
            prompt_query:
                Text that is appended to the beginning of the user's message. The default can be customized
                per environment, but the standard default is "According to only the information in the document sources
                provided within the context above, "
            pre_prompt_summary:
                Not yet used, use H2OGPTE.summarize_content
            prompt_summary:
                Not yet used, use H2OGPTE.summarize_content
            llm:
                Name or index of LLM to send the query. Use `H2OGPTE.get_llms()` to see all available options.
                Default value is to use the first model (0th index).
            llm_args:
                Dictionary of kwargs to pass to the llm.
            self_reflection_config: Dictionary of arguments for self-reflection, can contain the following string:string mappings:
                    llm_reflection: str
                        :code:`"gpt-4-0613"`  or :code:`""` to disable reflection
                    pre_prompt_reflection: str
                        :code:`"Pay attention to the following context. You will need to evaluate the quality of a response for a given prompt."`
                    prompt_reflection: str
                        'Given the above context, here\'s the prompt and the response: :code:`\"\"\"Prompt:\\\\n%s\\\\n\"\"\"\\\\n\\\\n\"\"\"Response:\\\\n%s\\\\n\"\"\"\\\\n\\\\nWhat is the quality of the response for the given prompt? Respond with a score ranging from Score: 0/10 (worst) to Score: 10/10 (best), and give a brief explanation why.'`
                    system_prompt_reflection: str
                        :code:`""`
                    llm_args_reflection: str
                        :code:`"{}"`
            rag_config:
                Dictionary of arguments to control RAG (retrieval-augmented-generation) types. Can contain the following key/value pairs:

                rag_type: str one of

                    :code:`"llm_only"` No RAG (LLM only)

                    :code:`"rag"` RAG (embed query)

                    :code:`"hyde1"` HyDE RAG (embed LLM response and query)

                    :code:`"hyde2"` HyDE RAG+ (embed HyDE RAG response and query)

                no_rag_llm_prompt_extension: str
                    example: :code:`'\\\\nKeep the answer brief, and list the 5 most relevant key words at the end.'`
            timeout:
                Amount of time in seconds to allow the request to run. The default is 1000 seconds.
            callback:
                Function for processing partial messages, used for streaming responses
                to an end user.

        Returns:
            ChatMessage: The response text and details about the response from the LLM.
            For example:

            .. code-block:: python

                ChatMessage(
                    id='XXX',
                    content='The information provided in the context...',
                    reply_to='YYY',
                    votes=0,
                    created_at=datetime.datetime(2023, 10, 24, 20, 12, 34, 875026)
                    type_list=[],
                )

        Raises:
          TimeoutError: The request did not complete in time.
        """
        correlation_id = str(uuid.uuid4())
        if self.rag_type:
            rag_config = {
                "rag_type": self.rag_type,
                "hyde_no_rag_llm_prompt_extension": self.hyde_no_rag_llm_prompt_extension,
            }
        request = ChatRequest(
            t="cq",
            mode="s",
            session_id=self._chat_session_id,
            correlation_id=correlation_id,
            body=message,
            system_prompt=self.system_prompt
            if system_prompt is None
            else system_prompt,
            pre_prompt_query=self.pre_prompt_query
            if pre_prompt_query is None
            else pre_prompt_query,
            prompt_query=self.prompt_query if prompt_query is None else prompt_query,
            pre_prompt_summary=pre_prompt_summary,
            prompt_summary=prompt_summary,
            llm=llm,
            llm_args=json.dumps(llm_args),
            self_reflection_config=json.dumps(self_reflection_config),
            rag_config=json.dumps(rag_config),
        )
        self.connection.send(serialize(request))

        if timeout is None:
            timeout = 1000
        deadline = time.time() + timeout
        request_id: Optional[str] = None
        while True:
            res = self.connection.recv(deadline - time.time())
            assert isinstance(res, str)
            payloads = res.splitlines()
            for payload in payloads:
                res = deserialize(payload)
                if res.t == "cx":  # ack
                    if res.session_id != self._chat_session_id:
                        continue
                    if res.correlation_id == correlation_id:
                        request_id = res.message_id
                elif res.t == "ca":  # response
                    if (
                        res.session_id != self._chat_session_id
                        or res.reply_to_id != request_id
                    ):
                        continue
                    chat_message = ChatMessage(
                        id=res.message_id,
                        content=res.body,
                        reply_to=res.reply_to_id,
                        votes=0,
                        created_at=datetime.now(),
                        type_list=[],
                    )
                    if callback:
                        callback(chat_message)
                        return
                    else:
                        return chat_message
                elif res.t == "cp":  # partial response
                    if callback:
                        if (
                            res.session_id != self._chat_session_id
                            or res.reply_to_id != request_id
                        ):
                            continue
                        callback(
                            PartialChatMessage(
                                id=res.message_id,
                                content=res.body,
                                reply_to=res.reply_to_id,
                            )
                        )
                elif res.t == "ce":
                    if (
                        res.session_id != self._chat_session_id
                        or res.reply_to_id != request_id
                    ):
                        continue
                    raise SessionError(f"Remote error: {res.body}")

    def disconnect(self):
        """Disconnect from an h2oGPTe server.

        This is primarily an internal function used when users create a
        session using `with` from the H2OGPTE.connection() function.
        """
        self.connection.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        self.disconnect()


def serialize(request: ChatRequest) -> str:
    return json.dumps(asdict(request), allow_nan=False, separators=(",", ":"))


def deserialize(response: str) -> Union[ChatResponse, ChatAcknowledgement, ChatError]:
    data = cast(Dict[str, Any], json.loads(response))
    t = data["t"]
    if t == "cx":
        return ChatAcknowledgement(**data)
    elif t == "ca" or t == "cp":
        return ChatResponse(**data)
    elif t == "ce":
        return ChatError(**data)
    else:
        raise SessionError(f"Invalid chat response type: {t}.")
