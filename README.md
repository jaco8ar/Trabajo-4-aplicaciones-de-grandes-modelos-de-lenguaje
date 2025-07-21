# Trabajo 4 aplicaciones de grandes modelos de lenguaje

---

## Descripción del proyecto

Aplicación web inteligente para generación de historias personalizadas mediante modelos de lenguaje.
Permite ingresar información estructurada o texto libre, seleccionar el género narrativo y generar historias con opción de refinarlas iterativamente.

Incluye validación semántica de entrada, generación por género, y exportación de historias.

---

## Enlaces útiles

- [Video demostrativo](https://drive.google.com/file/d/1CHmJ47aaH-BdLzQGIOM7pBrjJmWxmNDe/view?usp=drive_link)  
- [Informe técnico en QuartoPub](https://jochoara.quarto.pub/implementacion-del-agente-creativo-de-historias-con-llms/)  
- [Sitio web (Streamlit)](https://trabajo-4-aplicaciones-de-grandes-modelos-de-lenguaje-65wrdiam.streamlit.app/)


---

##  Estructura del repositorio

```
Trabajo-4-aplicaciones-de-grandes-modelos-de-lenguaje/
├── app/                                
│   ├── componentes/                    # Componentes visuales o lógicos (Streamlit)
│   ├── creador_de_historias/           # Lógica principal para generación de historias
│   ├── main.py                         # Punto de entrada para Streamlit
├── Historias-Generadas/                # Carpeta donde se guardan las historias generadas
├── Informe-Técnico/                    # Archivos fuente del informe técnico (Quarto)

```
## Prueba el proyecto

## Requisitos

- Python 3.8 o superior
- `pip` o entorno virtual como `.venv`

---

## Pasos para ejecutar el proyecto

###  Requisitos adicionales

Este proyecto hace uso de una clave de acceso de OpenAI proporcionada por la plataforma OpenRouter para acceder al agente de lenguaje. Si desea probar este repositorio de manera local puede proporcionar su propia clave y agregarla en un archivo .env bajo el nombre `OPENROUTER_API_KEY` una vez clone el repositorio.

### 1. Clona el repositorio

```bash
git clone https://github.com/jaco8ar/Trabajo-4-aplicaciones-de-grandes-modelos-de-lenguaje
cd Trabajo-4-aplicaciones-de-grandes-modelos-de-lenguaje
```

### 2. Crea y activa un entorno virtual

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt


# macOS/Linux
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

```bash
streamlit run app/main.py
```