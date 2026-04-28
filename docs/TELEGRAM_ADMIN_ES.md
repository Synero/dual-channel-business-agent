# Guia de Admin en Telegram

Tu panel de control privado. Solo tu ID de usuario de Telegram puede acceder a estos comandos.

## Comandos diarios

| Comando | Que hace |
|---------|----------|
| `stock` | Muestra el inventario actual desde stock.json |
| `ventas hoy` | Consulta tu base de datos por las ventas de hoy (si esta conectado) |
| `pendientes` | Muestra deudas pendientes de clientes u ordenes abiertas |
| `que tengo hoy?` | Igual que stock, pero de forma conversacional |

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

Esto es genial cuando estas ocupado trabajando.

## Actualizaciones de personalidad

Si tu estilo cambia o quieres corregir al bot:

> "No digas 'okis' tan seguido"
> "Dime los precios siempre que alguien pregunte"
> "Cuando digan hola, pregunta en que les puedes ayudar"

El bot registra estas correcciones y se ajusta.

## Obtener ayuda

> "Como funciona esto?" — El bot explica sus propias capacidades
> "Que puedes hacer?" — Lista los comandos disponibles
