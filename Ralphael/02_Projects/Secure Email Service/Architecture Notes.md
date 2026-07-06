# Secure Email Service Architecture Notes

Generated: 2026-06-14

## Folder Structure

- `(root)`: 9 indexed files
- `frontend`: 11 indexed files
- `symbolic_mersenne_cracker`: 2 indexed files

## Likely Architecture

- Stack: Node.js / JavaScript, Python, Docker
- Source root: `C:\Users\cyber\Downloads\secure-email-service`
- Tests detected: No

## README Signals

### `symbolic_mersenne_cracker/README.md`

# SymRandCracker ## Models the mersenne twister used by Python Random as a symbolic program. ## This allows recovering the state given a few outputs, even if they are truncated! See function `test` for an example interaction with the module. This was approved by STT (https://sectt.github.io/) , so you know it is good.

## Package / Build Signals

### `docker-compose.yml`

```text
services: ses: build: . restart: always ports: - '8000:8000' init: true redis: image: redis:7.2.4-alpine restart: always
```
### `frontend/package.json`

```text
{ "name": "frontend", "private": true, "version": "0.0.0", "type": "module", "scripts": { "dev": "vite", "build": "vite build", "preview": "vite preview" }, "devDependencies": { "vite": "^6.0.5" }, "dependencies": { "@bjorn3/browser_wasi_shim": "^0.3.0", "axist": "^0.0.4" } }
```
### `requirements.txt`

```text
fastapi==0.115.6 uvicorn==0.34.0 jinja2==3.1.5 redis==5.2.1 cryptography==44.0.0 python-smail==0.9.0 playwright==1.49.1 oscrypto@git+https://github.com/wbond/oscrypto.git@d5f3437 z3-solver
```
