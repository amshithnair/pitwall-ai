FROM pitwall-base:latest

WORKDIR /app

# Copy the service code and its specific config
COPY templates/service/pyproject.toml templates/service/
COPY templates/service/src/ templates/service/src/

# Install the service
RUN uv pip install --system -e templates/service/

CMD ["uvicorn", "pitwall.template_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
