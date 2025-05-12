from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Literal


class NameInput(BaseModel):
    """
    Pydantic V2 model to validate Ukrainian name parts and gender.

    Attributes:
        parts: list of 1-3 name components (family, given, patronymic or '-' for skip).
        gender: 'masculine' or 'feminine'.
    """
    parts: List[str] = Field(
        ..., description="Name parts: family, given, patronymic; use '-' to skip a part"
    )
    gender: Literal['masculine', 'feminine'] = Field(
        ..., description="Gender: 'masculine' or 'feminine'"
    )

    @field_validator('parts', mode='before')
    def split_or_pass(cls, v): # noqa
        """
        Split a space-separated string into parts, or accept a list as is.
        """
        if isinstance(v, str):
            return v.strip().split()
        return v

    @field_validator('parts', mode='after')
    def validate_parts(cls, parts: List[str]) -> List[str]: # noqa
        """
        Ensure there are between 1 and 3 parts and validate each part's characters.
        Letters, hyphens, underscores, or skip marker '-' are allowed.
        """
        if not 1 <= len(parts) <= 3:
            raise ValueError(f'Exactly 1 to 3 name parts required, got {len(parts)}')
        new_parts: List[str] = []
        for part in parts:
            if part == '-':
                new_parts.append(part)
            elif all(ch.isalpha() or ch in '-_' for ch in part):
                new_parts.append(part)
            else:
                # Replace any invalid part with skip marker
                new_parts.append('-')
        return new_parts

    @model_validator(mode='after')
    def ensure_given_present(cls, model): # noqa
        """
        Ensure at least one non-skip part exists (given name requirement).
        """
        non_skip = [p for p in model.parts if p != '-']
        if len(non_skip) == 0:
            raise ValueError('Given name is required, use "-" only to skip a part')
        return model
