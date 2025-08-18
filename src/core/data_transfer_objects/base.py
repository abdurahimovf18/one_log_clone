from typing import Self

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
	
	@classmethod
	def construct_from_dto(cls: type[Self], other: "BaseDTO") -> Self:
		"""
		Create a new instance of the current DTO type from another DTO.

		This method is a convenience wrapper around:
			cls.model_construct(**other.model_dump())

		It is primarily intended for cases where two DTOs share overlapping
		fields (e.g., API → domain DTO, input DTO → output DTO). Instead of
		manually calling `.model_dump()` on one DTO and passing the result
		to another, this method makes the conversion more concise and
		explicit.

		### Why use this instead of direct instantiation?
		- **Clarity**: Explicitly signals that one DTO is being created from another.
		- **Less boilerplate**: Avoids repeating `cls.model_construct(**dto.model_dump())`.
		- **Consistency**: Standardizes cross-DTO conversion patterns across the codebase.

		### Example
		```python
		class UserInDTO(BaseDTO):
			username: str
			password: str

		class UserOutDTO(BaseDTO):
			username: str

		user_in = UserInDTO(username="alice", password="secret")

		# Convert safely between DTO types
		user_out = UserOutDTO.construct_from_dto(user_in)
		# -> UserOutDTO(username="alice")
		```

		Args:
			other (BaseDTO): The source DTO instance.

		Returns:
			Self: A new instance of the current DTO type populated with values
			from the given DTO.
		"""
		return cls.model_construct(**other.model_dump())
