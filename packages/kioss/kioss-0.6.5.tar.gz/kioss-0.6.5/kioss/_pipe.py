from abc import ABC, abstractmethod
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    List,
    Optional,
    Type,
    TypeVar,
)

from kioss import _util
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kioss._visit import _iter_production, _explanation
    from kioss._visit._base import AVisitor

T = TypeVar("T")
U = TypeVar("U")
R = TypeVar("R")

ITERATOR_PRODUCING_VISITOR_CLASS: "Optional[Type[_iter_production.IteratorProducingVisitor]]" = (
    None
)
EXPLAINING_VISITOR_CLASS: "Optional[Type[_explanation.ExplainingVisitor]]" = None


class APipe(Iterable[T], ABC):
    upstream: "Optional[APipe]"

    def __iter__(self) -> Iterator[T]:
        if ITERATOR_PRODUCING_VISITOR_CLASS is None:
            raise ValueError("_pipe.ITERATOR_PRODUCING_VISITOR_CLASS is None")
        return self._accept(ITERATOR_PRODUCING_VISITOR_CLASS())

    def __add__(self, other: "APipe[T]") -> "APipe[T]":
        return self.chain(other)

    def __repr__(self) -> str:
        """
        Explain the plan of the pipe
        """
        if EXPLAINING_VISITOR_CLASS is None:
            raise ValueError("_pipe.EXPLAINING_VISITOR_CLASS is None")
        return self._accept(EXPLAINING_VISITOR_CLASS())

    @abstractmethod
    def _accept(self, visitor: "AVisitor") -> Any:
        raise NotImplementedError()

    @staticmethod
    def sanitize_n_threads(n_threads: int):
        if not isinstance(n_threads, int):
            raise TypeError(
                f"n_threads should be an int but got '{n_threads}' of type {type(n_threads)}."
            )
        if n_threads < 1:
            raise ValueError(
                f"n_threads should be greater or equal to 1, but got {n_threads}."
            )

    def map(
        self,
        func: Callable[[T], R],
        n_threads: int = 1,
    ) -> "APipe[R]":
        """
        Apply a function to each element of the Pipe, creating a new Pipe with the mapped elements.

        Args:
            func (Callable[[T], R]): The function to be applied to each element.
            n_threads (int): The number of threads for concurrent execution (default is 1, meaning only the main thread is used).
        Returns:
            Pipe[R]: A new Pipe instance with elements resulting from applying the function to each element.
        """
        APipe.sanitize_n_threads(n_threads)
        return MapPipe(self, func, n_threads)

    def do(
        self,
        func: Callable[[T], Any],
        n_threads: int = 1,
    ) -> "APipe[T]":
        """
        Run the func as side effect: the resulting Pipe forwards the upstream elements after func execution's end.

        Args:
            func (Callable[[T], R]): The function to be applied to each element.
            n_threads (int): The number of threads for concurrent execution (default is 1, meaning only the main thread is used).
        Returns:
            Pipe[T]: A new Pipe instance with elements resulting from applying the function to each element.
        """
        APipe.sanitize_n_threads(n_threads)
        return DoPipe(self, func, n_threads)

    def flatten(
        self: "APipe[Iterator[R]]",
        n_threads: int = 1,
    ) -> "APipe[R]":
        """
        Flatten the elements of the Pipe, which are assumed to be iterators, creating a new Pipe with individual elements.

        Returns:
            Pipe[R]: A new Pipe instance with individual elements obtained by flattening the original elements.
            n_threads (int): The number of threads for concurrent execution (default is 1, meaning only the main thread is used).
        """
        APipe.sanitize_n_threads(n_threads)
        return FlattenPipe(self, n_threads)

    def chain(self, *others: "APipe[T]") -> "APipe[T]":
        """
        Create a new Pipe by chaining the elements of this Pipe with the elements from other Pipes. The elements of a given Pipe are yielded after its predecessor Pipe is exhausted.

        Args:
            *others (Pipe[T]): One or more additional Pipe instances to chain with this Pipe.

        Returns:
            Pipe[T]: A new Pipe instance with elements from this Pipe followed by elements from other Pipes.
        """
        return ChainPipe(self, list(others))

    def filter(self, predicate: Callable[[T], bool]) -> "APipe[T]":
        """
        Filter the elements of the Pipe based on the given predicate, creating a new Pipe with filtered elements.

        Args:
            predicate (Callable[[T], bool]): The function that determines whether an element should be included.

        Returns:
            Pipe[T]: A new Pipe instance with elements that satisfy the predicate.
        """
        return FilterPipe(self, predicate)

    def batch(self, size: int = 100, period: float = float("inf")) -> "APipe[List[T]]":
        """
        Batch elements of the Pipe into lists of a specified size or within a specified time window.

        Args:
            size (int, optional): The maximum number of elements per batch (default is 100).
            period (float, optional): The maximum number of seconds to wait before yielding a batch (default is infinity).

        Returns:
            Pipe[List[T]]: A new Pipe instance with lists containing batches of elements.
        """
        return BatchPipe(self, size, period)

    def slow(self, freq: float) -> "APipe[T]":
        """
        Slow down the iteration to a maximum frequency in Hz (max number of elements yielded per second).

        Args:
            freq (float): The maximum frequency in Hz of the iteration, i.e. how many elements will be yielded per second at most.

        Returns:
            Pipe[T]: A new Pipe instance with elements iterated at the specified frequency.
        """
        return SlowPipe(self, freq)

    def catch(
        self,
        *classes: Type[Exception],
        when: Optional[Callable[[Exception], bool]] = None,
    ) -> "APipe[T]":
        """
        Any error whose class is exception_class or a subclass of it will be catched and yielded.

        Args:
            classes (Type[Exception]): The class of exceptions to catch
            when (Callable[[Exception], bool], optional): catches an exception whose type is in `classes` only if this predicate function is None or evaluates to True.

        Returns:
            Pipe[T]: A new Pipe instance with error handling capability.
        """
        return CatchPipe(self, *classes, when=when)

    def log(self, what: str = "elements") -> "APipe[T]":
        """
        Log the elements of the Pipe as they are iterated.

        Args:
            what (str): name the objects yielded by the pipe for clearer logs, must be a plural descriptor.

        Returns:
            Pipe[T]: A new Pipe instance with logging capability.
        """
        return LogPipe(self, what)

    def collect(self, n_samples: Optional[int] = None) -> List[T]:
        """
        Convert the elements of the Pipe into a list. The entire pipe will be iterated, but only n_samples elements will be saved in the returned list.

        Args:
            n_samples (int, optional): The maximum number of elements to collect in the list (default is infinity).

        Returns:
            List[T]: A list containing the elements of the Pipe truncate to the first `n_samples` ones.
        """
        return [
            elem for i, elem in enumerate(self) if (n_samples is None or i < n_samples)
        ]

    def superintend(
        self,
        n_samples: int = 0,
        n_error_samples: int = 8,
        raise_if_more_errors_than: int = 0,
    ) -> List[T]:
        """
        Superintend the Pipe:
        - iterates over it until it is exhausted,
        - logs
        - catches exceptions log a sample of them at the end of the iteration
        - raises the first encountered error if more exception than `raise_if_more_errors_than` are catched during iteration.
        - else returns a sample of the output elements

        Args:
            n_samples (int, optional): The maximum number of elements to collect in the list (default is infinity).
            n_error_samples (int, optional): The maximum number of error samples to log (default is 8).
            raise_if_more_errors_than (int, optional): An error will be raised if the number of encountered errors is more than this threshold (default is 0).
        Returns:
            List[T]: A list containing the elements of the Pipe truncate to the first `n_samples` ones.
        Raises:
            RuntimeError: If more exception than `raise_if_more_errors_than` are catched during iteration.
        """
        if not isinstance(self, LogPipe):
            plan = self.log("output elements")
        else:
            plan = self
        error_samples: List[Exception] = []
        errors_count = 0

        def register_error_sample(error):
            nonlocal errors_count
            errors_count += 1
            if len(error_samples) < n_error_samples:
                error_samples.append(error)
            return True

        safe_plan = plan.catch(Exception, when=register_error_sample)
        _util.LOGGER.info(repr(safe_plan))
        samples = safe_plan.collect(n_samples=n_samples)
        if errors_count > 0:
            _util.LOGGER.error(
                "first %s error samples: %s\nWill now raise the first of them:",
                n_error_samples,
                list(map(repr, error_samples)),
            )
            if raise_if_more_errors_than < errors_count:
                raise error_samples[0]

        return samples


class SourcePipe(APipe[T]):
    def __init__(self, source: Callable[[], Iterator[T]]):
        """
        Initialize a Pipe with a data source.

        The source must be a callable that returns an iterator, i.e., an object implementing __iter__ and __next__ methods.
        Each subsequent iteration over the pipe will use a fresh iterator obtained from `source()`.

        Args:
            source (Callable[[], Iterator[T]]): A factory function called to obtain a fresh data source iterator for each iteration.
        """
        self.upstream = None
        if not callable(source):
            raise TypeError(
                f"source must be a callable returning an iterator, but the provided source is not a callable: got source '{source}' of type {type(source)}."
            )
        self.source = source

    def _accept(self, visitor: "AVisitor") -> Any:
        return visitor.visit_source_pipe(self)


class FilterPipe(APipe[T]):
    def __init__(self, upstream: APipe[T], predicate: Callable[[T], bool]):
        self.upstream: APipe[T] = upstream
        self.predicate = predicate

    def _accept(self, visitor: "AVisitor") -> Any:
        return visitor.visit_filter_pipe(self)


class MapPipe(APipe[R]):
    def __init__(self, upstream: APipe[T], func: Callable[[T], R], n_threads: int):
        self.upstream: APipe[T] = upstream
        self.func = func
        self.n_threads = n_threads

    def _accept(self, visitor: "AVisitor") -> Any:
        return visitor.visit_map_pipe(self)


class DoPipe(APipe[T]):
    def __init__(self, upstream: APipe[T], func: Callable[[T], R], n_threads: int):
        self.upstream: APipe[T] = upstream
        self.func = func
        self.n_threads = n_threads

    def _accept(self, visitor: "AVisitor") -> Any:
        return visitor.visit_do_pipe(self)


class LogPipe(APipe[T]):
    def __init__(self, upstream: APipe[T], what: str = "elements"):
        self.upstream: APipe[T] = upstream
        self.what = what

    def _accept(self, visitor: "AVisitor") -> Any:
        return visitor.visit_log_pipe(self)


class FlattenPipe(APipe[T]):
    def __init__(self, upstream: APipe[Iterator[T]], n_threads: int):
        self.upstream: APipe[Iterator[T]] = upstream
        self.n_threads = n_threads

    def _accept(self, visitor: "AVisitor") -> Any:
        return visitor.visit_flatten_pipe(self)


class BatchPipe(APipe[List[T]]):
    def __init__(self, upstream: APipe[T], size: int, period: float):
        self.upstream: APipe[T] = upstream
        self.size = size
        self.period = period

    def _accept(self, visitor: "AVisitor") -> Any:
        return visitor.visit_batch_pipe(self)


class CatchPipe(APipe[T]):
    def __init__(
        self,
        upstream: APipe[T],
        *classes: Type[Exception],
        when: Optional[Callable[[Exception], bool]] = None,
    ):
        self.upstream: APipe[T] = upstream
        self.classes = classes
        self.when = when

    def _accept(self, visitor: "AVisitor") -> Any:
        return visitor.visit_catch_pipe(self)


class ChainPipe(APipe[T]):
    def __init__(self, upstream: APipe[T], others: List[APipe]):
        self.upstream: APipe[T] = upstream
        self.others = others

    def _accept(self, visitor: "AVisitor") -> Any:
        return visitor.visit_chain_pipe(self)


class SlowPipe(APipe[T]):
    def __init__(self, upstream: APipe[T], freq: float):
        self.upstream: APipe[T] = upstream
        self.freq = freq

    def _accept(self, visitor: "AVisitor") -> Any:
        return visitor.visit_slow_pipe(self)
