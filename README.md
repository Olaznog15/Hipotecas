# Hipotecas API
Esta es una API RESTful construida con Flask que permite gestionar clientes y realizar simulaciones de hipotecas. Los datos se almacenan en una base de datos sqlite incluida en el proyecto.
La APi ha sido creada de forma sencilla por lo que las tablas de la base de datos no estan del todo bien preparadas para un despliegue grande.
Se ha incluido el uso de swagger para una explicación rapida de los metodos.
Se ha utilizado una funcion para validar el DNI mediante el algoritmo oficial. No es valido para otro tipo de documentos


## Descripción

La API proporciona funcionalidades para:
- Crear y gestionar clientes.
- Realizar simulaciones de hipotecas en función del TAE y el plazo.

## Endpoints

### `GET /Cliente`
**Descripción**: Permite OBTENER un cliente mediante DNI.  
**Parametros de la solicitud**:
''' ?DNI=12345678A '''


### `POST /Cliente`
**Descripción**: Permite REGISTRAR un cliente con los datos proporcionados.  
**Cuerpo de la solicitud**:
```json
{
  "DNI": "12345678A",
  "Nombre": "Juan Pérez",
  "Email": "juan.perez@example.com",
  "CapitalSolicitado": 100000
}'''

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

### `DELETE /Cliente`
**Descripción**: Permite ELIMINAR un cliente con el DNI proporcionados.  
**Cuerpo de la solicitud**:
```json
{
  "DNI": "12345678A"
}

### `GET /Simulacion`
**Descripción**: Permite OBTENER una simulacion de una hipoteca para un usuario en concreto.  
**Parametros de la solicitud**:
DNI: Dni con letra del cliente registrado en la BBDD
TAE: Tasa anual equivalente para el calculo de la hipoteca
PLAZO: Numero de años en los que se quiere financiar la hipoteca
Ejemplo:
''' Simulacion?DNI=12345678A&TAE=3.5&PLAZO=35


## Instalación





