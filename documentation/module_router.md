# Module Router Documentation

## Overview

This document describes the `/module` router in the FastAPI application. The module resource allows managing modules and their relationships with pilots.

---

## Prefix & Tags

* **Prefix:** `/module`
* **Tags:** `Modules`

---

## Endpoints

### Get All Modules

**GET** `/module/`

* **Description:** Returns a list of all modules.
* **Response:** `List[schemas.Module]`

### Get One Module

**GET** `/module/{id}`

* **Description:** Returns one module by its ID.
* **Params:** `id` - integer (module ID)
* **Response:** `schemas.ShowFullModule`

### Create Module

**POST** `/module/`

* **Description:** Creates a new module.
* **Body:** `schemas.CreateModule`
* **Response:** `schemas.Module`

### Delete Module

**DELETE** `/module/{id}`

* **Description:** Deletes a module by ID.
* **Authorization:** Requires logged-in user
* **Params:** `id`
* **Response:** No content (204)

### Update Module

**PUT** `/module/{id}`

* **Description:** Updates a module's information.
* **Authorization:** Requires logged-in user
* **Body:** `schemas.CreateModule`
* **Response:** `schemas.Module`

---

## Activation

### Activate Module

**PUT** `/module/activate/{id}`

* **Description:** Marks a module as active (`in_config = True`).
* **Authorization:** Requires logged-in user
* **Response:** `schemas.Module`

### Deactivate Module

**PUT** `/module/deactivate/{id}`

* **Description:** Marks a module as inactive (`in_config = False`).
* **Authorization:** Requires logged-in user
* **Response:** `schemas.Module`

---

## Pilots

### Get All Pilots in Module

**GET** `/module/{id}/pilots`

* **Description:** Returns full module info including all related pilots.
* **Authorization:** Requires logged-in user
* **Response:** `schemas.ShowFullModule`

### Get Active Pilots in Module

**GET** `/module/{id}/active_pilots`

* **Description:** Returns only active pilots linked to the module.
* **Authorization:** Requires logged-in user
* **Response:** `schemas.ShowFullModule`

### Add Pilot to Module

**PUT** `/module/{id}/add_pilot`

* **Description:** Assigns a pilot to a module.
* **Authorization:** Requires logged-in user
* **Body:** `schemas.AddById` (contains `pilot_id`)
* **Response:** `schemas.ShowFullModule`

### Remove Pilot from Module

**DELETE** `/module/{id}/remove_pilot`

* **Description:** Removes a pilot from a module.
* **Authorization:** Requires logged-in user
* **Body:** `schemas.AddById` (contains `pilot_id`)
* **Response:** `{ "details": "Pilot removed" }`

---

## Validation & Errors

* **404 NOT FOUND** if module, pilot, or data not found
* **400 BAD REQUEST** if duplicate module name or pilot already linked

---

## Models Used

* `schemas.CreateModule`
* `schemas.Module`
* `schemas.ShowFullModule`
* `schemas.PilotName`
* `schemas.AddById`

---

## Access Control

* Some endpoints (create, update, delete, activate, etc.) require authentication with `Depends(oauth2.get_current_user)`

---

Let me know if you'd like to include example requests or move on to the next router! 🚀
