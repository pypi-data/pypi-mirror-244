import argparse
from abc import ABC
from http import HTTPStatus
from typing import Set, List, Optional

import uvicorn
import torch
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from transformers import PreTrainedTokenizerFast, PreTrainedTokenizer, AutoTokenizer, AutoModel, PreTrainedModel, BatchEncoding

from bixi.api.protocol import EmbeddingsRequest, EmbeddingsResponse, UsageInfo, ErrorResponse, ChatCompletionRequest, \
    CompletionRequest

app = FastAPI()


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


class EmbeddingModelWorker(ABC):
    def __init__(
            self,
            model_names: Set[str],
            limit_worker_concurrency: int,
            executor: [PreTrainedModel],
            tokenizer: [PreTrainedTokenizerFast, PreTrainedTokenizer]
    ):
        self.model_names = model_names
        self.limit_worker_concurrency = limit_worker_concurrency
        self.executor = executor
        self.tokenizer = tokenizer

    async def encode(self, inputs: List[str], batch_size: Optional[int] = 128):
        # Tokenize sentences
        encoded_input = self.tokenizer(inputs, padding=True, truncation=True, return_tensors='pt')
        # for s2p(short query to long passage) retrieval task, add an instruction to query (not add instruction for passages)
        # encoded_input = tokenizer([instruction + q for q in queries], padding=True, truncation=True, return_tensors='pt')
        return encoded_input

    # Compute token embeddings
    async def compute_embeddings(self, encoded_inputs: BatchEncoding):
        with torch.no_grad():
            model_output = self.executor(**encoded_inputs)
            # Perform pooling. In this case, cls pooling.
            sentence_embeddings = model_output[0][:, 0]
        # normalize embeddings
        sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)

        return sentence_embeddings
    async def decode(self, inputs: List[List[int]]):
        pass


@app.post("/v1/embeddings")
async def create_embeddings(request: EmbeddingsRequest):
    error_check_ret = await check_model(request, worker.model_names)
    if error_check_ret is not None:
        return error_check_ret

    inputs = []
    if isinstance(request.input, str):
        inputs.append(request.input)
    else:
        inputs += request.input
    token_number = 0
    encoded_inputs = await worker.encode(request.input, request.batch_size)
    for input_ids in encoded_inputs.input_ids:
        token_number += len(input_ids)
    result = await worker.compute_embeddings(encoded_inputs)
    data = []
    for index, value in enumerate(result):
        value_list = value.tolist()
        data.append(
            {
                "object": "embedding",
                "embedding": value_list,
                "index": index,
            }
        )
    usage = UsageInfo(
        prompt_tokens=token_number,
        total_tokens=token_number,
    )

    return EmbeddingsResponse(
        data=data,
        model=request.model,
        usage=usage
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--model-path", type=str, default="/workspace/models/bge-large-en-v1.5")
    parser.add_argument(
        "--model-names",
        type=lambda s: s.split(","),
        default="text-embedding-ada-002, bge-large-en",
        help="Optional display comma separated names",
    )
    parser.add_argument("--limit-worker-concurrency", type=int, default=1024)
    parser.add_argument("--num-gpus", type=int, default=1)
    parser.add_argument("--trust_remote_code", type=bool, default=True)

    args = parser.parse_args()
    tok = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True,)
    model = AutoModel.from_pretrained(args.model_path, trust_remote_code=True,)
    model.eval()
    worker = EmbeddingModelWorker(
        model_names=set(args.model_names),
        limit_worker_concurrency=args.limit_worker_concurrency,
        executor=model,
        tokenizer=tok
    )
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
