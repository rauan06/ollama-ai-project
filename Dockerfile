# Use the official ollama/ollama image as a base
FROM ollama/ollama

# Set up the volume and port
VOLUME /root/.ollama
EXPOSE 11434

# Start the container with the same settings as the provided command
CMD ["ollama"]
