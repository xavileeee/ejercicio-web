# Copilot Instructions ✅

**Propósito:** Este archivo contiene instrucciones y expectativas para GitHub Copilot al trabajar en este repositorio.

---

## Resumen del proyecto 💡
- Aplicación FastAPI muy simple que sirve una UI estática (`/static`) y expone endpoints en `src/app.py`.
- Datos en memoria: variable `activities` en `src/app.py` (se pierde al reiniciar).

---

## Objetivos principales para Copilot 🎯
- Priorizar **pequeñas mejoras seguras** con tests incluidos (pytest).
- Añadir **pruebas unitarias** y de integración para endpoints: `GET /activities` y `POST /activities/{activity_name}/signup`.
- Proponer y aplicar validaciones mínimas (email, límite de participantes, evitar duplicados) con mensajes y códigos HTTP apropiados.

---

## Reglas y convención de trabajo 🔧
- Mantener cambios pequeños y fáciles de revisar; abrir una rama por feature/bugfix.
- Escribir tests antes o junto al cambio (ej.: `tests/test_activities.py`).
- Usar español en los mensajes de commit y PR, salvo que el contexto requiera inglés.
- No introducir dependencias innecesarias; preferir librerías estándar del ecosistema Python o dependencias ya en `requirements.txt`.

---

## Comandos útiles para desarrollar 🛠️
- Instalar dependencias:
```bash
pip install -r requirements.txt
```
- Ejecutar servidor en local:
```bash
uvicorn src.app:app --reload
```
- Correr tests:
```bash
pytest -q
```
- Probar endpoints con curl (ejemplos):
```bash
curl http://localhost:8000/activities
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=alumno%40ejemplo.edu"
```

---

## Áreas de mejora recomendadas 💡
- Validación de formato de email y límites de participantes.
- Evitar duplicados al inscribir usuarios.
- Añadir manejo básico de concurrencia o migrar a persistencia (DB) cuando se añadan pruebas de integración.
- Añadir tests para casos de error (actividad no existe, actividad llena, email mal formado, inscripción duplicada).

---

## Qué hacer si necesitas más contexto ❓
- Revisar `src/app.py` y `src/static/*` para entender la UI y cómo consume la API.
- Leer `README.md` y `src/README.md` si están presentes.
- Si surgen dudas, abrir un issue con la etiqueta `help wanted`.

---

Si quieres, puedo **generar tests iniciales** para `get_activities` y `signup_for_activity` y proponer los cambios mínimos en `src/app.py` para validaciones básicas. ¿Procedo con eso? ✅
