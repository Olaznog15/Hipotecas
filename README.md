# Hipotecas API
Esta es una API RESTful construida con Flask que permite gestionar clientes y realizar simulaciones de hipotecas. Los datos se almacenan en una base de datos sqlite incluida en el proyecto.
La APi ha sido creada de forma sencilla por lo que las tablas de la base de datos no estan del todo bien preparadas para un despliegue grande.
Se ha incluido el uso de swagger para una explicación rapida de los metodos.
Se ha utilizado una funcion para validar el DNI mediante el algoritmo oficial. No es valido para otro tipo de documentos


## Descripción

La API proporciona funcionalidades para:
- Crear y gestionar clientes.
- Realizar simulaciones de hipotecas en función del TAE y el plazo.
- Puedes ver una pagina de presentacion en la ruta http://localhost:8086
- Puedes acceder a la documentacion Swagger en la ruta http://localhost:8086/swagger

## Endpoints

### `GET /Cliente`
**Descripción**: Permite OBTENER un cliente mediante DNI.  
**Parametros de la solicitud**:
```txt
?DNI=12345678A 
```

### `POST /Cliente`
**Descripción**: Permite REGISTRAR un cliente con los datos proporcionados.  
**Cuerpo de la solicitud**:
```json
{
  "DNI": "12345678A",
  "Nombre": "Juan Pérez",
  "Email": "juan.perez@example.com",
  "CapitalSolicitado": 100000
}
```
### `PUT /Cliente`
**Descripción**: Permite ACTUALIZAR un cliente con los datos proporcionados.  
**Cuerpo de la solicitud**:
```json
{
  "DNI": "12345678A",
  "Nombre": "Juan Pérez",
  "Email": "juan.perez@example.com",
  "CapitalSolicitado": 100000
}
```
### `DELETE /Cliente`
**Descripción**: Permite ELIMINAR un cliente con el DNI proporcionados.  
**Cuerpo de la solicitud**:
```json
{
  "DNI": "12345678A"
}
```
### `GET /Simulacion`
**Descripción**: Permite OBTENER una simulacion de una hipoteca para un usuario en concreto.  
**Parametros de la solicitud**:
DNI: Dni con letra del cliente registrado en la BBDD
TAE: Tasa anual equivalente para el calculo de la hipoteca
PLAZO: Numero de años en los que se quiere financiar la hipoteca
Ejemplo:
```txt
Simulacion?DNI=12345678A&TAE=3.5&PLAZO=35 
```

## Instalación
### Requisitos
- Python 3.x
- pip (gestor de paquetes de Python)
  
### Pasos:

#### 1. Clonar el repositorio o descargar el proyecto
Si aún no tienes el proyecto, clónalo o descárgalo en tu máquina.

#### 2. Crear un entorno virtual 
Ve a la carpeta del proyecto y Crea un entorno virtual con el siguiente comando:
```bash
python -m venv venv
```
o
```bash
python3 -m venv venv
```

#### 3. Activar el entorno virtual
En CMD Windows:
```bash
venv\Scripts\activate
```

En Powershell Windows:
```bash
.\venv\Scripts\activate
```

En Linux:
```bash
source venv/bin/activate
```

#### 4. Instalar las dependencias
Con el entorno virtual activado, instala todas las dependencias necesarias que están listadas en el archivo requirements.txt:
```bash
pip install -r requirements.txt
```


#### 5. Ejecutar la aplicación
Una vez instaladas las dependencias, ejecuta el archivo app.py para iniciar la API:
```bash
python app.py
```
Esto debería iniciar la API en http://localhost:8086 (o la IP y el puerto configurado en la aplicación).















