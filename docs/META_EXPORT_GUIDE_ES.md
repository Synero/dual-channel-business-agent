# Descarga tus mensajes de Instagram (Meta Account Center)

Para clonar tu personalidad real, necesitas tu historial real de DM de Instagram. Meta te permite descargarlos como un export en HTML.

## Paso a Paso

### 1. Ve a Meta Accounts Center

Abre: **https://accountscenter.meta.com**

Inicia sesión con la cuenta de Instagram que usas para chatear con clientes.

### 2. Navega a "Tu información y permisos"

Haz clic en **"Descargar tu información"**

### 3. Solicita una descarga

1. Haz clic en **"Solicitar una descarga"**
2. Selecciona tu cuenta de Instagram
3. Elige **"Copia completa"** (o "Seleccionar tipos de información" → Solo mensajes)
4. Formato: **HTML**
5. Calidad: **Baja** (más rápido, solo necesitas texto)
6. Rango de fechas: **Todo el tiempo** (recomendado para mejor captura de personalidad)
7. Haz clic en **"Enviar solicitud"**

### 4. Espera el correo

Meta te enviará un correo cuando esté listo (generalmente de 10 minutos a 24 horas).

### 5. Descarga el ZIP

Haz clic en el enlace de descarga del correo. Obtendrás un archivo como:

```
instagram-tuusuario-2026-01-01-xxxx.zip
```

### 6. Extrae y localiza los mensajes

```bash
unzip instagram-*.zip -d instagram_export/
cd instagram_export/messages/inbox/
```

Verás carpetas como:
```
inbox/
  juan_perez_1234567890/
    message_1.html
    message_2.html
    photos/...
  usuario_ejemplo_0987654321/
    message_1.html
    ...
```

Cada carpeta es una conversación. Los archivos HTML contienen tu historial de mensajes real.

### 7. Ejecuta el Parser

```bash
python scripts/parse_instagram_export.py instagram_export/messages/inbox/ --business-name "Tu Nombre de Negocio"
```

Esto hará:
- Parsear todas las conversaciones HTML
- Extraer TUS mensajes (identificados por el nombre del negocio)
- Construir un archivo de vocabulario, patrones de saludo y perfil de estilo de respuesta
- Guardar en `chat_logs/` para que el agente aprenda

## Qué se extrae

- **Vocabulario**: Palabras, jerga, abreviaturas que realmente usas
- **Patrones de saludo**: Cómo dices hola ("Holii", "Buenass", etc.)
- **Longitud de respuesta**: Mensajes cortos vs largos
- **Emojis**: Cuáles usas y con qué frecuencia
- **Formato de precios**: Cómo cotizas precios a los clientes
- **Patrones de cierre**: Cómo terminas las conversaciones

## Nota de privacidad

Esta herramienta solo extrae **tus propios mensajes** (no los de los clientes) y almacena todo localmente. Ningún dato sale de tu máquina.
