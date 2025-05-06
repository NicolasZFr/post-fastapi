# .devcontainer/Dockerfile o Dockerfile raíz, según tu setup

FROM python:3.11-slim

# 1. Crea grupo y usuario no-root
RUN groupadd --gid 1000 appuser \
 && useradd --uid 1000 --gid appuser --shell /bin/sh --create-home appuser
RUN apt-get update && apt-get install -y libpq-dev gcc


# 2. Establece el directorio de trabajo
WORKDIR /app

# 3. Copia requirements e instala paquetes (como root)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia el resto del código
COPY . .

# 5. Ajusta la propiedad de /app a appuser
RUN chown -R appuser:appuser /app

# 6. Cambia al usuario no-root
USER appuser

# 7. Exponer puerto y comando de arranque
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
