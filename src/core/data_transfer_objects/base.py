from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """
    Base Data Transfer Object (DTO) model for the application.

    This class serves as the foundational Pydantic model from which
    all other DTOs in the application should inherit. It centralizes
    common model settings to ensure consistency across the entire
    codebase.

    Model Configuration:
    - `from_attributes=True`: Allows model initialization from object attributes,
      enabling easy conversion from ORM models or other objects.
    - `extra="forbid"`: Disallows extra fields not explicitly defined in the model,
      preventing accidental data pollution or unexpected keys.

    Usage:
        class UserDTO(BaseDTO):
            id: int
            name: str

        user = UserDTO(id=1, name='Alice')

    By inheriting from BaseDTO, all DTOs automatically adopt these settings,
    reducing boilerplate and enforcing strict validation rules application-wide.
    """

    model_config = ConfigDict(
        # Enables population of model fields from attribute access,
        # useful when converting from ORM or other classes.
        from_attributes=True,

        # Forbids extra fields that are not declared in the model schema,
        # raising validation errors if unknown fields are passed.
        extra="forbid"
    )
