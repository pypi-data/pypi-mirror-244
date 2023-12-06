# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

# start a local terminal client

# This is the startup script for Smighty app
# Expected Use:
# ```
# python -m smighty.app.cli
# ```
# This will start a terminal client.
import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f'Hello, {name.capitalize()}!')


@app.command()
def goodbye():
    print('Have a great day!')


if __name__ == '__main__':
    app()
