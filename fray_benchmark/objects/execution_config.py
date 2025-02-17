import json
from typing import List, Dict, Any
from dataclasses import dataclass, field, asdict

@dataclass
class Executor:
    clazz: str
    method: str
    args: List[Any] = field(default_factory=list)
    classpaths: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RunConfig:
    executor: Executor
    ignore_unhandled_exceptions: bool = False
    interleave_memory_ops: bool = False
    max_scheduled_step: int = -1
    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=4)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        executor_data = data.pop('executor')
        executor = Executor(**executor_data)
        return cls(executor=executor, **data)