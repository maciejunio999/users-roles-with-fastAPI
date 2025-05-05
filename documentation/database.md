# Database Models Documentation

This document describes the database schema used in the application. It is based on SQLAlchemy ORM and defines the relationships between core entities: users, roles, pilots, modules, endpoints, and products.

---

## Association Tables

### `user_role_association`

* Links users with roles (many-to-many).
* Columns:

  * `user_id`: Foreign key to `users.id`
  * `role_id`: Foreign key to `roles.id`

### `user_pilot_association`

* Links users with pilots (many-to-many).
* Columns:

  * `user_id`: Foreign key to `users.id`
  * `pilot_id`: Foreign key to `pilots.id`

### `user_product_association`

* Links users with products (many-to-many).
* Columns:

  * `user_id`: Foreign key to `users.id`
  * `product_id`: Foreign key to `products.id`

### `role_pilot_association`

* Links roles with pilots (many-to-many).
* Columns:

  * `pilot_id`: Foreign key to `pilots.id`
  * `role_id`: Foreign key to `roles.id`

### `module_role_association`

* Links modules with roles (many-to-many).
* Columns:

  * `module_id`: Foreign key to `modules.id`
  * `role_id`: Foreign key to `roles.id`

### `module_pilot_association`

* Links modules with pilots (many-to-many).
* Columns:

  * `module_id`: Foreign key to `modules.id`
  * `pilot_id`: Foreign key to `pilots.id`

### `module_endpoint_association`

* Links modules with endpoints (many-to-many).
* Columns:

  * `module_id`: Foreign key to `modules.id`
  * `endpoint_id`: Foreign key to `endpoints.id`

### `role_endpoint_association`

* Links roles with endpoints (many-to-many).
* Columns:

  * `endpoint_id`: Foreign key to `endpoints.id`
  * `role_id`: Foreign key to `roles.id`

---

## Tables

### `User`

* Represents application users.
* Columns:

  * `id`: Primary key
  * `username`: Unique, not nullable
  * `email`: Unique, not nullable
  * `password`: Hashed password
* Relationships:

  * `roles`: Many-to-many with `Role`
  * `pilots`: Many-to-many with `Pilot`
  * `products`: Many-to-many with `Product`

### `Role`

* Represents a user role/permission.
* Columns:

  * `id`: Primary key
  * `name`: Unique, not nullable
  * `code`: Unique code, not nullable
  * `description`: Textual description
* Relationships:

  * `users`: Many-to-many with `User`
  * `pilots`: Many-to-many with `Pilot`
  * `endpoints`: Many-to-many with `Endpoint`

### `Pilot`

* Represents a configuration pilot.
* Columns:

  * `id`: Primary key
  * `name`: Unique, not nullable
  * `code`: Unique, not nullable
  * `description`: Textual description
  * `state`: Boolean flag (active/inactive)
* Relationships:

  * `roles`: Many-to-many with `Role`
  * `users`: Many-to-many with `User`
  * `modules`: Many-to-many with `Module`

### `Module`

* Represents a functional module.
* Columns:

  * `id`: Primary key
  * `name`: Unique, not nullable
  * `description`: Textual description
  * `in_config`: Boolean (included in configuration)
* Relationships:

  * `pilots`: Many-to-many with `Pilot`
  * `endpoints`: Many-to-many with `Endpoint`

### `Endpoint`

* Represents a backend endpoint.
* Columns:

  * `id`: Primary key
  * `name`: Unique, not nullable
  * `url`: Unique, not nullable
  * `description`: Textual description
  * `http_method`: Request method with allowed values: `_None`, `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
* Relationships:

  * `modules`: Many-to-many with `Module`
  * `roles`: Many-to-many with `Role`

### `Product`

* Represents a product entity.
* Columns:

  * `id`: Primary key
  * `name`: Unique, not nullable
  * `description`: Textual description
  * `state`: Boolean (active/inactive)
* Relationships:

  * `users`: Many-to-many with `User`

---

> **Note:** All cascading relationships use `cascade="all, delete"`, ensuring related records are cleaned appropriately when parent entities are deleted.
s