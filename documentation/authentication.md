# Authentication & Authorization

This section documents the authentication (JWT-based) and role-based authorization system used in the application.

## Token Generation (Login)

**Endpoint:** `POST /token`

**Request Body (Form Data):**

* `username` (str): User's username (email used internally).
* `password` (str): User's plaintext password.

**Behavior:**

* Validates user credentials.
* On success, generates a JWT access token containing the user's email and role codes.
* The token is valid for 30 minutes by default.

**Response Model:** `Token`

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

**Errors:**

* `404 Not Found`: If username or password is incorrect.

---

## Token Utility Functions (JWT\_token.py)

### `create_access_token(data: dict, expires_delta: timedelta | None)`

Generates a JWT token with expiration and custom payload.

* Adds `exp` claim to the payload.
* Encodes using `HS256` algorithm.

### `verify_token(token: str, credentials_exception)`

* Decodes token using `SECRET_KEY` and `HS256`.
* Extracts `sub` (email) and `roles`.
* Raises an HTTP 401 exception if invalid.

---

## OAuth2 Scheme

Defined using `OAuth2PasswordBearer`:

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

Used in `get_current_user()` to extract and verify token.

### `get_current_user(token)`

* Validates token.
* Returns parsed `TokenData` object (contains email and roles).

---

## Role-Based Access Control (RBAC)

Two decorators are available for enforcing access restrictions based on roles:

### `require_roles(*required_roles: str)`

* Ensures the user has **all** specified roles.
* Returns `403 Forbidden` if any required role is missing.

### `require_any_role(*allowed_roles: str)`

* Ensures the user has **at least one** of the allowed roles.
* Returns `403 Forbidden` if none match.

**Usage Example:**

```python
@router.get("/admin")
def read_admin_data(current_user: User = Depends(require_roles("admin"))):
    ...
```

---

## Security Notes

* Passwords are hashed using `passlib`.
* Tokens should be sent via the `Authorization: Bearer <token>` header.
* All protected routes must use `Depends(get_current_user)` or a role checker.
s