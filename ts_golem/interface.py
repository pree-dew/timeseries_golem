import json
import click
from multiprocessing import Process

from schema import SchemaError
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from ts_golem.golem_schema import signal_schema
from ts_golem.generate_timeseries import find_function

@click.group("cli", invoke_without_command=True)
@click.pass_context
def cli(ctx):
    pass

def validate_schema(ctx, sg_file):
    ctx.obj = dict()
    with open(sg_file, "r") as f:
        try:
            signal_details = json.loads(f.read())
            ctx.obj["signal_details"] = signal_details
        except json.decoder.JSONDecodeError as e:
            raise e
        try:
            validate(signal_details, signal_schema)
        except ValidationError as e:
            error_message = e.message.split('\n')[0]
            raise click.ClickException(f"Vaildation error:\n{error_message}\nPath: {e.json_path}")
        except SchemaError as se:
            named_errors = [e for e in se.errors if e is not None]
            if len(named_errors) != 0:
                err_message = "\n".join(named_errors)
                raise click.ClickException(f"Vaildation error:\n{err_message}")

            raise se
        return ctx
    

@cli.command(name="validate", help="parses the definition of signals that have been passed")
@click.pass_context
@click.option("-sg", "--sg-file", help="pass signal definitions via a json file")
def validate_signal(ctx, sg_file):
    validate_schema(ctx, sg_file)


@cli.command(name="generate", help="generate signals as per pattern you are looking for")
@click.pass_context
@click.option("-sg", "--sg-file", help="pass signal definitions via a json file")
@click.option("-cf", "--config-file", help="config for the generator")
def generate_signal(ctx, sg_file, config_file):
    validate_schema(ctx, sg_file)
    with open(config_file) as f:
        config = json.loads(f.read())

    # go over all signal details
    # excecute each signal in parallel
    processes = []
    i = 0
    for s in ctx.obj["signal_details"]:
        i += 1
        try:
            fun = find_function(s["signal_details"]["signal_type"])
        except KeyError as e:
            raise e
        p = Process(target=fun, args=[i, config, s])
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

def main():
    cli(prog_name="ts_golem")


if __name__ == '__main__':
    main()

