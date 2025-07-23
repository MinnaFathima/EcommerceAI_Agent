##🛒 E-Commerce AI Chatbot with Sales Analytics
This project is an AI-powered chatbot web application for an e-commerce platform. It allows users to query business metrics like Total Sales, ROAS (Return on Ad Spend), and Highest CPC via natural language and get interactive chart-based insights in response.

#💻 Features
Chat interface for querying e-commerce data

AI responds with relevant metrics

Charts rendered dynamically using Chart.js

REST API endpoints powered by Express.js

Data fetched from MySQL database

#🧰 Tech Stack
Frontend: HTML, JavaScript, Chart.js

Backend: Node.js, Express.js

Database: MySQL

Others: dotenv, CORS, body-parser

# 📁 Project Structure
bash
Copy
Edit
/project-root
│
├── server.js              # Express server and API routes
├── .env                   # Environment variables (e.g. PORT)
├── public/
│   └── index.html         # Frontend UI
├── script.js              # Handles chatbot logic and chart rendering
├── package.json
└── README.md              # This file
# ⚙️ Setup Instructions
# 1. Clone the repository
bash
Copy
Edit
git clone https://github.com/yourusername/ecommerce-ai-chatbot.git
cd ecommerce-ai-chatbot
# 2. Install dependencies
bash
Copy
Edit
npm install

# 3. Import Datasets
The required datasets (totalsalesandmetrics, adsalesandmetrics) are  imported into the MySQL ecommerce database.
Make sure your MySQL credentials in server.js match your setup:

js
Copy
Edit
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '****',
  database: 'ecommerce'
});

# 4. Start the server
bash
Copy
Edit
node server.js
You should see:
Server is running on port 5000

# 🌐 Access the App
Open index.html in your browser (you can double-click it or use Live Server in VS Code).

# 🔌 API Endpoints
Endpoint	Description
/api/total-sales	Returns total sales value
/api/roas	Returns ROAS (Ad Sales / Ad Spent)
/api/highest-cpc	Returns item with highest CPC

# 📊 Example Queries
"Show me total sales"

"What's the ROAS?"

"Which item has the highest CPC?"

# 📦 Future Enhancements
NLP integration using OpenAI API

Voice command support

User login and data segmentation

# 🙌 Acknowledgments
Node.js

Express

MySQL

Chart.js

📄 License
This project is licensed under the MIT License.
