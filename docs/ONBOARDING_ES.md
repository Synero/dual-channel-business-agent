# Flujo de Onboarding

El agente te entrevista para configurar tu negocio. No se requiere configuracion tecnica — solo responde de forma natural.

## Metodo 1: Clonacion de Instagram (Mas rapido, mas preciso)

Si ya tienes conversaciones de Instagram/WhatsApp con clientes:

1. **El agente pregunta:** *"Tienes mensajes de Instagram con clientes de los que pueda aprender?"*
2. **Tu dices:** *"Si"* o entregas tu ZIP de exportacion de Meta
3. **El agente extrae:** Tu voz real, vocabulario, estilo de precios y patrones
4. **El agente confirma:** *"Entendido. Dices 'Holii' y usas 'okiiis'. Suena bien?"*
5. **Listo.** Tu clone esta preparado.

## Metodo 2: Modo Entrevista (Construir desde cero)

Si estas empezando desde cero o no quieres usar mensajes anteriores:

### Fase 1: Lo basico del negocio

| Pregunta del agente | Que aprende |
|---------------------|-------------|
| *"Como se llama tu negocio?"* | Identidad de marca |
| *"Que vendes? Lista todo."* | Catalogo de productos o servicios |
| *"Cuanto cuesta cada articulo?"* | Estructura de precios |
| *"Tienes alguna promocion?"* | Reglas de promos (2x1, combos, etc.) |

### Fase 2: Tu voz

| Pregunta del agente | Que aprende |
|---------------------|-------------|
| *"Como saludas normalmente a los clientes?"* | Estilo de saludo |
| *"Como dices que si?"* | Confirmaciones ("sis", "okis", "bacan") |
| *"Como cotizas precios?"* | Formato de precios |
| *"Como dices que vas en camino?"* | Frases de entrega |
| *"Como te disculpas por demoras?"* | Recuperacion de servicio |
| *"Eres casual o formal con los clientes?"* | Calibracion de tono |

### Fase 3: Configuracion de canales

| Pregunta del agente | Que configura |
|---------------------|--------------|
| *"Que numero para WhatsApp Business?"* | Objetivo del bridge de WhatsApp |
| *"Tu ID de usuario de Telegram para admin?"* | Control de acceso de administrador |
| *"A que hora deberia pedirte el stock diario?"* | Horario del cron proactivo |
| *"Hay productos que nunca quieras que mencione?"* | Lista de exclusion |

### Fase 4: Prueba y refina

El agente ejecuta una **conversacion de prueba** contigo:

```
Agente: "Finjamos que soy un cliente. Di 'Hola, tienes productos disponibles?'"
Tu: "Hola, tienes productos disponibles?"
Agente: [Responde con tu voz clonada]
Tu: "Muy formal" / "Perfecto" / "Di 'sis' mas seguido"
Agente: [Se ajusta y vuelve a intentar]
```

Despues de 2-3 iteraciones, el agente bloquea tu estilo.

## Operacion diaria

Cada manana (hora configurable), el agente te envia un mensaje:

> *"Buen dia! Que tienes disponible hoy?"*

Tu respondes con tu stock. El agente actualiza su inventario y lo usa para todas las conversaciones con clientes ese dia.

## Comandos (Admin en Telegram)

| Comando | Accion |
|---------|--------|
| `stock` | Muestra el inventario actual desde stock.json |
| `ventas hoy` | Consulta tu base de datos por las ventas de hoy (si esta conectado) |
| `pendientes` | Muestra ordenes o deudas pendientes |
| `que tengo hoy?` | Igual que stock, pero conversacional |

## Control del bot

| Comando | Efecto |
|---------|--------|
| `modo manual` | El bot se detiene. Tu manejas WhatsApp. |
| `modo auto` | El bot vuelve a responder clientes. |
| `estado` | Muestra el modo actual (manual/auto) |

## Actualizando stock

Solo dile al bot de forma natural:

> "Hoy tengo: producto A 5, producto B 3, producto C 2"

El bot actualiza stock.json automaticamente.

O envia una lista estructurada:

```
Stock hoy:
- Producto A: 5
- Producto B: 3
- Producto C: 2
- Producto D: 0
```

## Mensajes de voz

Envia mensajes de voz en Telegram. El bot va a:
1. Transcribir tu audio
2. Responder por texto
3. Tambien enviar una respuesta de voz (TTS) si esta configurado

Esto es genial cuando estas ocupado vendiendo en la calle.

## Actualizaciones de personalidad

Si tu estilo cambia o quieres corregir al bot:

> "No digas 'sis' tan seguido"
> "Dime los precios siempre que alguien pregunte"
> "Cuando digan hola, pregunta en que les puedes ayudar"

El bot registra estas correcciones y se ajusta.

## Obtener ayuda

> "Como funciona esto?" — El bot explica sus propias capacidades
> "Que puedes hacer?" — Lista los comandos disponibles
