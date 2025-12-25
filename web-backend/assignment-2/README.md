# Assignment 2 – API Integration (Node.js + Express)

## Project Overview
This project was created as part of **Assignment 2 (API Integration)**.  
The goal of the assignment is to practice working with **server-side APIs**, processing data, and displaying it on the frontend using a clean and structured approach.

The application retrieves a **random user**, fetches **country information**, **exchange rates**, and **news headlines** related to the user's country.  
All API calls are handled **only on the server side**, and the frontend receives already processed and cleaned data.

---

## Technologies Used
- Node.js
- Express.js
- Axios
- HTML, CSS, JavaScript
- dotenv (for environment variables)

---

## APIs Used
1. **Random User Generator API**  
   https://randomuser.me/api/

2. **REST Countries API**  
   https://restcountries.com/

3. **ExchangeRate API**  
   https://www.exchangerate-api.com/

4. **News API**  
   https://newsapi.org/


---

## Features

### 1. Random User Information
After clicking the **"Get random user"** button, the server:
- Requests a random user from RandomUser API
- Extracts and sends to frontend:
    - First name
    - Last name
    - Gender
    - Profile picture
    - Age
    - Date of birth
    - City
    - Country
    - Full address (street name and number)

The user information is displayed as a **profile card** with labeled fields.

---

### 2. Country Information (REST Countries API)
Using the country obtained from the Random User API, the server retrieves:
- Country name
- Capital city
- Official language(s)
- Currency
- National flag

Only the required and cleaned data is sent to the frontend.

Missing data is handled gracefully and shown as **"N/A"**.

---

### 3. Exchange Rates
Based on the user's country currency:
- The server fetches exchange rates
- Displays comparison with:
    - USD (United States Dollar)
    - KZT (Kazakhstani Tenge)

**Example:**

1 DKK = 0.1579 USD
1 DKK = 81.0533 KZT


The exchange rate section is shown near the country information.

---

### 4. News Headlines (News API)
The server fetches **5 English news headlines** related to the user's country:
- The headline title must contain the country name
- Each article includes:
    - Title
    - Image (if available)
    - Short description
    - Source link to the full article

News articles are displayed using cards for better readability.

---

## Server-Side Logic
- All API requests are handled **only on the server**
- Frontend communicates with a single endpoint:


> ⚠️ The `.env` file should not be committed to GitHub.

---

## Installation and Running the Project

1. Install dependencies:
```bash
npm install

node server.js