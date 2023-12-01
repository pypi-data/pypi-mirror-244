import argparse
from typing import Callable, Dict, List, Tuple, Union

class MultiParser:
    parsers: Dict[str, Tuple[Callable[[argparse.Namespace], None], argparse.ArgumentParser]]

    def __init__(self) -> None: ...

    def register_parser(
        self,
        parser_name: str,
        executor: Callable[[argparse.Namespace], None],
        parser_factory: Callable[[], argparse.ArgumentParser],
    ) -> None: ...

    def parse_arguments(self, arguments: Union[List[str], None], parser_name: str) -> argparse.Namespace: ...

    def run(self) -> None: ...
