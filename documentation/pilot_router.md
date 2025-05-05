# Pilot Router Documentation

## Overview

This module handles the management of "Pilots" including their creation, modification, activation, and relationships with roles and users.

---

## Endpoints

### BASIC

#### `GET /pilot/`

Returns a list of all pilots.

* **Response**: `List[ShowPilot]`

#### `GET /pilot/{id}`

Returns a single pilot by ID.

* **Response**: `ShowFullPilot`

#### `POST /pilot/`

Creates a new pilot.

* **Request**: `CreatePilot`
* **Response**: `ShowPilot`

#### `DELETE /pilot/{id}`

Deletes a pilot by ID.

* **Response**: `204 No Content`

#### `PUT /pilot/{id}`

Updates an existing pilot by ID.

* **Request**: `CreatePilot`
* **Response**: `ShowPilot`

---

### ACTIVATION

#### `PUT /pilot/activate/{id}`

Activates a pilot (sets `state = True`).

* **Response**: `ShowPilot`

#### `PUT /pilot/deactivate/{id}`

Deactivates a pilot (sets `state = False`).

* **Response**: `ShowPilot`

---

### ROLES

#### `GET /pilot/{id}/roles`

Returns roles assigned to a pilot.

* **Response**: `PilotRoles`

#### `PUT /pilot/{id}/add_role`

Adds a role to the pilot.

* **Request**: `AddById`
* **Response**: `PilotRoles`

#### `DELETE /pilot/{id}/remove_role`

Removes a role from the pilot.

* **Request**: `AddById`
* **Response**: `204 No Content`

---

### USERS

#### `GET /pilot/{id}/users`

Returns users assigned to a pilot.

* **Response**: `PilotUsers`

#### `PUT /pilot/{id}/add_user`

Adds a user to the pilot and assigns all roles from the pilot to the user if not already assigned.
s
* **Request**: `AddById`
* **Response**: `PilotUsers`

#### `DELETE /pilot/{id}/remove_user`

Removes a user from the pilot.

* **Request**: `AddById`
* **Response**: `204 No Content`

---

## Validation & Error Handling

* All endpoints return `404 Not Found` if the referenced pilot, role, or user does not exist.
* Duplicate checks are implemented for name/code during creation and updates.
* Relationships (e.g. user already assigned) are validated to prevent duplicates.

---

## Notes

* Pilot state is represented by a boolean `state` flag.
* Associations with users and roles are handled via many-to-many relationships.
* Security is enforced via `Depends(oauth2.get_current_user)` on protected routes.
s