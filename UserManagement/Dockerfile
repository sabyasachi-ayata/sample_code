#Docker file for web-socker server
# 1. Use official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Create a working directory
WORKDIR /app

# 4. Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the FastAPI app code
COPY Umbs.py ./umbs.py

# 6. Expose port (matches Uvicorn’s default)
EXPOSE 8000

# 7. Run the Uvicorn server
CMD ["uvicorn", "umbs:app", "--host", "0.0.0.0", "--port", "8000"]
