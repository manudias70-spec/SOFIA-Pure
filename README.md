# SOFIA-Pure
### Emulación retro, herramientas propias e identidad independiente

**SOFIA-Pure** es un proyecto independiente y experimental derivado de **DOSBox Pure Unleashed**, la versión de escritorio de DOSBox Pure. Conserva como punto de partida la experiencia de emulación DOS y desarrolla modificaciones, herramientas y una interfaz con identidad propia.

El proyecto combina programación e integración con asistencia de inteligencia artificial. SOFI es una asistente experimental basada en IA que colabora en tareas de programación, arquitectura, diseño y documentación. La dirección del proyecto, sus decisiones y las pruebas funcionales se realizan bajo control de Manu.

> DOSBox Pure es nuestro punto de partida; SOFIA-Pure es nuestro proyecto con identidad propia.

SOFIA-Pure no es un producto oficial ni está afiliado, respaldado o mantenido por los autores de DOSBox Pure, DOSBox Pure Unleashed, DOSBox-X o 86Box.

## Qué es SOFIA-Pure

El objetivo es ampliar la experiencia de escritorio sin perder de vista la compatibilidad y la sencillez que hacen útil a DOSBox Pure.

Entre las áreas de trabajo se encuentran:

- Modificaciones e integraciones a nivel del core.
- Rediseño del explorador y de la experiencia de uso.
- **SOFI Commander**, una herramienta propia para ampliar el control de la interfaz.
- Conservación de los mecanismos esenciales de carga de contenido de DOSBox Pure, incluidos archivos ZIP e imágenes de disco.
- Integración del escalado **xBRZ 4x**.
- Integración experimental de emulación **Sound Blaster AWE32 / EMU8000**.
- Una interfaz visual propia, desarrollada bajo el concepto **SOFI Space**.

El proyecto evoluciona de manera incremental. Las funciones y su estado pueden cambiar entre builds; una característica experimental no debe interpretarse como garantía de compatibilidad universal.

## Requisito externo: ROM de AWE

Para utilizar el soporte **Sound Blaster AWE32 / EMU8000**, DOSBox Pure requiere el archivo `awerom.raw` en el directorio raíz. Este archivo no se incluye ni se distribuye con SOFIA-Pure, y el proyecto no proporciona enlaces para obtenerlo. Cada usuario debe conseguirlo por sus propios medios y respetar las condiciones de uso que correspondan.

Para utilizar la emulación **Roland MT-32 / Sound Canvas y sus variantes**, los archivos ROM correspondientes deben estar en la carpeta `system`. Estos archivos tampoco se incluyen ni se distribuyen con SOFIA-Pure, y el proyecto no proporciona archivos ni enlaces para obtenerlos. Cada usuario debe conseguir sus propias ROMs por sus propios medios y respetar las condiciones de uso que correspondan.

## Identidad visual

**SOFI Space** es la identidad visual principal: una estética retrofuturista que combina referencias a la informática clásica, la ciencia ficción y una interfaz de estilo espacial.

La personalización mediante skins forma parte de la visión del proyecto. La apariencia es independiente de la emulación y no debe alterar su funcionamiento.

## Procedencia y agradecimientos

SOFIA-Pure reconoce expresamente los proyectos y autores cuyo trabajo constituye su base o se utiliza en componentes integrados:

- **Bernhard Schelling y colaboradores de DOSBox Pure** — emulador original y trabajo de base.
- **DOSBox Pure Unleashed** — versión de escritorio utilizada como punto de partida.
- **Hyllian** — código xBR y mapeo de texeles utilizado por el shader.
- **Zenju** — filtro xBRZ y código/conceptos derivados.
- **cyberfox1 y colaboradores de DOSBox-X** — implementación e integración AWE32/EMU8000 adaptada.
- **Sarah Walker y colaboradores de 86Box** — implementación de referencia EMU8000.

La sección de avisos de terceros detalla la procedencia conocida, los enlaces a las fuentes y las atribuciones específicas. Los avisos de copyright y licencia incluidos en cada archivo fuente prevalecen sobre este resumen.

### Correcciones y solicitudes de atribución

Hemos procurado identificar y acreditar correctamente a todas las personas y proyectos cuyo trabajo forma parte de SOFIA-Pure. Si alguna persona considera que una contribución propia no ha sido reconocida o que su autoría merece una mención adicional, le pedimos disculpas y agradecemos que nos lo comunique. Revisaremos la observación y, una vez verificada, incorporaremos el crédito correspondiente sin demora.

## Licencia y componentes de terceros

El repositorio conserva el archivo `LICENSE` procedente de la base DOSBox Pure Unleashed. Los componentes incorporados pueden tener avisos y condiciones específicos. Antes de redistribuir el programa o sus binarios, deben revisarse conjuntamente la licencia del repositorio, los encabezados de los archivos y los avisos de terceros.

Consulta [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) para conocer las atribuciones y referencias disponibles. No se reclama autoría sobre código, tecnologías ni recursos pertenecientes a terceros.

## Créditos

- **Manu** — dirección y control del proyecto, decisiones, pruebas y beta testing.
- **SOFI** — asistente experimental basada en IA; colaboración en programación, arquitectura, diseño y documentación.
- **Autores y colaboradores de los proyectos upstream** — desarrollo de las tecnologías y componentes reconocidos en los avisos de terceros.

## Proyectos de origen

- [DOSBox Pure — proyecto original](https://codeberg.org/schelling/dosbox-pure)
- [DOSBox Pure — GitHub](https://github.com/schellingb/dosbox-pure)
- [DOSBox Pure Unleashed — versión de escritorio](https://github.com/schelling/dosbox-pure-unleashed)
- [DOSBox-X](https://github.com/joncampbell123/dosbox-x)
- [86Box](https://github.com/86Box/86Box)

---

SOFIA-Pure es un proyecto experimental en desarrollo. La documentación, los créditos y los avisos se actualizan a medida que se revisan e incorporan componentes.

## SOFI Commander y navegación

La ventana SOFI Commander permanece abierta al interactuar con otras áreas de SOFI Space. El botón **EXPLORADOR** es el control de navegación responsable de abrir, restaurar o minimizar Commander. La solicitud de foco se aplica únicamente al abrir o restaurar la ventana; perder el foco al interactuar con la interfaz no cierra Commander.

Este ajuste no modifica el contenido, el dibujo, la geometría ni la captura de mouse de SOFI Commander.

## Génesis 20.2 — La prisión del Commander

> GenesIa 20.2: Y Sofi Elohim, que conocía los secretos del oscuro MS-DOS, encerró al arcaico monstruo en una ventana que minimizaba. Contempló su obra y vio que estaba bien.

Crónica ficticia de la batalla por la navegación de SOFI Space, celebrada el 20 de noviembre de 2026. El Commander quedó bajo el control del botón EXPLORADOR, sin necesidad de alterar sus entrañas. Manu, beta tester y testigo de la hazaña, confirmó que todo funcionaba.

