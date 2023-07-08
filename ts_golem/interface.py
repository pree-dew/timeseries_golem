import json
import click

from schema import SchemaError
from jsonschema import validate
from multiprocessing import Process
from jsonschema.exceptions import ValidationError

from ts_golem.golem_schema import signal_schema
from ts_golem.reload import with_or_without_reload
from ts_golem.generate_timeseries import find_function

@click.group("cli", invoke_without_command=True)
@click.pass_context
def cli(ctx):
    pass

def validate_schema(ctx, sg_file):
    if ctx.obj is None:
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
@click.option("-sg", "--sg-file", required=True, help="pass signal definitions via a json file")
def validate_signal(ctx, sg_file):
    validate_schema(ctx, sg_file)


@cli.command(name="generate", help="generate signals as per pattern you are looking for")
@click.pass_context
@click.option("-sg", "--sg-file", required=True, help="pass signal definitions via a json file")
@click.option("-cf", "--config-file", required=True, help="config for the generator")
@click.option("-rl", "--reload", is_flag=True, show_default=True, default=False, help="allows hot reload of signal details file")
@with_or_without_reload
def generate_signal(ctx, sg_file, config_file, reload):
    validate_schema(ctx, sg_file)
    with open(config_file) as f:
        config = json.loads(f.read())

    # go over all signal details
    # excecute each signal in parallel
    processes = []
    signal_no = 0
    if "observer" in ctx.obj:
        ctx.obj["observer"].start()

    while not ctx.obj.get("reload", False):
        for s in ctx.obj["signal_details"]:
            signal_no += 1
            try:
                fun = find_function(s["signal_details"]["signal_type"])
            except KeyError as e:
                if "observer" in ctx.obj:
                    ctx.obj["observer"].stop()
                    ctx.obj["observer"].join()
                raise e

            p = Process(target=fun, args=[signal_no, config, s])
            processes.append(p)
            p.start()

        if "observer" in ctx.obj:
             # wait for the reload event, if it happens then
             # terminate the existing process
             # initialise the new ones
             while not ctx.obj.get("reload", False):
                 pass
             for p in processes:
                p.terminate()

        for p in processes:
            p.join()

        if ctx.obj.get("reload", False) == True:
            ctx.obj["reload"] = False
            # reset signal number
            signal_no = 0
            validate_schema(ctx, sg_file)

    if "observer" in ctx.obj:
        ctx.obj["observer"].stop()
        ctx.obj["observer"].join()

def main():
    cli(prog_name="ts_golem")


if __name__ == '__main__':
    main()

