# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a FacturaFlow! Este documento proporciona pautas para contribuir al proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo Contribuir?](#cómo-contribuir)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)
- [Pull Requests](#pull-requests)
- [Estilo de Código](#estilo-de-código)

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código.

### Nuestros Estándares

- ✅ Uso de lenguaje acogedor e inclusivo
- ✅ Respeto a diferentes puntos de vista y experiencias
- ✅ Aceptación de críticas constructivas
- ✅ Enfoque en lo mejor para la comunidad

## 🚀 ¿Cómo Contribuir?

### 1. Fork del Repositorio

```bash
# Clona tu fork
git clone https://github.com/TU_USUARIO/facturaflow.git
cd facturaflow
```

### 2. Crea una Rama

```bash
# Crea una rama para tu feature/fix
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
```

### 3. Realiza tus Cambios

- Escribe código limpio y documentado
- Sigue las convenciones de estilo
- Agrega tests si es posible
- Actualiza la documentación

### 4. Commit

```bash
git add .
git commit -m "feat: descripción breve del cambio"
```

#### Convención de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato, punto y coma faltantes, etc
- `refactor:` Refactorización de código
- `test:` Agregar tests
- `chore:` Actualización de tareas, configuración, etc

### 5. Push y Pull Request

```bash
git push origin feature/nueva-funcionalidad
```

Luego crea un Pull Request en GitHub.

## 🐛 Reportar Bugs

### Antes de Reportar

1. ✅ Verifica que no exista un issue similar
2. ✅ Asegúrate de usar la última versión
3. ✅ Verifica que el problema sea reproducible

### Template de Bug Report

```markdown
**Descripción del Bug**
Una descripción clara y concisa del bug.

**Pasos para Reproducir**
1. Ir a '...'
2. Hacer clic en '...'
3. Ver error

**Comportamiento Esperado**
Lo que esperabas que sucediera.

**Screenshots**
Si aplica, agrega screenshots.

**Entorno**
- OS: [ej. Windows 11]
- Python: [ej. 3.10]
- Navegador: [ej. Chrome 120]
```

## 💡 Sugerir Mejoras

### Template de Feature Request

```markdown
**¿El feature está relacionado con un problema?**
Una descripción clara del problema. Ej. "Siempre me frustra cuando..."

**Describe la solución que te gustaría**
Una descripción clara de lo que quieres que suceda.

**Describe alternativas consideradas**
Alternativas que has considerado.

**Contexto adicional**
Agrega cualquier otro contexto o screenshots.
```

## 🔀 Pull Requests

### Checklist

Antes de enviar tu PR, verifica:

- [ ] El código sigue el estilo del proyecto
- [ ] Has actualizado la documentación
- [ ] Has agregado tests (si aplica)
- [ ] Todos los tests pasan
- [ ] El commit sigue las convenciones
- [ ] Has actualizado el CHANGELOG.md

### Proceso de Revisión

1. Un maintainer revisará tu PR
2. Pueden solicitar cambios
3. Una vez aprobado, será merged

## 🎨 Estilo de Código

### Python (Backend)

```python
# Usa PEP 8
# Nombres descriptivos
# Docstrings para funciones

def calcular_total_factura(monto: float, impuesto: float) -> float:
    """
    Calcula el total de una factura incluyendo impuestos.
    
    Args:
        monto: Monto base de la factura
        impuesto: Porcentaje de impuesto (0-100)
    
    Returns:
        Total de la factura con impuestos
    """
    return monto * (1 + impuesto / 100)
```

### JavaScript (Frontend)

```javascript
// Usa camelCase
// Nombres descriptivos
// Comentarios para lógica compleja

async function cargarFacturas() {
    try {
        const response = await fetch(`${API_URL}/facturas/`);
        const facturas = await response.json();
        return facturas;
    } catch (error) {
        console.error('Error al cargar facturas:', error);
        throw error;
    }
}
```

### CSS

```css
/* Usa nombres de clase descriptivos */
/* Organiza por componentes */
/* Comenta secciones importantes */

/* Header principal */
.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
```

## 🧪 Tests

### Ejecutar Tests

```bash
# Backend
cd backend
pytest

# Frontend (si aplica)
cd frontend
npm test
```

## 📞 Contacto

Si tienes preguntas:

- 📧 Abre un issue
- 💬 Comenta en un issue existente

## 🙏 Agradecimientos

¡Gracias por contribuir a FacturaFlow!

---

**Última actualización:** Enero 2026
