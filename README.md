# 🚌 Proyecto SmartBus – Ing. Web Project

![Django](https://img.shields.io/badge/Django-5.2.x-092E20?style=flat&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat&logo=render)

## Gestión de ocupación y transferencias atómicas de pasajeros
Este proyecto implementa un sistema en Django para la administración de buses interprovinciales, gestionando:
- Horarios de salida
- Reserva de pasajeros
- Ocupación de buses
- Transferencia atómica de pasajeros entre buses
- Panel de administración para operadores

La lógica principal del proyecto gira en torno a optimizar la ocupación de buses, permitiendo mover pasajeros desde rutas con baja ocupación hacia otras más rentables, manteniendo **consistencia y seguridad transaccional**.
> **⚠️ Nota importante:**
Este repositorio contiene una versión inicial del sistema, con varios puntos por mejorar en estructura de carpetas, duplicación de código y separación de responsabilidades. Sin embargo, este README documenta fielmente el funcionamiento actual del proyecto.

---

## 🌐 Proyecto deployado en Render

Se puede ver y probar el proyecto en producción desde:

🔗 [https://ingwebcore.onrender.com](https://ingwebcore.onrender.com)

Este deployment incluye las principales funcionalidades del proyecto, listas para ser probadas:
- Dashboard para operadores
- Gestión de horarios y buses
- Reservas con asignación de asientos
- Transferencias atómicas
- Logs de transferencias
- Panel de administración de Django
> **Nota:** Render puede demorar unos segundos en iniciar si está en modo “cold start”.

---

## 🏗️ Arquitectura general del proyecto
El sistema está compuesto por tres aplicaciones principales:
```
smartbus/              → Configuración global (settings, urls, wsgi)
core/                  → Lógica de transferencias y procesos atómicos
administracion/        → Gestión de operadores, buses y horarios
reservas/              → Reservas de asientos y ocupación
```
### 1️⃣ 1. core/
Contiene la lógica crítica del sistema:
- **Servicios de transferencia atómica:**
    - Mueve pasajeros entre buses
    - Valida capacidad disponible
    - Verifica que el bus destino no haya salido
    - Garantiza integridad con ```transaction.atomic()```

- **TransferLog:**
Registro detallado de cada transferencia:
    - Quién la ejecutó
    - Capacidad antes/después
    - Lista de reservas afectadas
    - Resultado final

### 2️⃣ administracion/
Incluye la parte de gestión operativa:
- Modelos:
    - **Bus** (placa, capacidad)
    - **Operador** (autenticación)
    - **Ruta**
    - **Horario** (bus + ruta + fecha/hora)

- Formularios de edición
- Vistas para administración manual
- URLs propias
- Scripts de initial-seeding (como ```seed_real.py``` en la versión actual)

### 3️⃣ reservas/
Aquí se concentra la gestión de pasajeros:
- Modelo **Reserva**
- Validación de asientos ocupados
- Generación de reservas dummy
- Vistas de operaciones sobre asientos
- Scripts relacionados con pruebas y carga inicial

---

## 🔄 Flujo principal de transferencia de pasajeros
El proceso completo consiste en:
1. Selección de reservas pertenecientes a un horario (bus origen).
2. Selección de un horario destino con cupo disponible.
3. Validaciones aplicadas:
    - El bus destino aún no ha salido
    - No se mezclan horarios
    - No existen reservas previamente transferidas
    - Capacidad disponible suficiente
4. Asignación de nuevos asientos libres en el bus destino.
5. Persistencia en base de datos.
6. Registro en **TransferLog**.

Todo este flujo se ejecuta de manera atómica, evitando estados inconsistentes.

---

## 🧪 Scripts incluidos en el repositorio
El proyecto contiene algunos scripts para poblar la base de datos.
Ejemplo (dependiendo de tu versión actual):
- ```core/seed_real.py``` – Generación masiva de reservas y casos de prueba
- Scripts de creación de operadores
- Scripts para generar horarios

> Estos scripts son parte del código inicial y pueden estar dispersos o duplicados; sin embargo, son funcionales y se documentan aquí por transparencia.

---

## ⚙️ Instalación y ejecución
**Requisitos**
- Python 3.10+
- pip
- Entorno virtual recomendado
- Django (instalado automáticamente por requirements)

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/RFelipeGR/IngWebCore.git
cd IngWebCore
```
### 2️⃣ Crear y activar un entorno virtual
```bash
python -m venv env
source env/bin/activate        # Linux / Mac
env\Scripts\activate           # Windows
```
### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4️⃣ Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5️⃣ Cargar el servidor
```bash
python manage.py runserver
```

---

## 🧩 Endpoints principales
### Administración (/administracion/)
- Gestionar buses
- Gestionar rutas
- Gestionar horarios
- CRUD básico de operadores

### Reservas (/reservas/)
- Crear reservas
- Cargar reservas dummy
- Visualizar ocupación

### Transferencias (/core/)
- Ejecutar transferencia atómica
- Consultar logs de transferencia

---

## 🗃️ Estructura del modelo de datos (simplificado)
```
Bus
 ├─ placa
 └─ capacidad

Ruta
 └─ nombre

Horario
 ├─ bus (FK)
 ├─ ruta (FK)
 ├─ fecha_salida
 └─ estado

Reserva
 ├─ horario (FK)
 ├─ nombre_pasajero
 ├─ cedula
 └─ asiento

TransferLog
 ├─ origen (FK)
 ├─ destino (FK)
 ├─ operador (FK)
 ├─ reservas (lista)
 ├─ capacidad_origen/destino antes/después
 └─ estado + mensaje
```

---

## 🚨 Limitaciones y aspectos a mejorar
Este proyecto funciona, pero tiene áreas claras de mejora:

**1. Código duplicado**

Funciones para generar reservas, asignar asientos y operaciones de negocio se repiten en varias carpetas.

**2. Separación de responsabilidades deficiente**

Algunas vistas realizan lógica de negocio que debería estar en servicios.

**3. Scripts sueltos**

Scripts como seed_real.py deberían convertirse en management commands.

**4. Tests limitados**

Los tests actuales validan casos simples. Deben ampliarse para cubrir:
- Transferencias con horarios llenos
- Transferencias inválidas
- Concurrencia
- Validación de asiento repetido

**5. Validaciones débiles**

Se observan condiciones de borde no validadas o manejadas parcialmente.

---

## 🎯 Estado actual del sistema
A pesar de sus limitaciones, este backend cumple:
- Gestión funcional de buses y horarios
- Registro de pasajeros por horario
- Transferencia atómica con logs detallados
- Generación de datos de prueba
- Integración con Django Admin

Este README documenta con precisión la versión actual, permitiendo su uso y evaluación.

---

## ⭐ Contribuciones futuras sugeridas
- Re-estructurar ```services.py``` en cada app
- Unificar lógica de reservas (evitar duplicados)
- Crear comandos ```manage.py``` para seeding y mantenimiento
- Migrar a PostgreSQL para escalabilidad
- Tests unitarios + integración
- Normalizar estilos y eliminar código muerto

--- 

## 🎥 Video defensa del proyecto
En este video (grabado en clase) se pretende explicar:
- El funcionamiento general del sistema
- Cómo está estructurado el backend
- La lógica de transferencias atómicas (core)

[![Ver defensa del proyecto](https://img.youtube.com/vi/WKEVSXoFj_4/hqdefault.jpg)](https://www.youtube.com/watch?v=WKEVSXoFj_4)

--- 

## 🎥 Video reto propuesto
En este video se detalla la implementación del reto propuesto en clase:

[![Ver reto propuesto](https://img.youtube.com/vi/9qF8YaRhy70/hqdefault.jpg)](https://www.youtube.com/watch?v=9qF8YaRhy70)

---

## 👤 Autores

**Víctor A. Suquilanda** | **Roberto F. Guaña**  
📧 Carrera de Ing. Software | Proyecto Core MVC  
📅 Año: 2025    

---