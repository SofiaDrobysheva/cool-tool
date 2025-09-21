import typer

from cool_tool.commands.hi import hi
from cool_tool.commands.hello import hello
from cool_tool.commands.distance_matrix_hamming import count_hamming

app = typer.Typer()

# Register flat commands
app.command()(hi)
app.command()(hello)
app.command()(count_hamming)
