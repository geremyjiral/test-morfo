FROM python:3.12-slim-bullseye

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen
#--no-cache
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "src/main.py"]
