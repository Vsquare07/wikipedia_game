# Use a standard Python image
FROM python:3.13.5

# Set the working directory
WORKDIR /app

# Copy your requirements file
COPY requirements.txt .

# Install your dependencies plus the production server
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the rest of your project (app.py, model.py, static, templates)
COPY . .

# Hugging Face Spaces ALWAYS requires apps to run on port 7860
EXPOSE 7860

# Start the Flask app using Gunicorn on port 7860
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]