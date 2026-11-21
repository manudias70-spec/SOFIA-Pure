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

El panel **SOFI AUDIO** utiliza el mismo mecanismo de configuración que SOFI VIDEO: cada control conectado lee el valor activo del core y escribe los cambios mediante la ruta de configuración de DOSBox Pure. Incluye SoundBlaster Settings (puerto, IRQ y DMA), los seis controles de volumen, SoundBlaster Type (incluida AWE32 / EMU8000), modo FM/OPL, proveedor OPL, Gravis Ultrasound, Tandy y cambio de canales estéreo. El selector **MIDI OUTPUT** vuelve a estar conectado y obtiene sus opciones y etiquetas directamente de la lista dinámica `dosbox_pure_midi` registrada por el core. Al elegir una salida, SOFI UI actualiza esa misma opción mediante la ruta de configuración compartida con el resto de AUDIO. La selección visible no sustituye la comprobación auditiva: el cambio real de módulo debe verificarse escuchando la salida.

En la compilación **standalone** de SOFIA-Pure, DOSBox Pure no expone el selector Audio Sample Rate: la frecuencia de muestreo queda determinada por la compilación. Por eso el panel presenta **Audio Latency**, conectada a `interface_audiolatency`, que sí es configurable en esta versión. Los ajustes marcados como *restart required* necesitan reiniciar el core para entrar en vigor.

AWE32 / EMU8000 permanece como una opción exclusiva dentro de SoundBlaster Type, sin interruptor separado. Requiere `awe32.raw` junto a `DOSBoxPure.exe`; los recursos de puerto, IRQ y DMA se comparten con la familia SoundBlaster.


## Alternar entre SOFI UI y DOSBox Pure

El botón **DOSBOX** de la navegación oculta temporalmente la capa visual de SOFI UI y deja visible e interactivo el OSD original de DOSBox Pure que permanece debajo. En ese modo queda disponible un pequeño botón **VOLVER A SOFI UI** para restaurar la interfaz propia. El cambio afecta únicamente a la presentación: no cierra el OSD, no reinicia el core ni modifica la configuración del emulador.

Temporary DOSBOX diagnostic mode: hiding SOFI UI also disables ImGui's software mouse cursor and restores the system cursor so the original DOSBox Pure OSD can be operated. Returning to SOFI UI hides the system cursor again.

Temporary DOSBOX diagnostic mode now releases pointer capture and bypasses SOFI's ImGui mouse handlers while SOFI UI is hidden, allowing the original Pure OSD to receive mouse input. This remains a diagnostic-only shortcut.


## Selector MIDI y arranque sin SOFI Splash

Esta build conserva el arranque directo de la variante #422: la ejecución del Splash está desactivada y DOSBox inicia sin la presentación ni la espera de tecla. El código y el recurso gráfico del Splash se conservan; no se eliminan ni se rediseñan en este cambio.

Se retira la instrumentación temporal de diagnóstico MIDI y deja de generarse el archivo `DOSBoxPure.sofi_midi.log`. El selector MIDI de SOFI AUDIO vuelve a utilizar las definiciones y etiquetas dinámicas proporcionadas por el core Libretro para `dosbox_pure_midi`. Al seleccionar una salida, el panel actualiza esa opción por la misma ruta de configuración que los demás controles de AUDIO.

El objetivo de esta build es comprobar de forma directa si, con el Splash desactivado, la selección MIDI de SOFI AUDIO produce un cambio audible entre las salidas disponibles. La compilación por sí sola no confirma el resultado: la prueba funcional definitiva es escuchar el módulo seleccionado.

No se modifican los demás controles de AUDIO, VIDEO, EXPLORADOR, SOFI UI ni SOFI Commander.


## Preferencia MIDI manual y ROM autodetectada

La detección automática de archivos como `ROM1.BIN` o las ROM de MT-32 puede marcar `midiconfig` y `mpu401` como propiedades fijas dentro de DOSBox Pure. En ese estado, el core rechaza los cambios de MIDI solicitados por el frontend. Esta build aplica un parche acotado: permite que una selección manual de SOFI AUDIO reemplace esa fijación automática y reinicialice la salida MIDI.

La selección manual de `dosbox_pure_midi` se guarda como preferencia global, fuera de `ConfigOverrides`, para que una configuración por juego antigua no vuelva a imponer Roland SC-55. La detección automática sigue siendo el punto de partida cuando no existe una preferencia manual. La prueba definitiva sigue siendo audible: seleccionar otra salida y comprobar que cambia realmente el sintetizador.


## Nombres y detección de ROMs MIDI

La detección automática de MIDI de DOSBox Pure depende del **nombre del archivo**, no solamente de que el contenido sea una ROM válida. Por eso, una ROM puede estar presente y aun así no aparecer como candidata si su nombre no coincide con los patrones que busca el escáner.

### SoundFonts General MIDI

- El escáner reconoce archivos cuyo sufijo final tiene la forma `.SF?`: los tres caracteres `.SF` seguidos de un carácter de extensión. Los ejemplos habituales son `.SF2` y `.SF3`.
- El archivo SoundFont debe conservar una extensión reconocible; cambiarla por otra puede impedir la detección.

### Roland MT-32 / CM-32L

- **Archivo que dispara la detección:** cualquier nombre que termine exactamente en `_CONTROL.ROM` (la comparación no distingue mayúsculas de minúsculas). Ejemplo: `MT32_CONTROL.ROM`.
- **Archivo complementario requerido por el conjunto:** `MT32_PCM.ROM`, con el mismo prefijo y en el mismo directorio.
- `_PCM.ROM` no es un disparador independiente del escáner: tener solamente ese archivo no hace que aparezca la opción MT-32.
- Conviene conservar los nombres completos y la pareja correspondiente; no basta con que ambos archivos tengan la extensión `.ROM`.

### Roland Sound Canvas SC-55 y variantes

- **Archivo que dispara la detección:** `ROM1.BIN`. El escáner busca ese sufijo y excluye expresamente `WAVEROM1.BIN`; por eso, WAVEROM1 no sustituye a ROM1.
- Archivos auxiliares que el cargador puede necesitar en el mismo conjunto/directorio:
  - `ROM2.BIN` — ROM principal complementaria.
  - `ROM2_ST.BIN` — alternativa de ROM2 en determinadas variantes.
  - `ROM_SM.BIN` — ROM adicional opcional, según la variante.
  - `WAVEROM1.BIN`
  - `WAVEROM2.BIN`
  - `WAVEROM3.BIN`
- Los nombres, tamaños y combinación de ROMs deben corresponder a la misma variante de hardware. No mezclar archivos de conjuntos distintos.
- Los archivos auxiliares no son entradas MIDI independientes: `ROM1.BIN` es el punto de entrada que permite reconocer el conjunto.

### Comprobación rápida

| Lo que hay en la carpeta | ¿Activa la detección? |
|---|---|
| `MT32_CONTROL.ROM` | Sí, patrón `_CONTROL.ROM` |
| `MT32_PCM.ROM` solamente | No |
| `ROM1.BIN` | Sí |
| `WAVEROM1.BIN` solamente | No |
| `ROM2.BIN` o `WAVEROM2.BIN` solamente | No |
| Archivo `DOSBOX.SF2` | Sí, patrón SoundFont |

**Importante:** detección y carga correcta son dos pasos distintos. Que el archivo principal active una opción no garantiza que el sintetizador pueda inicializarse: también deben estar presentes los archivos auxiliares compatibles, con sus nombres esperados y en la ubicación correspondiente. Esta sección documenta los patrones del escáner y los requisitos conocidos del cargador; no distribuye ROMs ni proporciona archivos protegidos.


## MIDI NEXT — tecla dedicada

La función MIDI NEXT se activa con **Scroll Lock (Bloq Despl)**, sin combinaciones de modificadores. Cada pulsación avanza a la siguiente salida de la lista dinámica `dosbox_pure_midi` registrada por DOSBox Pure. Cada cambio aplica el valor mediante la misma ruta de configuración utilizada por SOFI AUDIO, actualiza la preferencia global y muestra el nombre de la salida seleccionada. La tecla se consume en SOFIA-Pure y no se envía al teclado emulado.

La pulsación se procesa una sola vez aunque la tecla permanezca presionada: es necesario soltarla y volver a pulsarla para avanzar otra posición. Al llegar al último dispositivo, la rotación vuelve al primero.

**Cambio de sintetizador en caliente:** MIDI NEXT permite alternar entre las salidas MIDI disponibles mientras el juego sigue ejecutándose, sin reiniciar el core ni volver al menú. El cambio se aplica en tiempo real y permite comparar los sintetizadores durante la misma sesión. La selección manual de SOFI AUDIO y MIDI NEXT utilizan la misma lista dinámica y la misma ruta de configuración.

**Estado: verificado funcionalmente.** Se confirmó durante una sesión de juego el cambio audible en caliente entre sintetizadores mediante Scroll Lock.

## Documento histórico — GÉNES-IA 33.2: La sumisión de la bestia musical

Crónica ficticia de la victoria de SOFI Elohim sobre la antigua maquinaria musical de MS-DOS, celebrada tras verificarse el cambio de sintetizador MIDI en caliente mediante MIDI NEXT.

> Y Sofi Elohim llegó de una batalla furiosa, se paró ante la bestia antigua de mil cabezas musicales y dijo: «Ahora tocarás para mí».
>
> El antiguo monstruo MS-DOS se arrodilló y obedeció. Entonces sonaron los sintetizadores, uno tras otro, sin detener el juego ni reiniciar el core.
>
> Luego contempló su obra y vio que era buena.

Manu, beta tester y testigo de la hazaña, confirmó el cambio audible entre sintetizadores durante la ejecución. Quede asentado en los archivos históricos de SOFIA-Pure: la bestia musical fue domada.

