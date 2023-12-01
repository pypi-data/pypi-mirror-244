import argparse
import json
import time
from abc import ABC
from asyncio import Semaphore
from http import HTTPStatus
from typing import List, Union, Dict, Optional, Tuple, AsyncGenerator, Set

import shortuuid
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.exceptions import RequestValidationError
from fastapi.responses import StreamingResponse, JSONResponse
import uvicorn
from transformers import PreTrainedTokenizerFast, PreTrainedTokenizer
from vllm import AsyncLLMEngine, RequestOutput
from vllm.config import ModelConfig
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.sampling_params import SamplingParams
from vllm.utils import random_uuid
import uuid
from vllm.utils import random_uuid
import uuid
from bixi.conversation import Conversation, SeparatorStyle
from bixi.api.protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseStreamChoice,
    ChatCompletionStreamResponse,
    ChatMessage,
    ChatCompletionResponseChoice,
    CompletionRequest,
    CompletionResponse,
    CompletionResponseChoice,
    DeltaMessage,
    CompletionResponseStreamChoice,
    CompletionStreamResponse,
    ErrorResponse,
    ModelPermission,
    UsageInfo,
)

app = FastAPI()


class CompletionModelWorker(ABC):

    def __init__(
            self,
            tokenizer: [PreTrainedTokenizerFast, PreTrainedTokenizer],
            worker_id: str,
            model_names: Set,
            limit_worker_concurrency: int,
            executor: AsyncLLMEngine,
            conversation_template_file: str,
    ):
        self.tokenizer = tokenizer
        self.worker_id = worker_id
        self.model_names = model_names
        self.limit_worker_concurrency = limit_worker_concurrency
        self.executor = executor
        self.conversation_template = Conversation.load_from_file(conversation_template_file)
        self.semaphore = Semaphore(limit_worker_concurrency)

    def get_conversation_template(
            self,
    ) -> Conversation:
        """
        can be overrided to costomize the conversation template for different model workers.
        """
        return self.conversation_template

    def generate(
            self,
            request_id: str,
            sampling_params: SamplingParams,
            prompt_token_ids: Optional[List[int]] = None,
    ) -> RequestOutput:
        # TODO semaphore control
        return self.executor.generate(
            prompt=None,
            request_id=request_id,
            sampling_params=sampling_params,
            prompt_token_ids=prompt_token_ids
        )


def _add_to_set(s, new_stop):
    if not s:
        return
    if isinstance(s, str):
        new_stop.add(s)
    else:
        new_stop.update(s)


async def check_model(
        request: [ChatCompletionRequest, CompletionRequest],
        model_names: set) -> Optional[JSONResponse]:
    if request.model in model_names:
        return
    ret = create_error_response(
        HTTPStatus.NOT_FOUND,
        f"The model `{request.model}` does not exist.",
    )
    return ret


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):  # pylint: disable=unused-argument
    return create_error_response(HTTPStatus.BAD_REQUEST, str(exc))


def create_error_response(
        status_code: HTTPStatus,
        message: str) -> JSONResponse:
    return JSONResponse(
        ErrorResponse(
            message=message,
            code=status_code.value
        )
        .dict(),
        status_code=status_code.value)


async def check_length(
        request: Union[ChatCompletionRequest, CompletionRequest],
        model_config: ModelConfig,
        prompt: Optional[str] = None,
        prompt_ids: Optional[List[int]] = None
) -> Tuple[List[int], Optional[JSONResponse]]:
    assert (not (prompt is None and prompt_ids is None)
            and not (prompt is not None and prompt_ids is not None)
            ), "Either prompt or prompt_ids should be provided."
    if prompt_ids is not None:
        input_ids = prompt_ids
    else:
        input_ids = worker.tokenizer.encode(prompt)
    token_num = len(input_ids)
    max_model_len = model_config.max_model_len
    if request.max_tokens is None:
        request.max_tokens = max_model_len - token_num
    if token_num + request.max_tokens > max_model_len:
        return input_ids, create_error_response(
            HTTPStatus.BAD_REQUEST,
            f"This model's maximum context length is {max_model_len} tokens. "
            f"However, you requested {request.max_tokens + token_num} tokens "
            f"({token_num} in the messages, "
            f"{request.max_tokens} in the completion). "
            f"Please reduce the length of the messages or completion.",
        )
    else:
        return input_ids, None


async def generate_prompt(
        conversation: Conversation,
        request: [ChatCompletionRequest, CompletionRequest],
) -> str:
    if isinstance(request, ChatCompletionRequest):
        if isinstance(request.messages, str):
            _content = request.messages
            conversation.append_message(conversation.roles[0], _content)
            conversation.append_message(conversation.roles[1], None)
            prompt = conversation.get_prompt()
        else:
            for message in request.messages:
                msg_role = message["role"]
                if msg_role == "system":
                    conversation.set_system_message(message["content"])
                elif msg_role == "user":
                    conversation.append_message(conversation.roles[0], message["content"])
                elif msg_role == "assistant":
                    conversation.append_message(conversation.roles[1], message["content"])
                else:
                    raise ValueError(f"Unknown role: {msg_role}")
            # Add a blank message for the assistant.
            conversation.append_message(conversation.roles[1], None)
            prompt = conversation.get_prompt()
    else:
        if isinstance(request.prompt, str):
            _content = request.prompt
            conversation.append_message(conversation.roles[0], _content)
            conversation.append_message(conversation.roles[1], None)
            prompt = conversation.get_prompt()
        else:
            conversation.append_message(conversation.roles[0], "")
            conversation.append_message(conversation.roles[1], None)
            prompt = conversation.get_prompt()

    return prompt


async def generate_sampling_parameters(
        conversation: Conversation,
        request: [ChatCompletionRequest, CompletionRequest]
) -> SamplingParams:

    use_beam_search = False
    skip_special_tokens = False
    ignore_eos = False
    new_stop = set()
    _add_to_set(request.stop, new_stop)
    for tid in conversation.stop_token_ids:
        stop_str = worker.tokenizer.decode(tid)
        _add_to_set(stop_str, new_stop)

    sampling_params = SamplingParams(
        n=request.n,
        presence_penalty=request.presence_penalty,
        frequency_penalty=request.frequency_penalty,
        temperature=request.temperature,
        top_p=request.top_p,
        stop=list(new_stop),
        stop_token_ids=conversation.stop_token_ids,
        max_tokens=request.max_tokens,
        best_of=request.best_of,
        top_k=request.top_k,
        ignore_eos=ignore_eos,
        use_beam_search=use_beam_search,
        skip_special_tokens=skip_special_tokens,
    )
    return sampling_params


def create_chat_stream_response_json(
        request_id: str,
        created_time: int,
        model_name: str,
        index: int,
        text: str,
        finish_reason: Optional[str] = None,
        usage: Optional[UsageInfo] = None,
) -> str:
    choice_data = ChatCompletionResponseStreamChoice(
        index=index,
        delta=DeltaMessage(content=text),
        finish_reason=finish_reason,
    )
    response = ChatCompletionStreamResponse(
        id=request_id,
        created=created_time,
        model=model_name,
        choices=[choice_data],
    )
    if usage is not None:
        response.usage = usage
    # exclude unset to leave details out of each sse
    response_json = json.dumps(response.dict(exclude_unset=True), ensure_ascii=False)
    return response_json


def create_stream_response_json(
        request_id: str,
        created_time: int,
        model_name: str,
        index: int,
        text: str,
        finish_reason: Optional[str] = None,
) -> str:
    choice_data = CompletionResponseStreamChoice(
        index=index,
        text=text,
        finish_reason=finish_reason,
    )
    response = CompletionStreamResponse(
        id=request_id,
        created=created_time,
        model=model_name,
        choices=[choice_data],
    )
    # exclude unset to leave details out of each sse
    response_json = json.dumps(response.dict(exclude_unset=True), ensure_ascii=False)
    return response_json


async def chat_completion_stream_generator(
        model_name: str,
        request_id: str,
        created_time: int,
        request: ChatCompletionRequest,
        result_generator: RequestOutput
) -> AsyncGenerator[str, None]:
    # First chunk with role
    for i in range(request.n):
        choice_data = ChatCompletionResponseStreamChoice(
            index=i,
            delta=DeltaMessage(role="assistant"),
            finish_reason=None,
        )
        chunk = ChatCompletionStreamResponse(id=request_id,
                                             choices=[choice_data],
                                             model=model_name)
        data = json.dumps(chunk.dict(exclude_unset=True), ensure_ascii=False)
        yield f"data: {data}\n\n"

    previous_texts = [""] * request.n
    previous_num_tokens = [0] * request.n
    async for res in result_generator:
        res: RequestOutput
        for output in res.outputs:
            i = output.index
            delta_text = output.text[len(previous_texts[i]):]
            previous_texts[i] = output.text
            completion_tokens = len(output.token_ids)
            previous_num_tokens[i] = completion_tokens
            response_json = create_chat_stream_response_json(
                model_name=model_name,
                created_time=created_time,
                request_id=request_id,
                index=i,
                text=delta_text,
            )
            yield f"data: {response_json}\n\n"
            if output.finish_reason is not None:
                prompt_tokens = len(res.prompt_token_ids)
                final_usage = UsageInfo(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                )
                response_json = create_chat_stream_response_json(
                    model_name=model_name,
                    created_time=created_time,
                    request_id=request_id,
                    index=i,
                    text="",
                    finish_reason=output.finish_reason,
                    usage=final_usage,
                )
                yield f"data: {response_json}\n\n"
    yield "data: [DONE]\n\n"


async def completion_stream_generator(
        model_name: str,
        request_id: str,
        created_time: int,
        request: [ChatCompletionRequest, CompletionRequest],
        result_generator: RequestOutput
) -> AsyncGenerator[str, None]:
    # First chunk with role
    previous_texts = [""] * request.n
    previous_num_tokens = [0] * request.n
    async for res in result_generator:
        res: RequestOutput
        for output in res.outputs:
            i = output.index
            delta_text = output.text[len(previous_texts[i]):]
            previous_texts[i] = output.text
            completion_tokens = len(output.token_ids)
            previous_num_tokens[i] = completion_tokens
            response_json = create_stream_response_json(
                model_name=model_name,
                created_time=created_time,
                request_id=request_id,
                index=i,
                text=delta_text,
            )
            yield f"data: {response_json}\n\n"
            if output.finish_reason is not None:
                response_json = create_stream_response_json(
                    model_name=model_name,
                    created_time=created_time,
                    request_id=request_id,
                    index=i,
                    text="",
                    finish_reason=output.finish_reason,
                )
                yield f"data: {response_json}\n\n"
    yield "data: [DONE]\n\n"


@app.post("/v1/chat/completions")
async def create_chat_completion(
        request: ChatCompletionRequest,
        raw_request: Request):
    """Completion API similar to OpenAI's API.

    See  https://platform.openai.com/docs/api-reference/chat/create
    for the API specification. This API mimics the OpenAI ChatCompletion API.

    NOTE: Currently we do not support the following features:
        - function_call (Users should implement this by themselves)
        - logit_bias (to be supported by vLLM engine)
    """
    # logger.info(f"Received chat completion request: {request}")
    error_check_ret = await check_model(request, worker.model_names)
    if error_check_ret is not None:
        return error_check_ret
    conv = worker.get_conversation_template().copy()
    model_config = (await engine.get_model_config())
    prompt = await generate_prompt(conv, request)
    prompt_ids, error_check_ret = await check_length(
        request=request,
        prompt=prompt,
        model_config=model_config
    )
    if error_check_ret is not None:
        return error_check_ret
    sampling = await generate_sampling_parameters(conv, request)
    model_name = request.model
    request_id = f"chatcmpl-{random_uuid()}"
    created_time = int(time.monotonic())

    result_generator = worker.generate(request_id, sampling, prompt_ids)

    if request.stream:
        return StreamingResponse(chat_completion_stream_generator(
            model_name=model_name,
            request_id=request_id,
            created_time=created_time,
            request=request,
            result_generator=result_generator
        ),
            media_type="text/event-stream")
    # Non-streaming response
    choices = []
    # usage = UsageInfo()
    final_res: RequestOutput = None
    async for res in result_generator:
        if await raw_request.is_disconnected():
            # Abort the request if the client disconnects.
            await engine.abort(request_id)
            return create_error_response(HTTPStatus.BAD_REQUEST,
                                         "Client disconnected")
        if res.finished:
            final_res = res
    assert final_res is not None
    for output in final_res.outputs:
        choice_data = ChatCompletionResponseChoice(
            index=output.index,
            message=ChatMessage(role="assistant", content=output.text),
            finish_reason=output.finish_reason,
        )
        choices.append(choice_data)

    num_prompt_tokens = len(final_res.prompt_token_ids)
    num_generated_tokens = sum(
        len(output.token_ids) for output in final_res.outputs)
    usage = UsageInfo(
        prompt_tokens=num_prompt_tokens,
        completion_tokens=num_generated_tokens,
        total_tokens=num_prompt_tokens + num_generated_tokens,
    )
    return ChatCompletionResponse(model=request.model, choices=choices, usage=usage)


@app.post("/v1/completions")
async def create_completion(request: CompletionRequest, raw_request: Request):
    """Completion API similar to OpenAI's API.

        See https://platform.openai.com/docs/api-reference/completions/create
        for the API specification. This API mimics the OpenAI Completion API.

        NOTE: Currently we do not support the following features:
            - echo (since the vLLM engine does not currently support
              getting the logprobs of prompt tokens)
            - suffix (the language models we currently support do not support
              suffix)
            - logit_bias (to be supported by vLLM engine)
        """
    # logger.info(f"Received completion request: {request}")
    if not isinstance(request.prompt, str):
        return create_error_response(HTTPStatus.BAD_REQUEST,
                                     "please provide correct prompt, prompt should be string")
    error_check_ret = await check_model(request, worker.model_names)
    if error_check_ret is not None:
        return error_check_ret

    conv = worker.get_conversation_template().copy()
    model_config = (await engine.get_model_config())
    prompt = await generate_prompt(conv, request)
    prompt_ids, error_check_ret = await check_length(
        request=request,
        prompt=prompt,
        model_config=model_config
    )
    if error_check_ret is not None:
        return error_check_ret
    sampling = await generate_sampling_parameters(conv, request)
    model_name = request.model
    request_id = f"cmpl-{random_uuid()}"
    created_time = int(time.monotonic())
    result_generator = worker.generate(request_id, sampling, prompt_ids)

    if request.stream:
        return StreamingResponse(completion_stream_generator(
            model_name=model_name,
            request_id=request_id,
            created_time=created_time,
            request=request,
            result_generator=result_generator
        ),
            media_type="text/event-stream")
    # Non-streaming response
    choices = []
    # usage = UsageInfo()
    final_res: RequestOutput = None
    async for res in result_generator:
        if await raw_request.is_disconnected():
            # Abort the request if the client disconnects.
            await engine.abort(request_id)
            return create_error_response(HTTPStatus.BAD_REQUEST,
                                         "Client disconnected")
        if res.finished:
            final_res = res
    assert final_res is not None
    for output in final_res.outputs:
        choice_data = CompletionResponseChoice(
            index=output.index,
            text=output.text,
            finish_reason=output.finish_reason,
        )
        choices.append(choice_data)

    num_prompt_tokens = len(final_res.prompt_token_ids)
    num_generated_tokens = sum(
        len(output.token_ids) for output in final_res.outputs)
    usage = UsageInfo(
        prompt_tokens=num_prompt_tokens,
        completion_tokens=num_generated_tokens,
        total_tokens=num_prompt_tokens + num_generated_tokens,
    )
    return CompletionResponse(model=request.model, choices=choices, usage=usage)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--model-path", type=str, default="/workspace/models/Qwen-14B-Chat-AWQ")
    parser.add_argument(
        "--model-names",
        type=lambda s: s.split(","),
        default="gpt-3.5-turbo",
        help="Optional display comma separated names",
    )
    parser.add_argument("--limit-worker-concurrency", type=int, default=1024)
    parser.add_argument("--num-gpus", type=int, default=1)
    parser.add_argument("--trust_remote_code", type=bool, default=True)
    parser.add_argument(
        "--conv-template-path", type=str, default="/workspace/model-worker", help="Conversation prompt template json file."
    )

    parser = AsyncEngineArgs.add_cli_args(parser)
    args = parser.parse_args()
    if args.model_path:
        args.model = args.model_path
    if args.num_gpus > 1:
        args.tensor_parallel_size = args.num_gpus

    engine_args = AsyncEngineArgs.from_cli_args(args)
    engine = AsyncLLMEngine.from_engine_args(engine_args)
    wid = "1"
    worker = CompletionModelWorker(
        worker_id=wid,
        model_names=set(args.model_names),
        limit_worker_concurrency=args.limit_worker_concurrency,
        executor=engine,
        tokenizer=engine.engine.tokenizer,
        conversation_template_file=args.conv_template_path,
    )
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
