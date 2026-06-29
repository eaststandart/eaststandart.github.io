# eststandart.github.io

A website for those who want to know how everything works and build technology with their own hands.

Сайт для тех, кто хочет знать как все устроено и создавать технологии своими руками.

### Структура проекта

```
eaststandart.github.io/
├── _includes              Код на языке liquid
│   ├── discus.liquid
│
├── _layouts               Шаблоны страниц
│
├── core/
│   ├── encryption.py      All crypto: XSalsa20-Poly1305, ChaCha20-Poly1305, X25519, Ed25519, BLAKE2b
│   ├── ratchet.py         Sender Keys forward secrecy: SenderChain + RatchetState
│   ├── animation.py       CRT boot and ratchet activation animations with SFX
│   ├── sounds.py          Cross-platform sound playback (WAV/MP3, Linux/macOS/Windows)
│   ├── identity.py        Ed25519 keypair generation and TOFU pubkey store
│   ├── utils.py           Terminal output, ANSI colours, TUI chrome
│   └── config.py          Configuration loading and CLI parsing
│
├── network/
│   ├── server.py          Async zero-metadata blind-forwarder server
│   ├── client.py          Terminal chat client (E2E, DH, TOFU, file transfer)
│   ├── client_ratchet.py  RatchetMixin — /ratchet command flow, migration wait
│   ├── client_dh.py       X25519 DH handshake mixin
│   ├── client_send.py     Outgoing message encryption (static + ratchet paths)
│   ├── client_recv.py     Incoming frame routing and decryption
│   └── client_commands.py Input loop, command dispatch, help
│
├── ui/
│   ├── launch.py          Guided launcher, arrow-key menu UI
│   └── setup.py           Dependency wizard, auto-installs what's needed
│
├── install/
│   ├── install.sh         Bootstrap for Linux / macOS / Termux / iSH
│   ├── install.bat        Bootstrap for Windows (CMD and PowerShell)
│   ├── install.py         Cross-platform Python installer
│   └── uninstall.py       Remove all NoEyes dependencies for clean reinstall
│
├── docs/
│   ├── README.md          This file
│   └── CHANGELOG.md       Version history
│
├── update.py              Self-updater, pulls latest from GitHub
└── sfx/                   Notification sounds
```
