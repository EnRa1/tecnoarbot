---
titulo: "Hugging Face Confirma Brecha de Seguridad que Afectó sus Datasets Internos y Credenciales"
fecha: 2026-07-20
keyword: datasets
---

# Hugging Face Confirma Brecha de Seguridad que Afectó sus Datasets Internos y Credenciales

*La plataforma Hugging Face, un hub clave para modelos e investigación de IA, ha revelado una brecha de seguridad que comprometió sus **datasets** internos y credenciales de servicio, impulsando una serie de acciones preventivas para usuarios y una investigación exhaustiva.*

La reconocida plataforma Hugging Face, fundamental en el ecosistema de la inteligencia artificial por alojar miles de modelos y **datasets**, ha confirmado un ciberataque que comprometió sus **datasets** internos y credenciales de servicio. La compañía hizo pública la intrusión la semana pasada, aunque la investigación para determinar si datos de clientes o socios fueron afectados aún se encuentra en curso.

Según el comunicado de la empresa, el incidente se originó a partir de un **dataset** subido a su plataforma. Este **dataset** aprovechó una vulnerabilidad de seguridad para ejecutar código malicioso en los servidores de Hugging Face. El ataque permitió a los intrusos escalar sus permisos y obtener un acceso más amplio a los sistemas internos de la plataforma. Como respuesta inmediata, Hugging Face revocó y rotó las credenciales robadas y ha instado a sus usuarios a que realicen la misma acción con cualquier clave almacenada en la plataforma, además de revisar sus cuentas en busca de actividad sospechosa. La vulnerabilidad que fue explotada durante el ciberataque ya ha sido subsanada, informó la compañía.

## Mecanismo del Ataque y la Explotación de Datasets

El modus operandi de los atacantes, según la descripción de Hugging Face, implicó el uso de lo que denominaron un "agente de IA externo". Este agente ejecutó "miles de acciones individuales a través de un enjambre de entornos aislados de corta duración", con un sistema de comando y control que se autotransfería en servicios públicos. No obstante, al ser consultado por TechCrunch, la compañía no proporcionó evidencia inmediata para respaldar esta afirmación. Este tipo de incidentes subraya el desafío particular que enfrentan empresas como Hugging Face, donde la propia infraestructura y los **datasets** compartidos pueden ser utilizados como vector de ataque para acceder a información sensible desde el interior.

## La IA en la Detección de Incidentes y los Límites de los Datasets Avanzados

Curiosamente, la propia Hugging Face detectó el ataque gracias a su sistema de detección de anomalías. Para el análisis de los registros del servidor que documentaron el ciberataque, la empresa utilizó un modelo de IA. Inicialmente, intentaron emplear un modelo de IA de frontera de un proveedor comercial, cuya identidad no fue revelada. Sin embargo, este esfuerzo de análisis se vio obstaculizado por las "guardrails" o restricciones impuestas por el proveedor. Ante esta situación, Hugging Face optó por utilizar su propio modelo de lenguaje grande (LLM) local, lo que, según afirmaron, ofreció el beneficio adicional de no tener que subir registros de ataques sensibles a los servidores de una empresa de IA externa.

Investigadores de seguridad han manifestado previamente su preocupación por las fuertes restricciones de algunos modelos de IA de frontera, como los Mythos y Fable de Anthropic, que limitan la capacidad de los defensores para indagar sobre asuntos relacionados con la ciberseguridad, incluyendo la defensa y la investigación. Incluso, Anthropic se vio obligada a retirar Fable del uso público después de que el gobierno de EE. UU. impusiera controles de exportación sobre el modelo, citando temores sobre su potencial uso en ciberataques ofensivos. La complejidad de gestionar grandes volúmenes de [datasets](https://techcrunch.com/2026/07/20/hugging-face-confirms-breach-affected-internal-datasets-and-credentials-urges-users-to-take-action/) y modelos en un entorno abierto, a la vez que se mantiene la seguridad, representa un desafío creciente para la industria.

Hugging Face ha comunicado el incidente a las autoridades y ha contratado a especialistas forenses en ciberseguridad para llevar a cabo una investigación profunda de la brecha y revisar sus protocolos de seguridad. No se ha aclarado si la empresa había realizado una auditoría de seguridad de sus sistemas antes de su lanzamiento, y un portavoz de Hugging Face no respondió a una solicitud de comentarios por parte de TechCrunch. La constante evolución de las amenazas cibernéticas exige una vigilancia y una protección continuas, especialmente para plataformas que gestionan un volumen tan crítico de [datasets](https://techcrunch.com/2026/07/20/hugging-face-confirms-breach-affected-internal-datasets-and-credentials-urges-users-to-take-action/) como Hugging Face.

## Fuentes
TechCrunch - https://techcrunch.com/2026/07/20/hugging-face-confirms-breach-affected-internal-datasets-and-credentials-urges-users-to-take-action/
