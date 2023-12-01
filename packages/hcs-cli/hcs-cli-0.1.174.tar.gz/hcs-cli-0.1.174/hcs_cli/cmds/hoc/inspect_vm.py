import click
import hcs_ext_hoc as hoc


@click.command()
@click.option("--org", required=True)
@click.option("--template", "-t", required=True)
@click.option("--vm", required=True)
def inspect_vm(org: str, template: str, vm: str):
    return hoc.inspect_vm(org, template, vm)
