# SOFIA-Pure — Auditoría arquitectónica

**Fecha:** 18 de noviembre de 2026  
**Tipo:** diagnóstico técnico; no implica cambios en el código del emulador ni en la Build 204.  
**Estado:** auditoría cerrada como diagnóstico. Las recomendaciones de este documento son propuestas, no implementaciones.

## 1. Referencias y alcance

- Repositorio de trabajo: https://github.com/manudias70-spec/SOFIA-Pure
- Repositorio base original: https://github.com/manudias70-spec/dosbox-unleashed
- Build de referencia: [Build 204 — GitHub Actions](https://github.com/manudias70-spec/SOFIA-Pure/actions/runs/44229109351)
- Rama de la Build 204: `experiment/video-options-layout`
- Commit auditado: `251c4e47a80b8be480f6ca5d9639bab80205d38b`
- Mensaje del commit: `Restore Info box to original footer position`
- Resultado conocido: compilación Win32 y Win64 MSVC correcta, artefactos publicados. El usuario probó la Build 204 y confirmó que funciona correctamente (“De 10”).

La auditoría busca determinar qué partes de SOFIA-Pure son independientes de DOSBox Pure y qué partes dependen de detalles internos del core. El objetivo práctico es estimar la viabilidad de sustituir DOSBox Pure RC8 por RC9 u otro core en el futuro, preservando la interfaz y las funciones propias.

No se modificó el código de la Build 204 durante esta auditoría.

## 2. Resumen ejecutivo

**Veredicto: viable con adaptación.**

SOFIA-Pure no está atrapado en una arquitectura cerrada y no necesita comenzar desde cero para evaluar DOSBox Pure RC9. Sin embargo, todavía no es un frontend completamente desacoplado del core.

Las partes visuales y de entrada básica están relativamente separadas. En cambio, SOFI Commander, el navegador, las operaciones de montaje/apertura, AWE32/EMU8000, parte del audio y varios servicios privados dependen de implementaciones internas de DOSBox Pure.

Por eso, cambiar RC8 por RC9 probablemente sea viable, pero requerirá adaptar parches, headers, helpers privados, opciones, audio y operaciones de contenido. Cambiar a otro core sería un trabajo mayor: la API Libretro proporciona una base común, pero no garantiza equivalencia funcional con las extensiones privadas de Pure.

## 3. Arquitectura observada

SOFIA-Pure es una aplicación anfitriona/frontend basada en ZillaLib que integra un core Libretro. DOSBox Pure es el core actualmente incorporado.

La estructura observada puede resumirse así:

```text
SOFIA-Pure
  |
  +-- SOFIA frontend / ZillaLib
  |     +-- ventana y presentación
  |     +-- entrada
  |     +-- opciones de interfaz
  |     +-- audio y vídeo de frontend
  |
  +-- integración Libretro
  |
  +-- extensiones y servicios privados de DOSBox Pure
        +-- OSD / SOFI Commander
        +-- navegador interno
        +-- montaje y apertura de contenidos
        +-- AWE32 / EMU8000
        +-- callbacks DBPS_*
```

El archivo de proyecto Visual Studio compila directamente `main.cpp`, `vfs_implementation.cpp` y fuentes internas del core dentro del mismo proyecto/binario. Por lo tanto, no debe describirse la integración actual como un simple reemplazo de una DLL intercambiable. La auditoría no determina aquí todos los detalles de enlace del ejecutable y no afirma más de lo que se comprobó.

Libretro ofrece un contrato estándar frontend-core, pero SOFIA-Pure también utiliza extensiones privadas de Pure.

## 4. SOFI Commander y OSD

### Hechos comprobados

- SOFI Commander está implementado dentro del OSD interno de DOSBox Pure, principalmente en `dosbox_pure_osd.h`.
- El script `tools/patch_osd_sidebar.py` (397 líneas) modifica principalmente `dosbox_pure_osd.h` y también `core_options.h`.
- El script aplica reemplazos textuales mediante `source.replace(old,new,1)`; algunos anclajes verifican coincidencias y abortan si no encuentran la estructura esperada.
- Commander agrega lógica y presentación propias: geometría, barra lateral, panel informativo, colores, botones, navegación, hit-testing y retorno al Explorer.
- Reutiliza primitivas y estructuras internas de Pure, entre ellas `DrawMenuBase`, `Print`, `DrawBox`, `FillRect`, bitmap font y estructuras de selección/opciones.

### Interpretación técnica

Commander no es únicamente un skin: contiene lógica propia, pero está fuertemente acoplado a las estructuras y primitivas internas del OSD Pure. Un cambio de organización en RC9 puede romper los anclajes del parche o requerir adaptar su integración.

### Recomendación

A largo plazo, mover la lógica y presentación de Commander al frontend SOFIA y dejar en un adaptador las operaciones que necesariamente requieran al core. No hacer esta migración como parte de una actualización rutinaria sin una etapa de pruebas independiente.

## 5. Frontend y frontera de integración (`main.cpp`)

### Hechos comprobados

- `main.cpp` (2170 líneas) contiene la aplicación anfitriona SOFIA/ZillaLib.
- Incluye interfaces Libretro, código de entrada, vídeo, xBRZ, Splash y headers internos de Pure, incluido `dosbox_pure_sta.h`.
- Existen globales como `DBPS_SaveSlotIndex` y `DBPS_BrowsePath`.
- `DBPS_QuitApplication()` invoca `ZL_Application::Quit()`.
- El frontend llama funciones estándar `retro_*` y también funciones privadas de Pure.

### Interpretación técnica

Hay una frontera funcional entre frontend y core, pero no es todavía una frontera limpia: parte de la aplicación conoce tipos, variables y funciones internas del core.

### Recomendación

Definir un Core Adapter que concentre las dependencias específicas y evite que la interfaz SOFIA invoque helpers privados directamente.

## 6. API Libretro y dependencias privadas

Entre las funciones estándar Libretro observadas se encuentran:

- `retro_get_system_info`
- `retro_set_environment`
- `retro_init`
- `retro_load_game`
- `retro_set_input_poll`
- `retro_set_input_state`
- `retro_set_video_refresh`
- `retro_get_system_av_info`
- `retro_set_controller_port_device`
- `retro_run`
- `retro_serialize_size`
- `retro_serialize`
- `retro_unserialize`

También se observaron dependencias privadas de DOSBox Pure, entre ellas:

- `DBPS_GetContentName()`
- `DBPS_NetworkConnect(...)`
- `DBPS_AudioMix(...)`
- `DBPS_SubmitOSDFrame(...)`
- `DBPS_IsShowingOSD()`
- `DBPS_StartCaptureJoyBind`, `DBPS_HaveJoy`, `DBPS_GetJoyBind`, `DBPS_GetMouse`
- `DBPS_RequestSaveLoad`, `DBPS_HaveSaveSlot`, `DBPS_OnContentLoad`, `DBPS_OnReset`
- `DBPS_OpenContent`, `DBPS_AddDisc`, `DBPS_InitLEDs`
- `DBP_Run::autoboot`, `DBP_FullscreenOSD`
- `DBP_MIXER_DoneSamplesCount()` (uso de depuración)
- `DBPS_BrowsePath`, `DBPS_SaveSlotIndex`

No debe asumirse que toda función con prefijo `retro_*` constituye por sí misma parte de la API contractual: cada símbolo debe verificarse. Del mismo modo, helpers como `retro_vfs_*_impl` no deben confundirse automáticamente con la API VFS contractual.

La dirección de dependencia varía según la función. Por ejemplo, el core entrega cuadros OSD mediante `DBPS_SubmitOSDFrame`, mientras que el frontend consulta estado o solicita operaciones mediante otros helpers. El prefijo de un símbolo no basta para determinar quién lo implementa o quién lo llama.

## 7. AWE32 / EMU8000

### Hechos comprobados

- El parche `patches/dosbox-pure-awe32-emu8k-core.patch` tiene aproximadamente 3658 líneas.
- Agrega `include/emu8k.h` y `src/hardware/emu8k.cpp), y modifica `sblaster.cpp`, `core_options.h` y `dosbox.cpp).
- La implementación EMU8000 está adaptada de `snd_emu8k.c` de 86Box.
- La integración utiliza estructuras internas como `MixerChannel`, puertos de I/O, Sound Blaster, callbacks, ROM y serialización.
- La ROM `awe32.raw` se busca junto al ejecutable mediante APIs de Windows. Si falta o no es válida, existe fallback a SB16.

### Interpretación técnica

La implementación EMU8000 es una extensión propia y relativamente delimitada, pero depende de componentes internos de Pure. Una actualización a RC9 puede exigir adaptar la integración con mixer, I/O y serializer. No hay evidencia suficiente para afirmar portabilidad a Linux o macOS.

### Recomendación

Mantener AWE32 como extensión específica del adaptador Pure. Auditarla y probarla por separado ante cada actualización del core; no mezclar su adaptación con una refactorización general del frontend.

## 8. Vídeo, xBRZ y presentación

### Hechos comprobados

- SOFIA implementa callbacks Libretro de vídeo, entre ellos `retro_video_refresh_cb()`, `retro_hw_get_proc_address()` y `retro_hw_get_current_framebuffer()`.
- La geometría se recibe mediante `RETRO_ENVIRONMENT_SET_GEOMETRY` y `RETRO_ENVIRONMENT_SET_SYSTEM_AV_INFO`.
- El frontend entrega al core el contexto gráfico/framebuffer de ZillaLib.
- `xbrz_shader.h` es código propio de SOFIA incluido desde `main.cpp`.
- `ApplyInterfaceOptions()` usa `interface_scaling`; con `Scaling == 'X'`, procesa xBRZ desde el frontend mediante ZillaLib.
- El workflow también incorpora opciones xBRZ en `core_options.h`.
- El workflow modifica dimensiones OSD a 960x540 y el frontend valida `DBPS_OSD_WIDTH/HEIGHT`.

### Interpretación técnica

El procesamiento xBRZ se encuentra del lado frontend y no modifica el renderizador interno de Pure. Su dependencia del core es baja, siempre que se mantengan el pipeline de vídeo y la integración gráfica esperada.

La presentación no es universalmente intercambiable: el contexto gráfico y framebuffer que espera SOFIA deben ser compatibles con el core utilizado. Un cambio en la geometría OSD también puede exigir adaptación.

### Recomendación

Conservar xBRZ y los filtros como responsabilidad de SOFIA. En una prueba RC9, validar primero geometría, framebuffer, contexto gráfico y OSD antes de tocar el shader.

## 9. Audio

### Hechos comprobados

- SOFIA utiliza `ZL_Audio::HookAudioMix(AudioMix)` y `ZL_Audio::Init(...)`.
- La mezcla/sincronización utiliza el helper privado de Pure `DBPS_AudioMix()`.
- SOFIA comunica parámetros de velocidad de reproducción (normal, rápida, lenta y paso a paso) y latencia.

### Interpretación técnica

El audio no está completamente desacoplado mediante el callback estándar de audio Libretro. La auditoría no permite afirmar que el core no utilice callbacks estándar en otras partes.

### Recomendación

Incluir audio en el contrato del Core Adapter y comprobar el comportamiento real de RC9. Para otros cores, será necesario un adaptador compatible con su mecanismo de audio.

## 10. Entrada: teclado, mouse y joystick

### Hechos comprobados

- El frontend ZillaLib captura teclado, mouse y joystick y traduce sus estados a Libretro.
- El teclado utiliza eventos keydown/keyup, modificadores y traducción de códigos a `RETROK`.
- El mouse traduce movimiento relativo/absoluto, botones, rueda y coordenadas.
- La lógica de mouse consulta `DBPS_IsShowingOSD()` para el bloqueo del puntero.
- El subsistema joystick gestiona detección/desconexión, botones, ejes, hats, trackballs, captura, perfiles XInput/PS4, persistencia y hasta cuatro puertos.
- La UI OSD de controles consulta helpers Pure como `DBPS_GetJoyBind`, `DBPS_HaveJoy` y `DBPS_StartCaptureJoyBind`.

### Interpretación técnica

El motor básico de entrada del frontend es propio y bastante independiente. En cambio, la configuración visual de mandos está acoplada al OSD. Otros cores pueden no admitir las mismas clases de dispositivos ni cuatro puertos con idéntica semántica.

### Recomendación

Conservar el motor de entrada. Desacoplar la configuración de mandos de la UI interna de Pure y validar las capacidades que cada core declara.

## 11. Navegador y sistema de archivos

### Hechos comprobados

- El navegador actual forma parte del Commander/OSD interno.
- Enumeración, filtrado de extensiones, navegación, selección, apertura y montaje dependen en gran medida de Pure.
- Se usan funciones VFS Libretro (`opendir`, `readdir`, etc.) para directorios desde el core.
- El VFS disponible al core no se convierte automáticamente en un servicio de archivos accesible desde el frontend.
- SOFIA contiene `vfs_implementation.cpp`, que constituye un posible punto de partida para estudiar una capa VFS propia del frontend.
- SOFIA agrega columnas de tamaño, fecha y hora mediante código propio y APIs Win32 como `GetFileAttributesExW`.
- `RefreshList()`, `DoInput()` y `DBPS_BrowsePath` forman parte del navegador interno.

### Interpretación técnica

Commander tiene lógica de navegación propia, pero el navegador está muy acoplado al motor interno de Pure. Migrarlo al frontend es factible conceptualmente, pero no equivale a mover una ventana: requiere separar proveedor de archivos, navegación y operaciones específicas del core. La implementación actual de metadatos también tiene dependencias Win32.

### Recomendación

Diseñar un proveedor de archivos frontend independiente y un adaptador para operaciones de contenido. No asumir que la VFS del core puede reutilizarse sin una capa explícita.

## 12. Carga, apertura y montaje de contenidos

### Hechos comprobados

- La carga inicial se realiza mediante `retro_load_game()`.
- En `retro_environment_cb()`, el host tiene comentado `RETRO_ENVIRONMENT_SET_DISK_CONTROL_EXT_INTERFACE` y devuelve `false); también rechaza la interfaz básica `RETRO_ENVIRONMENT_SET_DISK_CONTROL_INTERFACE`.
- Pure registra Extended Disk Control y fallback a la interfaz básica.
- Los callbacks del core invocan operaciones internas como `DBP_Mount` y `DBP_Unmount`.
- Abrir otro contenido desde el navegador no consiste en llamar nuevamente a `retro_load_game()`: `DBPS_OpenContent()` gestiona el flujo interno del OSD y el reinicio mediante `DBP_OnBIOSReboot()`.
- `DBPS_AddDisc()` llama a `DBP_AppendImage()` y `DBP_Mount()`.

### Interpretación técnica

La carga inicial es una operación Libretro estándar, pero el montaje y el cambio de contenido actuales dependen de servicios privados de Pure.

Disk Control puede servir como interfaz para cores que la implementen, pero está orientada al control de imágenes de disco. No garantiza equivalencia con todas las operaciones DOS: montar directorios, abrir ejecutables, cambiar boot, resetear o reproducir exactamente la semántica interna de Pure.

### Recomendación

Separar las operaciones de contenido en el Core Adapter. Utilizar Disk Control cuando corresponda y conservar un adaptador específico Pure para las operaciones adicionales.

## 13. Guardado y restauración de estados

### Hechos comprobados

- SOFIA utiliza `retro_serialize_size()`, `retro_serialize()` y `retro_unserialize()`.
- Los estados se envuelven en un contenedor RZIPv1, con chunks de 131072 bytes y compresión ZillaLib.
- La cabecera observada es `RASTATE\1MEM `.
- Existe compatibilidad con estados legados sin RZIP.
- Los archivos usan extensión `.state`; el nombre de contenido se obtiene mediante `DBPS_GetContentName()` y el slot mediante `DBPS_SaveSlotIndex`.
- El callback privado `DBPS_RequestSaveLoad(save,load)` establece flags que procesa el frontend.
- El bloque MEM es opaco y específico del core; Pure serializa estructuras internas mediante `DBPArchive` y `DBPSerialize_All()`.

### Interpretación técnica

El contenedor RZIP/RASTATE es infraestructura propia que puede conservarse. El contenido serializado no es portable ni garantiza compatibilidad entre RC8, RC9 u otros cores.

### Recomendación

Mantener el contenedor y abstraer identidad de contenido/slot y solicitud de guardado/carga. Tratar los estados internos como específicos de cada core y versión, salvo que exista una garantía explícita de compatibilidad.

## 14. Configuración

### Hechos comprobados

- `IsInterfaceConfigKey(key)` clasifica como interfaz las claves cuya primera letra es `i` y `dosbox_pure_aspect_correction`; las claves `interface_*` quedan del lado SOFIA.
- SOFIA utiliza `GetSetting`, `ConfigCache`, `ConfigOverrides` y Settings de ZillaLib.
- Entre las opciones propias `interface_*` se encuentran escalado, filtros CRT, latencia, velocidades rápida/lenta, modificador de hotkeys, bloqueo de mouse, hotkeys del sistema, botón central y ruta de contenidos.
- `ApplyInterfaceOptions()` gestiona shaders, xBRZ, CRT, latencia, velocidades, bloqueo de mouse y geometría.
- Las opciones del core se negocian mediante `RETRO_ENVIRONMENT_SET_CORE_OPTIONS_V2`, `GET_VARIABLE`, `SET_VARIABLE` y `GET_VARIABLE_UPDATE`.
- Las opciones `dosbox_pure_*` son específicas de Pure. `dosbox_pure_aspect_correction` tiene efecto cruzado en el frontend.

### Interpretación técnica

La configuración de interfaz está bastante separada, aunque existe al menos una opción de Pure con efecto cruzado en SOFIA. Esto es un acoplamiento identificable, no necesariamente un defecto.

### Recomendación

Separar claramente configuración SOFIA de configuración y capacidades del Core Adapter. Evitar que el frontend dependa de nombres de opciones específicos de Pure salvo dentro del adaptador.

## 15. Ciclo de vida del core

### Hechos comprobados

En `OnLoad()` de `main.cpp` se observó esta secuencia general:

1. `retro_get_system_info()`
2. `retro_set_environment()`
3. `retro_init()`
4. Inicialización de LEDs mediante función privada Pure.
5. `retro_load_game(&game)`
6. Configuración de callbacks de entrada y vídeo.
7. `retro_get_system_av_info()`
8. Configuración de cuatro puertos joystick.

En `OnDraw()`, SOFIA llama a `retro_run()` durante el ciclo de emulación y controla pausa, velocidad rápida/lenta, paso a paso y FPS.

En `OnQuit()`, se ejecuta `SynchronizeSettings(true)` y `retro_unload_game()`.

En el archivo inspeccionado no se encontró una llamada a `retro_deinit()` ni a `retro_reset()` desde `main.cpp`. También se observó que la llamada a `retro_load_game()` no comprueba su valor de retorno.

### Interpretación técnica

El ciclo de ejecución está controlado por el frontend y utiliza Libretro, pero inicialización, cierre y reinicio conservan dependencias privadas. Los puntos señalados son aspectos a revisar; no deben calificarse automáticamente como errores sin comprobar garantías y rutas adicionales del proyecto.

### Recomendación

Normalizar inicialización, carga, descarga, reset y cierre en el Core Adapter. Revisar el manejo de errores de carga y el cierre ordenado cuando se pruebe RC9.

## 16. Matriz de independencia y riesgo

| Subsistema | Independencia actual | Riesgo de adaptación |
|---|---|---|
| Interfaz SOFIA / Splash | Alta | Bajo |
| xBRZ y filtros del frontend | Alta | Bajo |
| Teclado y entrada básica | Alta | Bajo |
| Configuración propia `interface_*` | Alta/parcial | Bajo |
| Vídeo y contexto gráfico | Parcial | Medio |
| Audio | Parcial | Medio/alto |
| Guardado de estados | Parcial | Medio/alto |
| Navegador de archivos | Baja | Alto |
| SOFI Commander / OSD | Baja | Alto |
| Apertura y montaje de contenidos | Baja | Alto |
| AWE32 / EMU8000 | Baja respecto al core | Alto |
| Reinicio y helpers privados | Baja | Alto |

La matriz es una evaluación cualitativa de la arquitectura observada, no una predicción de que cada subsistema necesariamente vaya a fallar en RC9.

## 17. Arquitectura objetivo propuesta

La propuesta es introducir una capa de adaptación que concentre las particularidades de cada core:

```text
SOFIA-Pure
  |
  +-- SOFIA UI
  |
  +-- Commander / servicios SOFIA
  |
  +-- Core Adapter
        |
        +-- API Libretro estándar
        |
        +-- Extensiones específicas del core
              +-- DOSBox Pure RC8
              +-- DOSBox Pure RC9
              +-- otro core compatible
```

Responsabilidades sugeridas del Core Adapter:

- Inicialización, carga, descarga, reset y ciclo de vida.
- Capacidades del core y opciones específicas.
- Apertura, montaje y cambio de contenido.
- Integración de audio y vídeo.
- Entrada y capacidades de dispositivos.
- Guardado/restauración y metadatos de estados.
- Extensiones privadas de Pure, aisladas del resto de SOFIA.

Commander debería convertirse progresivamente en una interfaz autónoma que utilice un proveedor de archivos y solicite operaciones al Core Adapter. La VFS del frontend debe diseñarse explícitamente; no se debe asumir que la VFS expuesta al core sirve automáticamente al frontend.

## 18. Hoja de ruta recomendada

1. **Preservar la base funcional.** Mantener Build 204 como referencia conocida y no mezclar la auditoría con cambios de interfaz ya validados.
2. **Definir el contrato Core Adapter.** Especificar servicios, capacidades, errores y operaciones antes de implementar.
3. **Separar Commander.** Extraer primero lógica y presentación que no requieran al core; dejar operaciones específicas detrás del adaptador.
4. **Separar el proveedor de archivos.** Diseñar navegación y metadatos del lado frontend.
5. **Normalizar ciclo de vida y contenido.** Unificar carga, descarga, reset, apertura, montaje y capacidades.
6. **Normalizar audio, vídeo, entrada y estados.** Mantener las optimizaciones existentes, pero aislar particularidades de Pure.
7. **Mantener AWE32 como extensión específica.** Adaptarla por separado ante cambios del core.
8. **Probar RC9 en una rama experimental.** No reemplazar la referencia funcional hasta completar pruebas de compilación y comportamiento.

## 19. Qué conservar, qué adaptar y qué no asumir

### Conservar

- La identidad visual y la interfaz SOFIA.
- Splash y presentación del frontend.
- xBRZ y filtros que se ejecutan en SOFIA.
- El motor de entrada básico.
- El contenedor de estados RZIP/RASTATE.
- La Build 204 como referencia funcional.

### Adaptar o aislar

- Commander y navegador.
- Helpers privados DBPS/DBP.
- Apertura y montaje de contenidos.
- Audio y contexto gráfico.
- Opciones cruzadas entre frontend y Pure.
- AWE32/EMU8000 y su integración interna.

### No asumir

- Que cualquier core Libretro puede reemplazar a Pure sin pérdida de funciones.
- Que los estados guardados serán compatibles entre versiones/core.
- Que Disk Control reemplaza todas las operaciones DOS de Pure.
- Que la VFS del core está disponible automáticamente al frontend.
- Que RC9 conserva los mismos headers, estructuras OSD, helpers privados o anclajes de parche.
- Que las recomendaciones de esta auditoría ya están implementadas.

## 20. Conclusión

SOFIA-Pure tiene una base real de frontend propio y una parte importante de sus funciones puede preservarse. El proyecto no está arquitectónicamente cerrado, pero su independencia actual es parcial.

**El cambio a DOSBox Pure RC9 es viable con adaptación.** El camino razonable no es reescribir todo ni sustituir el core a ciegas: es conservar la base funcional, introducir gradualmente un Core Adapter y probar cada versión en una rama experimental.

La Build 204 queda como referencia probada por el usuario. Esta auditoría documenta el estado y propone una dirección futura; no modifica ni invalida esa build.
