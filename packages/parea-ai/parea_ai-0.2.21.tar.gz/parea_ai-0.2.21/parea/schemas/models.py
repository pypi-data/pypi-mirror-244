from typing import Any, Dict, List, Optional, Union

from enum import Enum

from attrs import define, field, validators


class Role(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"
    example_user = "example_user"
    example_assistant = "example_assistant"


@define
class Message:
    content: str
    role: Role = Role.user

    def to_dict(self) -> dict[str, str]:
        return {
            "content": self.content,
            "role": str(self.role),
        }


@define
class ModelParams:
    temp: float = 1.0
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    max_length: Optional[int] = None


@define
class LLMInputs:
    model: Optional[str] = None
    provider: Optional[str] = None
    model_params: Optional[ModelParams] = None
    messages: Optional[List[Message]] = None
    functions: Optional[List[Any]] = None
    function_call: Optional[Union[str, dict[str, str]]] = None


@define
class Completion:
    inference_id: Optional[str] = None
    trace_name: Optional[str] = None
    llm_inputs: Optional[dict[str, Any]] = None
    llm_configuration: LLMInputs = LLMInputs()
    end_user_identifier: Optional[str] = None
    deployment_id: Optional[str] = None
    name: Optional[str] = None
    metadata: Optional[dict] = None
    tags: Optional[list[str]] = None
    target: Optional[str] = None
    cache: bool = True
    log_omit_inputs: bool = False
    log_omit_outputs: bool = False
    log_omit: bool = False


@define
class CompletionResponse:
    inference_id: str
    content: str
    latency: float
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost: float
    model: str
    provider: str
    cache_hit: bool
    status: str
    start_timestamp: str
    end_timestamp: str
    error: Optional[str] = None
    trace_id: Optional[str] = None


@define
class UseDeployedPrompt:
    deployment_id: str
    llm_inputs: Optional[dict[str, Any]] = None


@define
class Prompt:
    raw_messages: list[dict[str, Any]]
    messages: list[dict[str, Any]]
    inputs: Optional[dict[str, Any]] = None


@define
class UseDeployedPromptResponse:
    deployment_id: str
    name: Optional[str] = None
    functions: Optional[dict[str, Any]] = None
    function_call: Optional[str] = None
    prompt: Optional[Prompt] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    model_params: Optional[dict[str, Any]] = None


@define
class FeedbackRequest:
    score: float = field(validator=[validators.ge(0), validators.le(1)])
    trace_id: Optional[str] = None
    inference_id: Optional[str] = None
    name: Optional[str] = None
    target: Optional[str] = None


@define
class NamedEvaluationScore:
    name: str
    score: float = field(validator=[validators.ge(0), validators.le(1)])


@define
class Log:
    configuration: LLMInputs = LLMInputs()
    inputs: Optional[Dict[str, str]] = None
    output: Optional[str] = None
    target: Optional[str] = None
    latency: Optional[float] = 0.0
    input_tokens: Optional[int] = 0
    output_tokens: Optional[int] = 0
    total_tokens: Optional[int] = 0
    cost: Optional[float] = 0.0


@define
class TraceLog(Log):
    trace_id: Optional[str] = field(default=None, validator=validators.instance_of(str))
    start_timestamp: Optional[str] = field(default=None, validator=validators.instance_of(str))
    organization_id: Optional[str] = None

    # metrics filled from completion
    error: Optional[str] = None
    status: Optional[str] = None
    deployment_id: Optional[str] = None
    cache_hit: bool = False
    output_for_eval_metrics: Optional[str] = None
    evaluation_metric_names: Optional[List[str]] = None
    scores: Optional[List[NamedEvaluationScore]] = None
    feedback_score: Optional[float] = None

    # info filled from decorator
    trace_name: Optional[str] = None
    children: List[str] = field(factory=list)

    # metrics filled from either decorator or completion
    end_timestamp: Optional[str] = None
    end_user_identifier: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None
    tags: Optional[List[str]] = None


@define
class TraceLogTree(TraceLog):
    children: Optional[list[TraceLog]] = None


@define
class CacheRequest:
    configuration: LLMInputs = LLMInputs()
