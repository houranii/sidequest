FROM python:3.9-slim

# Set environment variables for user and group
ENV USER_NAME=appuser
ENV USER_UID=1000
ENV USER_GID=1000

# Create the application group and user
RUN groupadd --gid $USER_GID $USER_NAME && \
    useradd --uid $USER_UID --gid $USER_GID --system $USER_NAME

WORKDIR /app

# Copy requirements and install
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Copy source code
COPY src ./src

# Run the app
CMD [ "python", "src/main.py"]
