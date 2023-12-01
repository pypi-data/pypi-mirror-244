"""Code generated by Speakeasy (https://speakeasyapi.dev). DO NOT EDIT."""

from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from ionic import utils
from typing import List, Union


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class ValidationError:
    loc: List[Union[str, int]] = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('loc') }})
    msg: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('msg') }})
    type: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('type') }})
    

