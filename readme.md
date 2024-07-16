# Receipt Processor

This project is a simple web service that processes receipts and calculates points based on certain rules.

## Requirements

- Docker

## Running the Application

### Using Docker

1. **Build the Docker image:**
   Navigate to the root folder of this project and run this command:

   docker build -t receipt-processor .

2. **Run the docker image:**

   docker run -p 4000:4000 receipt-processor
