# Descripción del Modelo de Datos (ER)

#### USERS

Tabla que almacena los datos de los usuarios.

- **id** (int, PK): Identificador único del usuario.
- **username** (string, Unique): Nombre de usuario.
- **email** (string, Unique): Correo electrónico del usuario.
- **password** (string): Contraseña en formato hash.
- **role** (enum): Rol del usuario (super_admin, admin, anonymous).
- **is_active** (boolean): Indica si el usuario está activo.
- **created_at** (timestamp): Fecha de creación.
- **updated_at** (timestamp): Última actualización.
- **created_by** (int, FK): Usuario que creó el registro.
- **updated_by** (int, FK): Usuario que actualizó el registro.
- **last_login** (timestamp): Última fecha de inicio de sesión.
- **token** (string): Token de sesión del usuario.

#### PRODUCTS

Tabla que almacena la información de los productos.

- **id** (int, PK): Identificador único del producto.
- **sku** (string, Unique): Código único del producto.
- **name** (string): Nombre del producto.
- **price** (decimal): Precio del producto.
- **brand** (string): Marca del producto.
- **category** (string): Categoría del producto.
- **stock** (int): Cantidad disponible en inventario.
- **short_description** (text): Descripción corta del producto.
- **long_description** (text): Descripción detallada del producto.
- **is_active** (boolean): Indica si el producto está activo.
- **created_at** (timestamp): Fecha de creación.
- **updated_at** (timestamp): Última actualización.
- **created_by** (int, FK): Usuario que creó el registro.
- **updated_by** (int, FK): Usuario que actualizó el registro.

#### PRODUCT_LOGS

Registro de cambios en productos realizados por administradores.

- **id** (int, PK): Identificador único.
- **product_id** (int, FK): Producto afectado.
- **admin_id** (int, FK): Administrador que realizó la acción.
- **action** (string): Tipo de acción (created, updated, deleted, activated, deactivated, stock_updated, price_updated).
- **changes** (json): Detalle de los cambios.
- **created_at** (timestamp): Fecha del cambio.

#### USER_LOGS

Registro de cambios en usuarios realizados por administradores.

- **id** (int, PK): Identificador único.
- **admin_id** (int, FK): Administrador que realizó la acción.
- **target_user_id** (int, FK): Usuario afectado.
- **action** (string): Tipo de acción (created, updated, deleted, activated, deactivated).
- **changes** (json): Detalle de los cambios.
- **created_at** (timestamp): Fecha del cambio.

#### PRODUCT_QUERIES

Registro de consultas realizadas por usuarios anónimos.

- **id** (int, PK): Identificador único.
- **product_id** (int, FK): Producto consultado.
- **anonymous_user_id** (int, nullable): ID de usuario anónimo si es rastreable.
- **queried_at** (timestamp): Fecha y hora de la consulta.

#### Diagrama ER
![alt text](ER_diagram.png)

# Descripción del Diagrama de Secuencia

#### 1. Consulta de Productos

1. **Paso 1**: Un usuario anónimo o administrador solicita la lista de productos a la API, con filtros opcionales por categoría, marca y precio.
2. **Paso 2**: La API consulta la base de datos para recuperar la lista de productos según los filtros aplicados.
3. **Paso 3**: La base de datos responde con la lista de productos disponibles.
4. **Paso 4**: La API devuelve la información al usuario.

#### 2. Consulta de Detalle de un Producto

1. **Paso 1**: Un usuario anónimo o administrador solicita el detalle de un producto específico a la API.
2. **Paso 2**: La API consulta la base de datos para recuperar los datos del producto solicitado.
3. **Paso 3**: La base de datos responde con la información del producto.
4. **Paso 4**: La API devuelve el detalle del producto al usuario.
5. **Paso 5**: Si el usuario es anónimo, la API registra la consulta en la tabla `PRODUCT_QUERIES`.

#### 3. Creación de Producto por un Administrador

1. **Paso 1**: Un administrador envía una solicitud `POST` a la API con los datos de un nuevo producto.
2. **Paso 2**: La API inserta el nuevo producto en la base de datos.
3. **Paso 3**: La base de datos confirma la creación del producto.
4. **Paso 4**: La API registra la acción en `PRODUCT_LOGS`.
5. **Paso 5**: La API envía una notificación a los otros administradores sobre la creación del nuevo producto.

#### 4. Actualización Completa de un Producto

1. **Paso 1**: Un administrador envía una solicitud `PUT` con los nuevos datos de un producto.
2. **Paso 2**: La API actualiza la información del producto en la base de datos.
3. **Paso 3**: La base de datos confirma la actualización.
4. **Paso 4**: La API registra los cambios en `PRODUCT_LOGS`.
5. **Paso 5**: La API envía una notificación a los otros administradores.

#### 5. Modificación de Estado, Stock o Precio

1. **Paso 1**: Un administrador envía una solicitud `PATCH` para activar/desactivar un producto, modificar su stock o actualizar el precio.
2. **Paso 2**: La API actualiza solo el campo correspondiente en la base de datos.
3. **Paso 3**: La base de datos confirma la actualización.
4. **Paso 4**: La API registra la acción en `PRODUCT_LOGS`.
5. **Paso 5**: La API envía una notificación a los otros administradores sobre el cambio.

#### 6. Gestión de Usuarios por un Super Administrador

1. **Paso 1**: Un super administrador envía una solicitud `POST` para crear un nuevo usuario.
2. **Paso 2**: La API guarda el usuario en la base de datos con la contraseña encriptada.
3. **Paso 3**: La base de datos confirma la creación.
4. **Paso 4**: La API registra la acción en `USER_LOGS`.

#### 7. Autenticación y Gestión de Sesiones

1. **Paso 1**: Un usuario envía credenciales para iniciar sesión (`POST /login`).
2. **Paso 2**: La API valida las credenciales en la base de datos.
3. **Paso 3**: Si son correctas, la API genera un token JWT con duración de 5 minutos y un refresh token de 8 horas.
4. **Paso 4**: La API devuelve los tokens al usuario.
5. **Paso 5**: Para renovar el token (`POST /refresh-token`), el usuario envía su refresh token.
6. **Paso 6**: La API valida el refresh token y genera un nuevo token JWT.
7. **Paso 7**: Para cerrar sesión (`POST /logout`), la API invalida el token del usuario.

#### 8. Recuperación de Contraseña

1. **Paso 1**: Un usuario solicita restablecer su contraseña (`POST /forgot-password`).
2. **Paso 2**: La API genera un token temporal y lo envía por correo.
3. **Paso 3**: El usuario usa el token para establecer una nueva contraseña (`POST /reset-password`).

#### 9. Consulta de Logs por Administradores

1. **Paso 1**: Un administrador solicita la lista de logs (`GET /logs`), filtrando por usuario, fecha o producto.
2. **Paso 2**: La API consulta la base de datos para recuperar los logs.
3. **Paso 3**: La base de datos devuelve los logs filtrados.
4. **Paso 4**: La API devuelve la información al administrador.

#### 10. Diagrama de secuencia
![alt text](secuencia_diagram.png)

# Arquitectura en Capas (Puertos y Adaptadores)

La arquitectura está organizada en **capas bien definidas**, siguiendo el patrón de **puertos y adaptadores** (también conocido como arquitectura hexagonal). Cada capa tiene una responsabilidad clara, lo que garantiza un diseño **desacoplado**, **escalable** y **fácil de mantener**.

---

#### 1. Dominio (Domain)

El **dominio** es el núcleo de la aplicación y contiene las **entidades de negocio** y las **reglas del negocio**. Aquí se definen las **dataclasses** que representan las entidades principales:

- **`Product`**:
  - Atributos: `id`, `name`, `price`, `is_active`.
  - Representa un producto en el sistema.

- **`User`**:
  - Atributos: `id`, `username`, `email`, `is_active`.
  - Representa un usuario del sistema.

- **`LogEntry`**:
  - Atributos: `id`, `action`, `timestamp`.
  - Registra las actividades importantes en el sistema, como cambios en productos o usuarios.

---

#### 2. Puertos (Ports)

Los **puertos** son **interfaces abstractas** que definen los **contratos** que deben cumplir las implementaciones concretas. Actúan como un punto de conexión entre el dominio y las capas externas.

- **`ProductRepository`**:
  - Métodos: `get_by_id`, `save`, `delete`.
  - Define cómo interactuar con los productos (obtener, guardar, eliminar).

- **`UserRepository`**:
  - Métodos: `get_by_id`, `save`, `delete`.
  - Define cómo interactuar con los usuarios.

- **`NotificationService`**:
  - Métodos: `send_email`.
  - Define cómo enviar notificaciones por correo electrónico.

- **`AuthService`**:
  - Métodos: `login`, `refresh`, `logout`, `validate_token`.
  - Define cómo manejar la autenticación y la gestión de sesiones.

---

#### 3. Capa de Aplicación (Application)

En esta capa se encuentran los **servicios de aplicación**, que implementan la lógica de negocio y actúan como intermediarios entre los **adaptadores primarios** (vistas) y los **adaptadores secundarios** (repositorios y servicios externos).

- **`ProductService`**:
  - Métodos: `get_product`, `create_product`, `delete_product`.
  - Implementa la lógica de negocio relacionada con los productos.

- **`UserService`**:
  - Métodos: `get_user`, `create_user`, `delete_user`.
  - Implementa la lógica de negocio relacionada con los usuarios.

- **`AuthServiceImpl`**:
  - Métodos: `login`, `refresh`, `logout`, `validate_token`.
  - Implementa la lógica de autenticación y gestión de tokens.

---

#### 4. Adaptadores Primarios (Primary Adapters)

Los **adaptadores primarios** son los puntos de entrada a la aplicación, como las **vistas de Django** y los **serializadores**. Su función es manejar las solicitudes HTTP y convertirlas en llamadas a los servicios de aplicación.

- **`ProductView`**:
  - Métodos: `get`, `post`, `delete`.
  - Maneja las solicitudes HTTP relacionadas con productos.

- **`UserView`**:
  - Métodos: `get`, `post`, `delete`.
  - Maneja las solicitudes HTTP relacionadas con usuarios.

- **`AuthView`**:
  - Métodos: `login`, `refresh`, `logout`.
  - Maneja las solicitudes HTTP relacionadas con la autenticación.

- **`ProductSerializer`**:
  - Métodos: `to_json`, `from_json`.
  - Convierte objetos `Product` a JSON y viceversa.

- **`UserSerializer`**:
  - Métodos: `to_json`, `from_json`.
  - Convierte objetos `User` a JSON y viceversa.

- **`AuthSerializer`**:
  - Métodos: `to_json`, `from_json`.
  - Convierte datos de autenticación a JSON y viceversa.

- **`urls.py`**:
  - Define las rutas de la aplicación (por ejemplo, `/product/`, `/user/`, `/auth/`).

---

#### 5. Adaptadores Secundarios (Secondary Adapters)

Los **adaptadores secundarios** son las implementaciones concretas de los puertos. Se encargan de interactuar con la **infraestructura externa**, como bases de datos o servicios de terceros.

- **`ProductRepositoryImpl`**:
  - Métodos: `get_by_id`, `save`, `delete`.
  - Implementa el repositorio de productos usando MySQL.

- **`UserRepositoryImpl`**:
  - Métodos: `get_by_id`, `save`, `delete`.
  - Implementa el repositorio de usuarios usando MySQL.

- **`EmailService`**:
  - Métodos: `send_email`.
  - Implementa el envío de correos electrónicos usando SMTP o AWS SES.

- **`JWTService`**:
  - Métodos: `login`, `refresh`, `logout`, `validate_token`.
  - Implementa la autenticación basada en tokens JWT.

---

#### 6. Infraestructura (Infrastructure)

La **infraestructura** incluye los componentes externos que la aplicación necesita para funcionar, como bases de datos y servicios de correo.

- **`models.py`**:
  - Define los modelos de Django (`ProductModel`, `UserModel`, `LogEntryModel`), que se mapean a las tablas de la base de datos.

- **`MySQL Database`**:
  - Almacena los datos de productos, usuarios y logs.

- **`AWS SES / SMTP`**:
  - Servicio externo para el envío de correos electrónicos.

---

#### Relaciones entre Componentes

1. **Dominio → Puertos**:
   - Las entidades del dominio (`Product`, `User`) implementan los puertos (`ProductRepository`, `UserRepository`), definiendo cómo interactuar con ellas.

2. **Puertos → Adaptadores Secundarios**:
   - Los puertos están implementados por los adaptadores secundarios (`ProductRepositoryImpl`, `UserRepositoryImpl`, `EmailService`, `JWTService`), que interactúan con la infraestructura.

3. **Adaptadores Primarios → Servicios de Aplicación**:
   - Las vistas (`ProductView`, `UserView`, `AuthView`) dependen de los servicios de aplicación (`ProductService`, `UserService`, `AuthServiceImpl`) para acceder a la lógica de negocio.

4. **Adaptadores Secundarios → Infraestructura**:
   - Los adaptadores secundarios interactúan con la infraestructura (MySQL, AWS SES/SMTP) para realizar operaciones concretas, como almacenar datos o enviar correos.

5. **URLs → Vistas**:
   - Las rutas definidas en `urls.py` redirigen las solicitudes HTTP a las vistas correspondientes.

---
#### Diagrama de Arquitectura
![alt text](Arq_diagram.png)

# Estructura de Archivos del Proyecto

```plaintext
    zebrandsAssignment/
    │── config/                           # Configuración global de Django
    │   ├── settings.py                    
    │   ├── urls.py                         
    │   ├── wsgi.py                         
    │   ├── asgi.py                         
    │   ├── __init__.py                      
    │
    │── domain/                            # Capa de Dominio (Entidades y Puertos)
    │   ├── entities/
    │   │   ├── product.py                   
    │   │   ├── user.py                      
    │   │   ├── log_entry.py                 
    │   │   ├── product_query.py             
    │   │   ├── __init__.py                    
    │   │
    │   ├── ports/                           # Interfaces Abstractas
    │   │   ├── product_repository.py        
    │   │   ├── user_repository.py           
    │   │   ├── notification_service.py      
    │   │   ├── auth_service.py              
    │   │   ├── __init__.py                    
    │
    │── application/                         
    │   ├── product_service.py               
    │   ├── user_service.py                  
    │   ├── auth_service.py                  
    │   ├── log_service.py                   
    │   ├── __init__.py                        
    │
    │── adapters/                            # Implementaciones de Puertos (Adaptadores)
    │   ├── primary/                          # Adaptadores Primarios (Interfaces de Entrada)
    │   │   ├── views/
    │   │   │   ├── product_view.py            
    │   │   │   ├── user_view.py               
    │   │   │   ├── auth_view.py               
    │   │   │   ├── log_view.py                
    │   │   │   ├── __init__.py                 
    │   │   │
    │   │   ├── serializers/
    │   │   │   ├── product_serializer.py      
    │   │   │   ├── user_serializer.py         
    │   │   │   ├── auth_serializer.py         
    │   │   │   ├── log_serializer.py          
    │   │   │   ├── __init__.py                 
    │   │   │
    │   │   ├── routers/
    │   │   │   ├── product_urls.py            
    │   │   │   ├── user_urls.py               
    │   │   │   ├── auth_urls.py               
    │   │   │   ├── log_urls.py                
    │   │   │   ├── __init__.py                
    │
    │   ├── secondary/                         # Adaptadores Secundarios (Interfaces de Salida)
    │   │   ├── repositories/
    │   │   │   ├── product_repository_impl.py  
    │   │   │   ├── user_repository_impl.py     
    │   │   │   ├── log_repository_impl.py      
    │   │   │   ├── __init__.py                 
    │   │   │
    │   │   ├── services/
    │   │   │   ├── email_service.py            
    │   │   │   ├── jwt_auth_service.py         
    │   │   │   ├── __init__.py                 
    │
    │── infrastructure/                        # Configuración de Infraestructura
    │   ├── database.py                         # Configuración de conexión a MySQL
    │   ├── email_config.py                     # Configuración de envío de correos (AWS SES / SMTP)
    │   ├── security.py                         # Configuración de JWT, autenticación
    │   ├── models.py                           # Modelos Django ORM
    │   ├── __init__.py                          
    │
    │── tests/                                  # Pruebas unitarias y de integración
    │   ├── test_product.py                      
    │   ├── test_user.py                         
    │   ├── test_auth.py                         
    │   ├── test_logs.py                         
    │   ├── __init__.py                          
    │
    │── manage.py                               
    │── requirements.txt                         
    │── Dockerfile                               
    │── docker-compose.yml                        
    │── README.md                                

```


# Configuración y Uso

### 1. Configuración en Entorno Local

#### 1. Clonar el Repositorio
```bash
 git clone https://github.com/tu_usuario/zebrands.git
 cd zebrands
```

#### 2. Crear y Activar un Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/macOS
venv\Scripts\activate  # En Windows
```

#### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### 4. Configurar Variables de Entorno
Renombra el archivo de ejemplo `.env.example` a `.env` y modifica las variables según tu configuración.
```bash
cp .env.example .env
```

Ejemplo de configuración en `.env`:
```
DJANGO_SECRET_KEY=tu_secreto
DJANGO_DEBUG=True
DATABASE_URL=mysql://usuario:password@localhost:3306/zebrands_db
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu_api_key_sendgrid
```

#### 5. Configurar la Base de Datos
Ejecuta las migraciones:
```bash
python manage.py migrate
```

Si deseas cargar datos de prueba:
```bash
python manage.py loaddata fixtures/fixtures.json
```

#### 6. Crear un Superusuario (Opcional)
```bash
python manage.py createsuperuser
```

#### 7. Iniciar el Servidor Local
```bash
python manage.py runserver
```
El servidor estará disponible en `http://127.0.0.1:8000/`.

---

### 2. Configuración con Docker

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu_usuario/zebrands.git
cd zebrands
```

#### 2. Crear el Archivo `.env`
```bash
cp .env.example .env
```
Modifica las variables de entorno según tu configuración.

#### 3. Construir y Levantar los Contenedores
```bash
docker-compose up --build
```
Esto iniciará los contenedores de **Django** y **MySQL**.

#### 4. Aplicar Migraciones y Cargar Fixtures
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py loaddata fixtures/fixtures.json
```

#### 5. Crear un Superusuario (Opcional)
```bash
docker-compose exec web python manage.py createsuperuser
```

#### 6. Acceder a la Aplicación
- API disponible en: `http://localhost:8000/`
- Panel de administración en: `http://localhost:8000/admin/`

Para detener los contenedores:
```bash
docker-compose down
```

---

### Endpoints Principales

| Método | Endpoint | Descripción |
|--------|---------|-------------|
| GET | `/api/products/` | Listar productos |
| GET | `/api/products/{id}/` | Obtener detalles de un producto |
| POST | `/api/products/` | Crear un producto (Admin) |
| PATCH | `/api/products/{id}/toggle_active/` | Activar/Desactivar producto |
| GET | `/api/logs/` | Ver registros de auditoría |

Para más detalles sobre los endpoints, visita `http://localhost:8000/swagger/`.

---

### Configuración de Correos con SendGrid
Si estás usando **SendGrid** para enviar correos electrónicos:

1. Crea una cuenta en [SendGrid](https://sendgrid.com/).
2. Obtén una **API Key** en la configuración de SendGrid.
3. Asegúrate de agregar la API Key en el archivo `.env`:
   ```
   EMAIL_HOST=smtp.sendgrid.net
   EMAIL_PORT=587
   EMAIL_HOST_USER=apikey
   EMAIL_HOST_PASSWORD=tu_api_key_sendgrid
   DEFAULT_FROM_EMAIL=correo_verificado@tudominio.com
   ```
4. Para probar el envío de emails:
   ```bash
   docker-compose exec web python manage.py shell
   >>> from django.core.mail import send_mail
   >>> send_mail('Asunto', 'Mensaje de prueba', 'tu_correo@dominio.com', ['destinatario@correo.com'])
   ```

---

## Troubleshooting

### Error: `gunicorn: executable file not found in $PATH`
Si ves este error al ejecutar `docker-compose up`, asegúrate de que `gunicorn` está en `requirements.txt` y vuelve a construir la imagen:
```bash
docker-compose build --no-cache
docker-compose up
```

### Error: `bind: address already in use` en MySQL
Si el puerto `3306` ya está en uso, detén cualquier proceso MySQL en tu máquina:
```bash
sudo systemctl stop mysql
```
Luego, reinicia los contenedores:
```bash
docker-compose down -v
docker-compose up --build
```

### Error: `No se pudo cargar el fixture`
Si los fixtures no se cargan correctamente, revisa si el archivo `fixtures/fixtures.json` existe y es válido:
```bash
cat fixtures/fixtures.json | jq .
```
Si hay un error, intenta exportar de nuevo los datos:
```bash
python manage.py dumpdata --natural-foreign --natural-primary --indent 2 -o fixtures/fixtures.json
```

