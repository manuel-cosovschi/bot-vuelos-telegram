# VolaBarato 🌏✈️

Bot de Telegram que te avisa automáticamente cuando hay vuelos baratos desde Buenos Aires hacia Japón o Estados Unidos (área Orlando/Miami), con revisión diaria y notificaciones.

---

## 📊 Características
- Scraping real desde Kiwi.com usando Selenium
- Búsqueda por rango de fechas para encontrar precios ocultos
- Comparación con umbral máximo definido por ruta
- Envió automático de alertas por Telegram
- Revisión diaria sin que el usuario tenga que hacer nada

---

## 🛠️ Requisitos

- Python 3.10 o superior
- Cuenta de Telegram
- Token de bot creado con @BotFather
- (Opcional) Cuenta de GitHub y Render para correrlo en la nube 24/7

---

## 📚 Instalación paso a paso (local)

### 1. Cloná o descargá este repositorio:
```bash
git clone https://github.com/TU_USUARIO/bot-vuelos-telegram.git
cd bot-vuelos-telegram
```

### 2. Crear y activar entorno virtual (opcional pero recomendado):
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### 4. Crear archivo `.env` con tu token:
```env
TELEGRAM_TOKEN=TU_TOKEN_DE_BOT_AQUI
```

### 5. Ejecutar el bot localmente:
```bash
python bot.py
```

### 6. Usar el bot en Telegram:
- Buscá: `@VolaBarato_bot`
- Enviá `/start` y luego `/alerta`

---

## ⏰ Automatización diaria
El bot ejecuta todos los días una búsqueda de vuelos automática gracias a `apscheduler`. No necesitás hacer nada, solo tenerlo corriendo.

---

## ☁️ Despliegue en Render (modo 24/7 gratis)

1. Subí este proyecto a un repositorio de GitHub (sin el archivo `.env`)
2. Creá cuenta en [https://render.com](https://render.com)
3. Seleccioná "New Web Service" y conectá tu repo
4. Configurá:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Environment Variables**: agregá `TELEGRAM_TOKEN`
   - **Instance Type**: Free

---

## 🎓 Rutas configuradas

### ✈️ Ruta 1: Buenos Aires → Japón
- Fechas: abril/mayo 2026 (21 días)
- Umbral: USD $1000 ida y vuelta

### ✈️ Ruta 2: Buenos Aires → Orlando/Miami
- Fechas: agosto/septiembre 2026 (14 días)
- Umbral: USD $300 ida y vuelta

---

## 🚀 Autor
Desarrollado por Manu (VolaBarato_bot en Telegram)

---

## 🔐 Seguridad
Este bot usa un archivo `.env` para guardar el token privado y nunca debe subirse a GitHub ni compartirse.

---
