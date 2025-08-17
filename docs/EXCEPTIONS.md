## Exception Raising Rules

Exception handling in this application distinguishes between **business logic exceptions** (user/service errors) and **developer logic exceptions** (bugs that should never happen at runtime). This separation ensures that the system:

* Communicates clearly when a real-world, user-facing error occurs.
* Guards against silent failures or unnoticed bugs during development.
* Maximizes runtime performance by avoiding unnecessary validations.

---

### 1. Business Logic Exceptions

Business logic exceptions represent real, user- or service-facing conditions that *can actually occur at runtime*. These should be raised using **custom exception classes**.

**Example:**

```python
class User(BaseDTO):
    is_validated: bool = Field(default=False)

user = User(is_validated=False)

if not user.is_validated:
    raise UserNotValidated()
```

This case is valid because `user.is_validated` depends on real input/state and can differ in production.

**Guidelines:**

* Raise exceptions when the system encounters conditions caused by external factors (user input, missing data, failed authorization, etc.).
* Always prefer **domain-specific exception classes** over generic ones.
* Provide enough context in the exception message for debugging/logging.

---

### 2. Developer Logic Exceptions (Assertions)

Some cases represent conditions that should *never occur* at runtime unless there is a **developer bug**. For these cases, use **assertions** instead of regular exceptions.

Assertions:

* Are checked only in debug/testing mode.
* Provide clarity on assumptions made by the developer.
* Avoid unnecessary overhead in production by skipping redundant runtime checks.

**Example:**

```python
class UserDomainSchema:
    type id = uuid.UUID
    type username = str


class UserUserNameResponseDTO(BaseDTO):
    username: UserDomainSchema.username


class UserOptionalDTO(BaseDTO):
    id: UserDomainSchema.id | None = None
    username: UserDomainSchema.username | None = None


def get_username(id: UserDomainSchema.id, session, ...) -> UserUserNameResponseDTO:
    ...

some_id = 1
user_with_username = get_username(id=some_id, session=session)

# Constructing domain object directly from response

domain_user = UserOptionalDTO.model_construct(**user_with_username.model_dump())

# This should always hold true by design
assert domain_user.username is not None, (
    f"User must have username, but got {domain_user.username}"
)
```

Here, `domain_user.username` being `None` would indicate a **bug** in `get_username` or schema design, not a runtime/user error.

**Guidelines:**

* Use `assert` only when the condition is guaranteed by design and should never fail unless the code is incorrect.
* Never use assertions for user input validation.
* Assertions should always include a descriptive message for debugging.

---

### 3. Performance Considerations

* Business logic exceptions: Checked and raised at runtime, since conditions are external and unpredictable.
* Assertions: Provide cheap, optional validation of invariants during development/testing.
* By separating the two, the system avoids redundant runtime checks while still ensuring developer bugs are caught early.

---

### 4. Summary of Rules

* **Business logic errors (runtime conditions):** Raise regular exceptions (preferably domain-specific).
* **Developer errors (should never happen):** Use `assert`.
* **Do not mix the two.**
* Ensure exception messages are clear, contextual, and useful for debugging.


## Application common exceptions

Target: This file documents various errors that may occur in the application and provides quick solutions.

---

**Exception:** `PydanticSchemaGenerationError`
**Description:** When using typing with Pydantic models, you may face unexpected errors if you use the schema class instead of its annotated field.
**Example:**

```python
class Schema:
    id = Annotated[int, Field()]

class User(BaseDTO):
    id: Schema  # ❌ should be Schema.id
```

**Solution:** Always use the specific annotated field from the schema (`Schema.id`) instead of the schema class itself.
