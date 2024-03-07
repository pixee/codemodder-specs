#!/usr/bin/env python3
import json

import click
import jsonschema


@click.command()
@click.argument('schema_file', type=click.File('r'))
def validate_schema(schema_file):
    schema = json.load(schema_file)
    jsonschema.Draft202012Validator.check_schema(schema)
    print('✅ Schema is valid')


if __name__ == '__main__':
    validate_schema()
