## Exception Raising Rules

Exception handling in this application is divided into two clear categories: **Business Logic Exceptions** and **Developer Logic Exceptions**. This separation ensures both clarity in debugging and proper security guarantees in production.

---

### Business Logic Exceptions

Business logic exceptions represent expected errors that occur due to user actions, invalid requests, or service-level conditions. These exceptions:

* Are defined in `src.core.exceptions`.
* Replace Python’s or framework’s default exceptions, so that errors always reflect **user actions** or **domain-driven decisions**.
* Contain little to no free-text error messages. If they include text, it is a **fixed, predefined string** to avoid leaking sensitive details.
* Are intended to be safely exposed to users or external services.

**Examples:**

* Trying to delete a record that does not exist.
* Submitting a request that violates business rules.

---

### Developer Logic Exceptions

Developer logic exceptions represent **bugs or missed cases** in implementation that should never occur at runtime if the system is correctly designed. These exceptions:

* Are raised using `src.core.exceptions.common.Development`.
* Must always include descriptive arguments to explain **what assumption was broken**.
* Indicate issues that arise due to the complexity of domain-driven design (DDD) models, type mismatches, or overlooked invariants.
* Should be caught during **unit tests, integration tests, or QA**, not during real production runtime.

If a `Development` exception is raised in production, it signals a **bug in the system** that requires immediate developer attention.

**Examples:**

* A branch in code that should be unreachable is executed.
* A DTO field type mismatch occurs despite schema guarantees.
* An internal invariant assumed by the domain model is violated.

---

### Summary of Rules

* **Business Logic Exceptions** → predictable, safe, user-driven, never leak sensitive data.
* **Developer Logic Exceptions** → unpredictable, bug-driven, descriptive, must be eliminated before production.

This clear boundary ensures that the system:

1. Provides a secure, predictable interface to end-users.
2. Helps developers quickly detect and fix logic flaws caused by DDD complexity.


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
