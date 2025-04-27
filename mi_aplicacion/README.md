# 🐍 Aplicación Flask con Plantillas Dinámicas

Este proyecto es una práctica de la lección sobre sistemas de plantillas Front-End con Flask. La aplicación usa la herencia de plantillas con Jinja2 para mostrar datos dinámicos en páginas HTML organizadas.

---

## 📁 Estructura del Proyecto

```plaintext
mi_aplicacion/
│
├── app.py                  # Archivo principal que ejecuta la app Flask
├── static/                 # Archivos estáticos (CSS, imágenes, etc.)
│   └── styles.css
├── templates/              # Plantillas HTML con herencia Jinja2
│   ├── base.html
│   ├── index.html
│   ├── pagina1.html
│   └── pagina2.html
└── README.md               # Documentación del proyecto
```

---

## 🚀 ¿Qué hace esta aplicación?

- Muestra una **página principal** de bienvenida.
- Tiene una **página con una lista** de tecnologías (datos dinámicos).
- Tiene una **página con una tabla** de usuarios (datos dinámicos).
- Usa **plantillas HTML reutilizables** gracias a la herencia de Jinja2.
- Aplica estilos personalizados desde el archivo `styles.css`.

---

## ⚙️ Cómo ejecutar la aplicación

1. Asegúrate de tener Python instalado.
2. Instala Flask (si no lo tienes):
   ```bash
   pip install flask

3.Ejecuta el archivo principal: python app.py

4.Abre tu navegador en http://127.0.0.1:5000
