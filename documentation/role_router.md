# Roles Router Documentation

## Base Path

```
/role
```

## Tags

```
Roles
```

---

## Endpoints

### 1. Get All Roles

**GET** `/role/`

* **Description**: Returns a list of all roles.
* **Response**: `List[CreateRole]`
* **Status Code**: `200 OK`

---

### 2. Get Role by ID

**GET** `/role/{id}`

* **Description**: Get detailed information about a specific role.
* **Path Parameter**: `id: int` (Role ID)
* **Response**: `ShowFullRole`
* **Status Code**: `200 OK`

---

### 3. Create Role

**POST** `/role/`

* **Description**: Create a new role.
* **Request Body**: `CreateRole`
* **Response**: `CreateRole`
* **Authorization**: Requires logged-in user
* **Status Code**: `201 CREATED`

---

### 4. Update Role

**PUT** `/role/{id}`

* **Description**: Update an existing role.
* **Path Parameter**: `id: int`
* **Request Body**: `CreateRole`
* **Response**: `ShowFullRole`
* **Authorization**: Requires logged-in user
* **Status Code**: `202 ACCEPTED`

---

### 5. Delete Role

**DELETE** `/role/{id}`

* **Description**: Delete a role by ID.
* **Path Parameter**: `id: int`
* **Authorization**: Requires logged-in user
* **Status Code**: `204 NO CONTENT`

---

### 6. Get Users Assigned to Role

**GET** `/role/{id}/users`

* **Description**: Get a list of users assigned to a specific role.
* **Path Parameter**: `id: int`
* **Response**: `RoleUsers`
* **Authorization**: Requires logged-in user
* **Status Code**: `200 OK`

---

### 7. Add User to Role

**PUT** `/role/{id}/add_user`

* **Description**: Assign a user to a specific role.
* **Path Parameter**: `id: int`
* **Request Body**: `AddById` (contains `id` of user)
* **Response**: `ShowFullRole`
* **Authorization**: Requires logged-in user
* **Status Code**: `202 ACCEPTED`

---

### 8. Remove User from Role

**DELETE** `/role/{id}/remove_user`

* **Description**: Remove a user from a role.
* **Path Parameter**: `id: int`
* **Request Body**: `AddById` (contains `id` of user)
* **Authorization**: Requires logged-in user
* **Status Code**: `204 NO CONTENT`

---

### 9. Get Pilots Assigned to Role

**GET** `/role/{id}/pilots`

* **Description**: Get a list of pilots assigned to a specific role.
* **Path Parameter**: `id: int`
* **Response**: `RolePilots`
* **Authorization**: Requires logged-in user
* **Status Code**: `200 OK`

---

### 10. Add Pilot to Role

**PUT** `/role/{id}/add_pilot`

* **Description**: Assign a pilot to a specific role.
* **Path Parameter**: `id: int`
* **Request Body**: `AddById` (contains `id` of pilot)
* **Response**: `ShowFullRole`
* **Authorization**: Requires logged-in user
* **Status Code**: `202 ACCEPTED`

---

### 11. Remove Pilot from Role

**DELETE** `/role/{id}/remove_pilot`

* **Description**: Remove a pilot from a role.
* **Path Parameter**: `id: int`
* **Request Body**: `AddById` (contains `id` of pilot)
* **Authorization**: Requires logged-in user
* **Status Code**: `204 NO CONTENT`

---

## Notes

* Most endpoints require authentication via `oauth2.get_current_user`.
* Validation errors and integrity checks are handled with appropriate HTTP status codes and detailed messages.
* Role `code` and `name` must be unique.
* Pilot and User relationships are automatically managed with the role assignment/removal logic.
