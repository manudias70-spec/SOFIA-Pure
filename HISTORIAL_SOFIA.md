# HISTORIAL DE DESARROLLO — SOFIA-PURE

**Versión del registro:** 0.1  
**Fecha de reconstrucción:** 18 de noviembre de 2026

## 1. Proyecto de origen

SOFIA-Pure parte del proyecto original:

- **Repositorio:** [DOSBox Unleashed](https://github.com/manudias70-spec/dosbox-unleashed)
- **Propietario:** `manudias70-spec`

Este repositorio constituye la base de referencia anterior a las modificaciones propias de SOFIA-Pure.

## 2. Cronología de desarrollo

### Build 10 — Escalado gráfico
- Incorporación del escalador gráfico **xBRZ 4x**.

### Build 12 — Identidad visual
- Incorporación de la pantalla de inicio **Splash SOFIA**.
- Conserva la incorporación de xBRZ 4x de la Build 10.

### Build 59 — Compatibilidad de audio
- Implementación de **Sound Blaster AWE32**.
- La funcionalidad efectiva de esta implementación queda pendiente de confirmación específica para esta build.

### Build 77 — Optimización y Splash
- Incorporación de optimizaciones generales.
- Nuevos cambios en la pantalla de inicio Splash SOFIA.
- Mantiene los desarrollos anteriores: xBRZ 4x y AWE32.

### Builds posteriores a la 77 y anteriores a la 119 — Intentos de UI externa
- Se realizaron distintos intentos de incorporar una interfaz de usuario externa.
- Los intentos fueron fallidos: la UI externa no quedó implementada de forma funcional.
- Esta etapa se registra como trabajo experimental fallido, no como una característica incorporada.

### Build 119 — Base de retomada
- Se retoma el desarrollo tomando esta build como nueva base de trabajo.
- Se considera probable que sea una copia de la Build 77; esta relación aún no fue comprobada mediante comparación de fuentes o commits.

### Build 137 — Reorganización de la UI
- Primera serie de cambios orientados a reorganizar la interfaz de usuario.
- El alcance técnico concreto de la reorganización queda pendiente de documentar.

## 3. Estado de verificación

Este documento registra los cambios identificados durante la reconstrucción histórica.

No se consideran confirmados, salvo indicación expresa:
- Los detalles técnicos de cada optimización.
- Las modificaciones específicas realizadas al Splash en cada etapa.
- El resultado de pruebas funcionales individuales.
- La relación exacta entre cada build y su commit.

## 4. Repositorio de desarrollo

[SOFIA-Pure — GitHub](https://github.com/manudias70-spec/SOFIA-Pure)

---

**Criterio de documentación:** cada nueva build deberá registrar su número, cambios incorporados, estado de compilación, pruebas funcionales y referencia al commit o ejecución de GitHub Actions cuando estén disponibles.

Los datos pendientes se completarán únicamente con evidencia o confirmación del desarrollador.
