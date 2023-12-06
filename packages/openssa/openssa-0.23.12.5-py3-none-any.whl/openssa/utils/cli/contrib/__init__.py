"""OpenSSA Contrib CLI."""


from collections.abc import Sequence

import click

from .ssa_prob_solver import openssa_contrib_ssa_prob_solver_cli


__all__: Sequence[str] = ('openssa_contrib_cli',)


@click.group(name='contrib',
             cls=click.Group,
             commands={'ssa-prob-solver': openssa_contrib_ssa_prob_solver_cli},
             invoke_without_command=False,
             no_args_is_help=True,
             subcommand_metavar='OPENSSA_SUB_COMMAND',
             chain=False,
             help='OpenSSA Contrib CLI >>>',
             epilog='^^^ OpenSSA Contrib CLI',
             short_help='OpenSSA Contrib CLI',
             options_metavar='[OPTIONS]',
             add_help_option=True,
             hidden=False,
             deprecated=False)
def openssa_contrib_cli():
    """Trigger OpenSSA Contrib Utilities from CLI."""
