# VoicePet-PQRS

**Integrantes**

**Mariana Alcaraz Alvarez**


tengo 23 años, vivo en chigorodo antioquia voy por el cuarto semestre de ingenieria industrial, me considero una persona responsable, comprometida, proactiva y me gusta trabajar en equipo.  




**VoicePet Gestor De PQRS**
<img width="1024" height="559" alt="WhatsApp Image 2026-10-13 at 8 14 33 PM" src="https://github.com/user-attachments/assets/bd913269-27ed-4b03-8ea1-dc0e87482451" />

**Descripcion**

este proyecto consiste en el Movimiento Estudiantil de Perritos y Gaticos de los estudiantes de la UdeA que gestiona la atención veterinaria para perros y gatos mediante la recepción de PQRS, su nombre cosiste en la voz de los animalitos con las siglas de PQRS, con el fin de hacer un trabajo mas eficiente al momento de recibir cada una de las solicitudes y que sean atendidas en el menor tiempo posible. 

**licencia del software**

<a href="https://github.com/marianaalcaraz-rgb/VoicePet-PQRS"><font dir="auto" style="vertical-align: inherit;"><font dir="auto" style="vertical-align: inherit;">VoicePet PQRS</font></font></a><font dir="auto" style="vertical-align: inherit;"><font dir="auto" style="vertical-align: inherit;"> © 2026 por </font></font><a href="https://ejemplo.com"><font dir="auto" style="vertical-align: inherit;"><font dir="auto" style="vertical-align: inherit;">movimiento estudiantil</font></font></a><font dir="auto" style="vertical-align: inherit;"><font dir="auto" style="vertical-align: inherit;"> tiene licencia </font></font><a href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><font dir="auto" style="vertical-align: inherit;"><font dir="auto" style="vertical-align: inherit;">CC BY-NC-SA 4.0</font></font></a><img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/nc.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/sa.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;">

**Visión Del Proyecto**

**Descripcion General Del Software** 

VoicePet es un sistema de gestión de consola, desarrollado en Python, donde permita gestionar documentos PQRS, centralizado y automatizado diseñado para el Movimiento Estudiantil de Perritos y Gaticos (MEPEGA) de la Universidad de Antioquia. Este sistema reemplaza el registro tradicional en papel por una solución digital que unifica la gestión de PQRS (Peticiones, Quejas, Reclamos y Sugerencias) recibidas a través de diversos canales. VoicePet organiza la atención de servicios veterinarios para perros y gatos mediante la asignación automática de radicados únicos, el control riguroso de tiempos de respuesta y la generación de métricas analíticas de gestión. 

**Objetivos del Sistema**

Digitalizar y optimizar el flujo de trabajo de registro, seguimiento y resolución de PQRS en MEPEGA para garantizar una atención veterinaria ágil, transparente y oportuna para perros y gatos en la UdeA.

*Estandarizar el registro: Asignar a cada solicitud un número de radicado propio, único, consecutivo e independiente, evitando la duplicidad de registros.   

*Garantizar el cumplimiento de plazos: Implementar un control temporal automático que fije el plazo máximo de 30 días calendario para dar respuesta a cada PQRS y emita alertas oportunas sobre documentos próximos a vencer.   

*Proveer herramientas analíticas: Ofrecer un motor de consulta y reporte de estadísticas en tiempo real sobre los registros activos, distribuidos por tipo de documento y por especie (perros y gatos).


**Beneficios**


*Para el equipo gestor (Estudiantes de MEPEGA):

Eliminación del error humano asociado al registro manual en papel y lápiz.   
Búsqueda instantánea de registros activos y visibilidad inmediata de la PQRS más antigua.   
Alertas automáticas sobre el estado de vencimiento de las solicitudes.  

*Para los usuarios y peticionarios:

Emisión de comprobantes (fichos) transparentes con la fecha límite exacta de respuesta (30 días).   
Trazabilidad clara sobre las solicitudes presentadas para sus mascotas.  

*Para el servicio de bienestar animal (Perros y Gatos):

Priorización efectiva de casos veterinarios pendientes, evitando el traspaso o la pérdida de solicitudes. 

**Requisitos Funcionales**


Registro de PQRS: El sistema debe permitir el registro de Peticiones, Quejas, Reclamos y Sugerencias, solicitando la información particular de la solicitud y discriminando el tipo de animal atendiéndose (perro o gato).   

Asignación de Radicado Único: El sistema debe generar de forma automática un número de radicado consecutivo, único e independiente para cada documento, garantizando la ausencia de números repetidos.   

Cálculo de Fecha Límite de Respuesta: El sistema debe calcular automáticamente el plazo máximo de respuesta de 30 días calendario a partir del momento de la radicación de la PQRS.   

Consulta de Registros Activos: El sistema debe permitir consultar las PQRS activas que están actualmente en proceso de gestión. 


**Requisitos No Funcionales**

Los requisitos no funcionales definen los criterios de calidad, rendimiento y operación del software VoicePet.   

Independencia de Almacenamiento (Fiabilidad): Cada documento debe ser almacenado de manera independiente con su propia estructura de datos particular, evitando consolidarlos en un mismo repositorio unificado.   

Usabilidad e Identidad Visual: La interfaz de usuario debe ser intuitiva, amigable para los estudiantes encargados y reflejar la nueva identidad visual incluyendo el logo oficial de VoicePet.   

Control de Versiones y Despliegue: El código del proyecto debe gestionarse de forma centralizada a través de un repositorio en GitHub bajo la administración del líder de equipo.   

Integridad de Datos: El algoritmo de generación de consecutivo debe garantizar la consistencia atómica para evitar la duplicación de radicados incluso durante registros concurrentes.   

Mantenibilidad: La arquitectura del código debe estar dividida modularmente de forma que se facilite el mantenimiento por parte de los miembros del equipo de desarrollo.



