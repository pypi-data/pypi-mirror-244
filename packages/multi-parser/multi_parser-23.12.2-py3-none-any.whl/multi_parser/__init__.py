import argparse
import sys
from typing import Dict, List, Tuple, Union
from typing import Callable


class MultiParser:
    parsers: Dict[str, Tuple[Callable[[argparse.Namespace], None], argparse.ArgumentParser]]

    def __init__(self) -> None:
        self.parsers = {}

    def register_parser(
            self,
            parser_name: str,
            executor: Callable[[argparse.Namespace], None],
            parser_factory: Callable[[], argparse.ArgumentParser],
    ) -> None:
        if parser_name in self.parsers:
            raise ValueError(f'Parser "{parser_name}" is already registered.')

        self.parsers[parser_name] = (executor, parser_factory())

    def parse_arguments(self, arguments: Union[List[str], None], parser_name: str) -> argparse.Namespace:
        if parser_name not in self.parsers:
            raise ValueError(f'No parser registered for parser "{parser_name}".')

        parser_arguments = []
        new_parser = False

        for argument in arguments:
            if not argument.startswith('--') and new_parser:
                break

            if new_parser:
                parser_arguments.append(argument)

            if argument == parser_name:
                new_parser = True

        _, parser_factory = self.parsers[parser_name]

        return parser_factory.parse_args(parser_arguments)

    def run(self) -> None:
        if len(sys.argv) == 1:
            print("No parser specified. Available parsers are:", ', '.join(self.parsers.keys()))
            return

        parser_names = [
            argument for argument in sys.argv[1:] if not argument.startswith('--') and argument in self.parsers
        ]

        if not parser_names:
            print("Invalid or no parser specified. Available parsers are:", ', '.join(self.parsers.keys()))
            return

        for parser_name in parser_names:
            try:

                parser_arguments = self.parse_arguments(sys.argv[1:], parser_name)
                executor = self.parsers[parser_name][0]
                executor(parser_arguments)

            except ValueError as error:
                print(f"Value error processing '{parser_name}': {error}")

            except argparse.ArgumentError as error:
                print(f"Argument parsing error in '{parser_name}': {error}")
