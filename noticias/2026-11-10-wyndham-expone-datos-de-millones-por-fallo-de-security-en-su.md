---
titulo: "Wyndham Expone Datos de Millones por Fallo de Security en su App Android"
fecha: 2026-11-10
keyword: security
---

# Wyndham Expone Datos de Millones por Fallo de Security en su App Android

*Un fallo crítico de security en la aplicación Android del gigante hotelero Wyndham permitió el acceso a una base de datos interna con información personal de millones de clientes, según un informe exclusivo de TechCrunch, resaltando la importancia de robustas prácticas de ciberseguridad.*

## Vulnerabilidad Crítica de Security Descubierta

El gigante hotelero y de resorts Wyndham International ha confirmado un incidente de ciberseguridad después de que un investigador de seguridad descubriera una vulnerabilidad significativa. Robert Wiggins, de What Security, reveló a TechCrunch que encontró una contraseña incrustada directamente en el código fuente de la aplicación Android de Wyndham. Esta credencial permitía el acceso a una base de datos interna de la compañía, alojada por Salesforce, que contenía datos personales sensibles de los clientes.

Entre la información expuesta se encontraban nombres de clientes, direcciones de correo electrónico, números de miembro de Wyndham Rewards y tokens de inicio de sesión (JWTs) que mantienen a los usuarios conectados a sus aplicaciones. La base de datos también albergaba archivos y documentos internos de Wyndham. Wiggins estimó que la base de datos contenía millones de entradas, aunque no pudo determinar el número exacto de registros de clientes afectados. Cabe destacar que Wyndham cuenta con aproximadamente 129 millones de miembros inscritos en su programa de recompensas.

La práctica de "hardcoding" o incrustar contraseñas o credenciales directamente en el software público es un riesgo de security muy conocido en el desarrollo de aplicaciones. Este método permite que cualquier persona con acceso al código extraiga la contraseña y la utilice para acceder a servidores o bases de datos asociadas, lo que a menudo resulta en una calificación de severidad máxima para la vulnerabilidad. La facilidad con la que herramientas de inteligencia artificial pueden rastrear miles de líneas de código descompilado, como las utilizadas por Wiggins, hace que este tipo de debilidades de security sean más fáciles de detectar.

## La Respuesta de Wyndham y los Desafíos en Ciberseguridad

Según el relato de Wiggins a TechCrunch, la compañía no disponía de un canal claro para reportar fallos de seguridad, lo que lo llevó a buscar la ayuda del medio para alertar a Wyndham. Poco después de que TechCrunch contactara al personal de ciberseguridad de Wyndham, la credencial expuesta fue revocada, bloqueando el acceso posterior a la base de datos. Un portavoz de Wyndham declaró a TechCrunch que "nuestro equipo ha tomado medidas para abordar el problema" y que "nuestros equipos de security no tienen evidencia de ningún acceso no autorizado", sin ofrecer más detalles sobre esta última afirmación.

Consultado sobre la capacidad de la empresa para detectar accesos previos a la base de datos (por ejemplo, mediante registros de servidor), Wyndham se negó a responder. Tampoco quiso confirmar si tenía previsto notificar a los clientes afectados o informar del incidente a reguladores estadounidenses como la Comisión de Bolsa y Valores (SEC), requisito para las empresas públicas en casos de incidentes de ciberseguridad materiales. La duración de la contraseña incrustada en la aplicación y los planes para una solución a largo plazo también quedaron sin respuesta.

Wiggins, quien recientemente descubrió una vulnerabilidad casi idéntica en la aplicación de Applebee's, expresó su satisfacción por la corrección del problema. Sin embargo, también manifestó preocupación por la falta de visibilidad sobre la actividad pasada, lo que deja abierta la posibilidad de que actores maliciosos pudieran haber accedido y filtrado grandes cantidades de información personal. La compañía tampoco quiso confirmar si establecería un programa de divulgación de vulnerabilidades para que investigadores externos puedan reportar problemas de [security](https://tecno.ar/2026-11-10-jensen-huang-de-nvidia-en-el-ojo-de-la-tormenta-firma-de-cri) de forma privada. Michael Francess, director de ciberseguridad de Wyndham, indicó que los investigadores pueden enviar correos a [email protected] con detalles sobre posibles problemas de [security](https://tecno.ar/2026-11-10-anthropic-avanza-con-su-opi-pese-a-la-volatilidad-del-mercad).

## Un Historial y las Implicaciones para la Security de Datos

Este incidente no es el primero para Wyndham en los últimos años. En 2024, otro investigador de [security](https://tecno.ar/2026-11-09-francia-acusa-a-iran-de-ciberataques-masivos-a-congeladores-) descubrió que varios mostradores de check-in de hoteles Wyndham utilizaban software espía de acceso remoto que filtraba capturas de pantalla de los registros de los huéspedes. Este patrón subraya la importancia crítica de la inversión continua en infraestructura de protección de datos y en programas proactivos de detección y reporte de vulnerabilidades.

La persistencia de este tipo de fallos, especialmente en empresas con una base de usuarios tan masiva, pone de manifiesto la necesidad de una vigilancia constante en el desarrollo de software y una cultura organizacional que priorice la ciberseguridad. La falta de transparencia por parte de Wyndham en ciertos aspectos, como la notificación a los usuarios y reguladores, y la implementación de un programa de divulgación de vulnerabilidades, plantea preguntas sobre su compromiso con la protección de datos a largo plazo. En un panorama donde las amenazas cibernéticas son cada vez más sofisticadas, garantizar la robustez de la [security](https://techcrunch.com/2026/11/09/hotel-giant-wyndham-exposed-customer-data-after-app-security-lapse/) de los sistemas es fundamental para la confianza del consumidor y el cumplimiento normativo. La colaboración con expertos en [seguridad informática](https://tecno.ar/2026-11-09-francia-acusa-a-iran-de-ciberataques-masivos-a-congeladores-) y la implementación de mejores prácticas son pasos cruciales para evitar futuras exposiciones.

## Fuentes
TechCrunch - https://techcrunch.com/2026/11/09/hotel-giant-wyndham-exposed-customer-data-after-app-security-lapse/
