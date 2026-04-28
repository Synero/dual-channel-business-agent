#!/usr/bin/env node
/**
 * Standalone QR code generator for WhatsApp Baileys auth.
 *
 * Usage:
 *   node generate-qr.mjs
 *
 * Expects:
 *   - Baileys session directory at ../session (relative to this file)
 *   - npm install @whiskeysockets/baileys @hapi/boom pino qrcode
 *
 * Output:
 *   - Prints QR code to terminal
 *   - On successful scan, saves session to ../session/
 *   - Run once; session persists across reboots
 */

import { makeWASocket, useMultiFileAuthState, DisconnectReason } from '@whiskeysockets/baileys';
import { Boom } from '@hapi/boom';
import pino from 'pino';
import qrcode from 'qrcode';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SESSION_DIR = path.join(__dirname, '..', 'session');

const logger = pino({ level: 'silent' });

async function start() {
  const { state, saveCreds } = await useMultiFileAuthState(SESSION_DIR);

  const sock = makeWASocket({
    auth: state,
    logger,
    printQRInTerminal: false,
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('connection.update', async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      console.log('\n--- ESCANEA ESTE QR CON WHATSAPP BUSINESS ---');
      console.log('Ajustes > Dispositivos vinculados > Vincular\n');
      console.log(qr + '\n');
    }

    if (connection === 'open') {
      console.log('WhatsApp conectado! Sesion guardada en:', SESSION_DIR);
      process.exit(0);
    }

    if (connection === 'close') {
      const shouldReconnect = (lastDisconnect?.error instanceof Boom)
        ? lastDisconnect.error.output.statusCode !== DisconnectReason.loggedOut
        : true;
      if (shouldReconnect) {
        console.log('Reconectando...');
      } else {
        console.log('Sesion cerrada. Borra', SESSION_DIR, 'para re-vincular.');
        process.exit(1);
      }
    }
  });
}

start().catch(console.error);
