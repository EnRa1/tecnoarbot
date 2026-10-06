---
titulo: "OpenAI Introducirá Marcas de Agua Invisibles en ChatGPT para la UE"
fecha: 2026-10-06
keyword: openai
---

# OpenAI Introducirá Marcas de Agua Invisibles en ChatGPT para la UE

*La tecnológica OpenAI ha anunciado que implementará un sistema de marcas de agua imperceptible en el texto generado por sus modelos ChatGPT y Codex en la Unión Europea, cumpliendo así con las nuevas normativas de transparencia de la Ley de IA de la UE.*

OpenAI, líder en inteligencia artificial, ha revelado sus planes para incorporar una marca de agua invisible en el contenido textual producido por sus populares modelos ChatGPT y Codex, específicamente para los usuarios en la Unión Europea. Esta medida, detallada en una publicación de blog, responde directamente a las reglas de transparencia de la Ley de IA de la UE, que entraron en vigor el pasado 2 de agosto y exigen que el contenido generado por IA sea identificable por otros sistemas.

La compañía detalló que esta característica se desplegará progresivamente en las próximas semanas para los usuarios elegibles de ChatGPT y Codex dentro de la UE, abarcando todos los planes. Para los desarrolladores que utilizan la API de OpenAI a nivel mundial, la función estará disponible a partir de hoy para modelos seleccionados, aunque por defecto permanecerá desactivada. Por el momento, OpenAI no tiene previsto convertir el marcado de texto en una opción global predeterminada. La marca de agua no es un símbolo visible; en cambio, opera al moldear sutilmente las elecciones de palabras del modelo, creando un patrón que es indetectable para el lector humano, pero que puede ser reconocido por un detector especializado. Al residir en el propio texto, la marca se conserva incluso cuando el contenido es copiado y pegado. OpenAI aseguró que este sistema no identifica al usuario y que no se observaron cambios significativos en el rendimiento de sus modelos con la función activada.

## Tecnología Detrás del Marcado de OpenAI

Junto con el anuncio, OpenAI publicó un informe técnico sobre su método, denominado "textGrain", coescrito con investigadores de la Universidad de Pensilvania y Yale. Este documento técnico explica cómo se utiliza una clave secreta para influir en las predicciones de la siguiente palabra, introduciendo cientos de "empujones" que, acumulados, permiten a un detector identificar el contenido generado por IA utilizando únicamente el texto y la clave.

No obstante, las pruebas realizadas por OpenAI sugieren que la marca de agua puede ser eliminada o al menos dificultada con la edición. Por ejemplo, al reemplazar el 10% de las palabras con sinónimos, la tasa de detección disminuyó de aproximadamente el 92% al 66%. La empresa también señaló que los pasajes cortos, las respuestas matemáticas y los textos traducidos presentan una mayor dificultad para la detección. Debido a estas limitaciones, OpenAI ha decidido restringir el acceso inicial al detector solo a investigadores aprobados y organizaciones expertas, quienes contribuirán a evaluar su fiabilidad y los usos responsables.

## El Compromiso de OpenAI con la Transparencia y Desafíos

La empresa enfatizó que la ausencia de una marca de agua en un texto no significa, de forma concluyente, que su autoría sea humana. El contenido podría ser demasiado breve, haber sido editado intensamente, o provenir de una IA de otra compañía. Las marcas de agua "pueden indicar que un sistema de OpenAI generó o procesó parte de un pasaje, pero no cuánto juicio humano, edición o creatividad se invirtió en él", aclaró la compañía.

Esta iniciativa de transparencia por parte de OpenAI se da en un contexto donde otras empresas ya han tomado medidas similares. Hace dos meses, Anthropic anunció que marcaría el texto generado por Claude a nivel mundial, una decisión que generó cierta controversia entre sus usuarios, quienes argumentaron que ellos aportaron las "instrucciones, contexto y decisiones", siendo Claude meramente "la herramienta". El compromiso de grandes tecnológicas, incluido [OpenAI](https://tecno.ar/2026-09-15-openai-google-y-anthropic-unen-fuerzas-en-conversaciones-cla), con el código de práctica de la UE sobre contenido generado por IA refleja una tendencia hacia una mayor responsabilidad en el sector.

Curiosamente, OpenAI ya había desarrollado un sistema de marca de agua similar en el pasado, pero se abstuvo de lanzarlo, en parte por la preocupación de que los usuarios pudieran migrar a plataformas rivales que no aplicaran este tipo de marcas, según un informe de The Wall Street Journal en 2024. Este nuevo paso de [OpenAI](https://techcrunch.com/2026/10/05/openai-will-start-watermarking-chatgpts-text-in-the-eu/) marca un giro significativo, impulsado por el marco regulatorio europeo.

## Fuentes
TechCrunch - https://techcrunch.com/2026/10/05/openai-will-start-watermarking-chatgpts-text-in-the-eu/
