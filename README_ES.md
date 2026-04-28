# Dual Channel Business Agent

> Clona tu personalidad real desde los DM de Instagram o crea una nueva desde cero y despliega un agente de ventas con IA para tu negocio.

**[Read in English](README.md)**

**Construido para negocios reales** — Un asistente que realmente suena como tú, no un chatbot corporativo.

Los chatbots genericos matan tu marca personal. Este agente aprende tu voz real, alimentado con mensajes reales de Instagram/WhatsApp. Puede atender clientes 24/7 mientras te enfocas en lo mas importante.

---

## El Problema

Los dueños de negocios viven en redes sociales (Instagram, WhatsApp, Facebook). Pero cuando estas vendiendo, horneando o simplemente ocupado, no puedes responder a todos. Y los asistentes de IA genericos suenan como call centers — los clientes se dan cuenta inmediatamente y se van.

## La Solucion

Una arquitectura de agente de doble canal que:

1. **Clona tu personalidad real** desde exportaciones de DM de Instagram (no es un script)
2. **Atiende clientes por WhatsApp** con tu voz real, tu jerga y tu ritmo
3. **Te da un panel de administracion en Telegram** para actualizar datos, revisar ventas y prender/apagar el bot
4. **Se adapta a tu tipo de negocio** con 6 modos incluidos: retail, services, freelance, SaaS, rentals, events
5. **Revisa operaciones de forma proactiva** para que el agente nunca prometa lo que no puedes entregar

---

## Arquitectura

```
+-----------------+     +------------------+     +-----------------+
|   WhatsApp      |     |   Hermes Agent   |     |    Telegram     |
|  (Clientes)     |<----|   Gateway        |---->|  (Dueno/Admin)  |
+-----------------+     +------------------+     +-----------------+
         |                        |                        |
         ▼                        ▼                        ▼
   Baileys Bridge          Motor de Personalidad        Control Admin
   (WhatsApp Web)          +-------------+          +-------------+
                           |  Instagram  |          |  Datos Modo |
                           |  DM Parser  |          |   Archivos  |
                           +-------------+          +-------------+
```

**Canales:**
- **WhatsApp** — Clientes. Calido, natural, clonado desde conversaciones reales.
- **Telegram** — Solo para el dueno. Actualizacion de datos, consulta de ventas, encendido/apagado del bot.

**Componentes principales:**
- `parse_instagram_export.py` — Extrae vocabulario, ritmo y patrones del export HTML de Meta
- `proactive_stock.py` — Cron diario que le pregunta al dueno por el estado operacional del dia
- Hermes Agent gateway — Orquestacion multi-plataforma con memoria persistente

---

## Requisitos

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) (gateway de IA multi-plataforma) — **Esto es requerido. Este repo es un skill/configuracion para Hermes Agent, no una app standalone.**
- Node.js + Baileys (bridge de WhatsApp Web)
- Python 3.9+
- Supabase (opcional, para seguimiento de ventas)

---

## Modos de Negocio

El agente se adapta a tu tipo de negocio con **6 modos incluidos**. Cada modo cambia el flujo de conversacion, el esquema de datos y los patrones operacionales:

| Modo | Para | El cliente dice | Datos clave |
|------|------|-----------------|-------------|
| **retail** | Vendedores de productos (comida, ropa, handmade) | "Quiero 2 de X y 1 de Y" | Catalogo, stock diario, pedidos, logistica de entrega |
| **services** | Negocios con citas (peluquerias, clinicas) | "Tienen hora para manana?" | Catalogo de servicios, calendario, citas |
| **freelance** | Profesionales por proyecto (diseno, dev) | "Cuanto me cobras por un logo?" | Servicios, proyectos, cotizaciones, hitos |
| **saas** | Suscripciones de software | "Quiero ver la posibilidad de una demo" | Planes, trials, tickets de soporte |
| **rentals** | Alquiler de equipos/propiedades | "Tienen disponible del 15 al 20?" | Inventario, disponibilidad, reservas, depositos |
| **events** | Organizadores de experiencias | "Quiero inscribirme al sabado" | Catalogo de eventos, reservas, lista de espera, capacidad |

Cada modo incluye:
- **MODE.md** — Descripcion, ejemplos, flujo de conversacion, patrones de pago
- **data-schema.json** — Archivos de datos estructurados que el agente lee/escribe
- **prompt-fragments.md** — Instrucciones especificas del modo para el LLM

---

## Inicio Rapido

> **La forma mas rapida:** Dile a tu Hermes Agent que lo configure por ti. Como ya tienes un agente de IA corriendo, deja que el maneje el clone, la config y el deploy.

### Setup Manual (si prefieres)

**1. Instala Hermes Agent**

```bash
pip install hermes-agent
# o sigue: https://github.com/NousResearch/hermes-agent#installation
```

**2. Clona este skill en tu directorio de Hermes**

```bash
cd ~/.hermes/skills/
git clone https://github.com/Synero/dual-channel-business-agent.git
cd dual-channel-business-agent
```

**3. Ejecuta el asistente de configuracion**

```bash
python scripts/setup_wizard.py
```

El wizard te entrevista para configurar tu negocio. Adapta las preguntas segun el modo que elijas (retail, services, freelance, SaaS, rentals o events). Genera:
- `generated_config/SOUL.md` — La personalidad de tu agente
- `generated_config/data/` — Archivos de datos especificos del modo (catalogo, calendario, proyectos, etc.)
- `generated_config/config.yaml` — Un snippet de config para Hermes Agent

**4. Apunta Hermes Agent a esta config**

Copia los archivos generados a tu directorio de Hermes Agent, o mezcla la config en tu `~/.hermes/config.yaml` existente.

**5. Inicia el gateway**

```bash
hermes gateway run
```

Tu agente se conecta a WhatsApp (via bridge de Baileys en puerto 3002) y Telegram.

---

### Opcion A: Clonar desde Instagram (Recomendado)

Si ya tienes conversaciones de Instagram/WhatsApp con clientes:

1. **Descarga tus datos de Instagram** → Ver [Guia de Exportacion de Meta](docs/META_EXPORT_GUIDE_ES.md)
2. **Ejecuta el parser:** `python scripts/parse_instagram_export.py /ruta/a/messages/ --business-name "Tu Nombre"`
3. **El wizard lo detecta automaticamente** cuando encuentra `personality_profile.json`

> O simplemente dile a tu Hermes Agent: *"Descarga mis datos de Instagram, parsealos y configura el agente de negocio por mi."*

### Opcion B: Crear Nueva Personalidad

Ejecuta el wizard y responde las preguntas. El agente te entrevista para construir la personalidad de tu negocio desde cero.

---

## Documentacion

- [Guia de Exportacion de Meta Account Center](docs/META_EXPORT_GUIDE_ES.md) — Como descargar tus DM de Instagram
- [Flujo de Onboarding](docs/ONBOARDING_ES.md) — Como el agente te entrevista para configurar el negocio
- [Guia de Admin en Telegram](docs/TELEGRAM_ADMIN_ES.md) — Comandos para el dueno

---

## Licencia

MIT — Construido con amor para negocios de todas partes.
