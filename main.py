import argparse
import random
import subprocess
import tempfile
from pathlib import Path

from language.emitter import Emitter
from language.lexer import Lexer
from language.parser import Parser


def main(source_file, output_file, debug=False):
    with open(source_file, 'r') as inputFile:
        source = inputFile.read()

    output_file = Path(output_file)

    if debug:
        c_file = output_file.parent / f"{output_file.name}.cpp"
    else:
        c_file = Path(tempfile.gettempdir()) / f"{random.randint(0, 10000)}{output_file.name}.cpp"

    output_file.parent.mkdir(parents=True, exist_ok=True)

    lexer = Lexer(source)
    emitter = Emitter(c_file)

    parser = Parser(lexer, emitter)

    try:
        parser.program()
        subprocess.check_output(['g++', str(c_file), '-o', str(output_file)])
    except FileNotFoundError:
        print("G++ not found. Please install G++ and try again.")
    except Exception as e:
        print(e)
    finally:
        if not debug:
            c_file.unlink(missing_ok=True)


if __name__ == '__main__':
    args = argparse.ArgumentParser(
        prog='Not Python',
        description='A simple compiler written in Python'
    )

    args.add_argument('filename')  # positional argument
    args.add_argument('-d', '--debug', action='store_true', help='Preserve intermediate files')
    args.add_argument('-o', '--output', default=None, help='Output executable name')

    args = args.parse_args()

    if args.output is None:
        output = Path(args.filename).parent / f"{Path(args.filename).name.split('.')[0]}.exe"
    else:
        output = args.output

    main(args.filename, output, args.debug)
