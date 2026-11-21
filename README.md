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

Para utilizar el soporte **Sound Blaster AWE32 / EMU8000**, esta integración del core requiere el archivo `awe32.raw` junto a `DOSBoxPure.exe`. El archivo debe ser la ROM compatible de 1 MiB que espera el EMU8000. No se incluye ni se distribuye con SOFIA-Pure, y el proyecto no proporciona enlaces para obtenerlo. Cada usuario debe conseguirlo por sus propios medios y respetar las condiciones de uso que correspondan.

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
- [DOSBox Pure Unleashed — versión de escritorio](https://github.com/dosbox-pure/dosbox-pure-unleashed)
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

## Evangelio del Mono — capítulo 1, versículo 1

> Y el mono, sin conocimientos de C++, tocó el fondo con su dedo. Y el Commander perdió la compostura. Entonces Sofi examinó las escrituras del código y halló la condición maldita.

El mono no resolvió el bug: encontró cómo reproducirlo. Su clic reveló el comportamiento extraño que permitió investigar el conflicto de foco y separar la solicitud de foco del estado real de la ventana. Quede asentado que una observación sencilla puede abrir el camino hacia la causa de un problema difícil.


## Prototipo visual del panel VIDEO

La rama `experiment/video-panel-visual` incorpora un primer prototipo visual del panel **VIDEO** en SOFI Space. El botón VIDEO abre un panel hacia la derecha de la navegación, con listas desplegables que conservan visualmente el valor elegido. Incluye las opciones de video de la configuración de escritorio de DOSBox Pure: adaptadores y modos gráficos, memoria SVGA, emulación y rendimiento Voodoo, escalado, filtro CRT, corrección de aspecto y overscan.

**Estado: controles conectados a la configuración.** SOFI VIDEO lee los valores activos desde la configuración que utiliza DOSBox Pure y refleja la selección real al abrir el panel. Al cambiar una opción, escribe el valor correspondiente en la configuración del emulador y notifica la actualización mediante el mecanismo de variables de Libretro. Los ajustes propios de la interfaz (Scaling y filtros CRT) solicitan además la reaplicación de sus efectos; Aspect Ratio Correction actualiza la geometría de presentación.

El selector Scaling incluye **xBRZ 4x**, vinculado al valor `xbrz` incorporado en las opciones del core durante la compilación. Las opciones que DOSBox Pure identifica como «restart required» conservan esa limitación: el cambio queda guardado, pero requiere reiniciar el core para entrar en vigor.


## Estado de SOFI AUDIO

El panel **SOFI AUDIO** utiliza el mismo mecanismo de configuración que SOFI VIDEO: cada control lee el valor activo del core y escribe los cambios mediante la ruta de configuración de DOSBox Pure. Incluye SoundBlaster Settings (puerto, IRQ y DMA), selección de MIDI, los seis controles de volumen, SoundBlaster Type (incluida AWE32 / EMU8000), modo FM/OPL, proveedor OPL, Gravis Ultrasound, Tandy y cambio de canales estéreo. La lista MIDI se obtiene de las opciones dinámicas que entrega el core, para mostrar los SoundFonts y ROMs detectados en el directorio de sistema. La selección MIDI se guarda también como preferencia persistente, incluso cuando existe una configuración específica del juego; al cerrar el panel AUDIO se fuerza la sincronización de los ajustes pendientes. La detección de Roland SC-55 / MT-32 y sus variantes sigue dependiendo de que las ROM correspondientes estén presentes.

En la compilación **standalone** de SOFIA-Pure, DOSBox Pure no expone el selector Audio Sample Rate: la frecuencia de muestreo queda determinada por la compilación. Por eso el panel presenta **Audio Latency**, conectada a `interface_audiolatency`, que sí es configurable en esta versión. Los ajustes marcados como *restart required* necesitan reiniciar el core para entrar en vigor.

AWE32 / EMU8000 permanece como una opción exclusiva dentro de SoundBlaster Type, sin interruptor separado. Requiere `awe32.raw` junto a `DOSBoxPure.exe`; los recursos de puerto, IRQ y DMA se comparten con la familia SoundBlaster.
