from io import TextIOBase
import tiktoken
from tiktoken.model import MODEL_TO_ENCODING
import click


__version__ = "1.0.0"

@click.command()
@click.option("--model", default="gpt-3.5-turbo", type=click.Choice(MODEL_TO_ENCODING.keys()))
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default=click.get_text_stream("stdout"))
def encode(model: str, input: TextIOBase, output: TextIOBase):
    encoding = tiktoken.encoding_for_model(model)
    output.write("\n".join(map(str, encoding.encode(input.read()))))
    output.write("\n")