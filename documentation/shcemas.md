## Schemas Documentation

### General

#### `AddById`

Used when referencing another resource by ID.

```json
{
  "id": 1
}
```

---

### Roles

#### `CreateRole`

```json
{
  "name": "Admin",
  "code": "ADMIN",
  "description": "Administrator role"
}
```

#### `ShowRole`

Extends `CreateRole` with `id`.

```json
{
  "id": 1,
  "name": "Admin",
  "code": "ADMIN",
  "description": "Administrator role"
}
```

#### `RoleCode`

```json
{
  "code": "ADMIN"
}
```

---

### Pilots

#### `CreatePilot`

```json
{
  "name": "PilotA",
  "code": "PILOT_A",
  "description": "Main pilot"
}
```

#### `ShowPilot`

Extends `CreatePilot` with `id` and `state`.

```json
{
  "id": 1,
  "name": "PilotA",
  "code": "PILOT_A",
  "description": "Main pilot",
  "state": true
}
```

#### `UpdatePilotState`

```json
{
  "state": false
}
```

---

### Modules

#### `CreateModule`

```json
{
  "name": "Module1",
  "description": "Test module"
}
```

#### `Module`

Extends `CreateModule` with `in_config`.

```json
{
  "name": "Module1",
  "description": "Test module",
  "in_config": true
}
```

#### `FullModule`

Extends `CreateModule` with `id` and `in_config`.

#### `ShowFullModule`

Extends `FullModule` and includes pilots.

---

### Endpoints

#### `CreateEndpoint`

```json
{
  "name": "GetUser",
  "url": "/user",
  "description": "Endpoint for getting user info"
}
```

#### `HttpMethod`

```json
{
  "http_method": "GET"
}
```

#### `ShowEndpoint`

Extends `CreateEndpoint` with `id` and `http_method`.

---

### Products

#### `CreateProduct`

```json
{
  "name": "ProductX",
  "description": "Enterprise license"
}
```

#### `ShowProduct`

Extends `CreateProduct` with `id` and `state`.

#### `UpdateProductState`

```json
{
  "state": true
}
```

---

### Users

#### `User`

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "securepass"
}
```

#### `ShowUser`

```json
{
  "username": "john",
  "email": "john@example.com"
}
```

#### `UserId`

Extends `ShowUser` with `id`.

#### `UserInDB`

Extends `User`, used internally for hashed password.

#### `Login`

```json
{
  "username": "john",
  "password": "securepass"
}
```

#### `Token`

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

#### `TokenData`

```json
{
  "email": "john@example.com",
  "roles": ["ADMIN", "USER"]
}
```

#### `UserRoles`

Extends `UserId` and includes a list of roles.

#### `UserPilots`

Extends `UserId` and includes a list of pilots.

---

### Nested / Full Representations

#### `RolePilots`

Extends `ShowRole` with `pilots` list.

#### `RoleUsers`

Extends `ShowRole` with `users` list.

#### `PilotRoles`

Extends `ShowPilot` with `roles` list.

#### `PilotUsers`

Extends `ShowPilot` with `users` list.

#### `EndpointRoles`

Extends `ShowEndpoint` with `roles` list.

#### `EndpointModules`

Extends `ShowEndpoint` with `modules` list.

#### `ShowFullUser`

Extends `ShowUser` with `roles` and `pilots`.

#### `ShowFullRole`

Extends `ShowRole` with `users` and `pilots`.

#### `ShowFullPilot`

Extends `ShowPilot` with `users` and `roles`.

#### `ShowFullEndpoint`

Extends `ShowEndpoint` with `modules` and `roles`.

#### `ShowFullProduct`

Extends `ShowProduct` with `users`.
