from abc import ABC, abstractmethod
from typing import Any, Type, Callable, List, TypeVar


class PipelineOperation(ABC):
    @abstractmethod
    def process(self, data: Any) -> Any: ...


class FastInstantiateMeta(type):
    def __getattr__(self, attribute, *args, **kwargs):
        instantiated = self(*args, **kwargs)
        return getattr(instantiated, attribute)


T = TypeVar('T', bound='Pipeline')


class PyPipeline(metaclass=FastInstantiateMeta):
    def __init__(self):
        self.operations = None

    @classmethod
    def send(cls: Type[T], data: Any) -> T:
        obj = cls()
        obj.data = data
        obj.operations = []
        return obj

    def through(self: T, operations: List[Type[PipelineOperation]]) -> T:
        for operation in operations:
            if not isinstance(operation, type) or not issubclass(operation, PipelineOperation):
                raise ValueError(f"{operation} is not a valid subclass of PipelineOperation.")
        self.operations = operations
        return self

    def then(self, callback: Callable) -> Any:
        if not self.operations:
            raise TypeError("No operations provided.")
        for operation in self.operations:
            # Simulating processing using operation as a class or function
            self.data = self.run_operation(operation, self.data)
        # Applying the final callback to the processed data
        return callback(self.data)

    def then_return(self) -> Any:
        if not self.operations:
            raise TypeError("No operations provided.")
        for operation in self.operations:
            # Simulating processing using operation as a class or function
            self.data = self.run_operation(operation, self.data)

        return self.data

    @staticmethod
    def run_operation(op: Type[PipelineOperation], data: Any) -> Any:
        if not issubclass(op, PipelineOperation):
            raise TypeError("Pipeline operation must be a subclass of PipelineOperation.")

        try:
            return op().process(data)
        except Exception as e:
            raise RuntimeError(f"Error running operation {op.__name__}: {str(e)}")

    def pipes(self):
        return self.operations