# Factura SH

## Overview
This Django-based application processes billing requests from customers who made purchases on Mercado Libre. It provides an API for handling invoices, managing customer data, and integrating with external accounting services.

## Features
- Receives and processes billing requests.
- Validates customer and transaction data.
- Generates invoices in compliance with local tax regulations.
- Stores invoice records for future reference.
- Integrates with Mercado Libre's API to retrieve sales data.

## Requirements
- Python 3.8+
- Django 4+
- SQLite
- Mercado Libre API credentials

## Installation
```bash
# Clone the repository
git clone https://github.com/BalaamLeon/Factura-SH.git
cd Factura-SH

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

## Configuration
1. Create a `.env` file and set the following variables:
   ```env
   DJANGO_SECRET_KEY=your_secret_key
   DATABASE_URL=your_database_url
   MERCADO_LIBRE_CLIENT_ID=your_client_id
   MERCADO_LIBRE_CLIENT_SECRET=your_client_secret
   ```
2. Register your application in Mercado Libre to obtain API credentials.

## API Endpoints
### Create Invoice
**POST** `/api/invoices/`
- **Request Body:**
  ```json
  {
    "order_id": "123456789",
    "customer": {
      "name": "John Doe",
      "email": "john@example.com",
      "tax_id": "ABC12345"
    },
    "items": [
      {"name": "Product 1", "price": 100, "quantity": 2}
    ]
  }
  ```
- **Response:**
  ```json
  {
    "invoice_id": "INV-20240101-0001",
    "status": "generated",
    "pdf_url": "https://yourapp.com/invoices/INV-20240101-0001.pdf"
  }
  ```

## Testing
Run the tests using:
```bash
python manage.py test
```

## License
MIT License. See `LICENSE` file for details.
