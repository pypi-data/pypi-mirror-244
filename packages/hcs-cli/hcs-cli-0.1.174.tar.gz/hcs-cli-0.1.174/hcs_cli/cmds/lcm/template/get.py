"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import click
from hcs_cli.service.lcm import template
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp.data_util import deep_get_attr


@click.command()
@click.argument("id", type=str, required=True)
@click.option(
    "--field",
    "-f",
    type=str,
    required=False,
    help="Optionally, retrieve specific field value. E.g. '-f sparePolicy.max'.",
)
@cli.org_id
def get(id: str, field: str, org: str, **kwargs):
    """Get template by ID"""
    org_id = cli.get_org_id(org)
    ret = template.get(id, org_id, **kwargs)
    if not ret:
        return None, 1

    if field:
        return deep_get_attr(ret, field)
    return ret
