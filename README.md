A python CLI tool for managing convinient code snippets. 
Build with Typer and UV as dependency manager. 

# Make an alias, to avoid typing out the full name:
ct='uv run cool-tool'

To build the package do:
`uv build`

To run uv as shell (useful when doing development):
`uv tool install . -e`

To add dependencies:
`uv add <package-name>`
Note, you if it’s in the Python standard library → you don’t install it. E.g. just import itertools directly.

To increase by a minor update (use --dry-run to view changes first):
`uv version --bump minor --dry-run`

To update version manually (use --dry-run to view changes first):
`uv version 2.0.0 --dry-run`
