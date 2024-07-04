#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from .bench_result import BenchResult

@click.group()
@click.argument("path", type=str)
@click.pass_context
def main(ctx, path: str):
    ctx.obj = path

@main.command('to_csv')
@click.pass_obj
def to_csv(path: str):
    BenchResult(path).to_csv()



if __name__ == "__main__":
    main(None, None)