const express = require('express');
const cors = require('cors');
const mysql = require('mysql');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());

//  MySQL connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'pass123', 
  database: 'ecommerce' 
});

db.connect(err => {
  if (err) {
    console.error(' Error connecting to MySQL:', err);
    return;
  }
  console.log(' Connected to MySQL');
});

//  Example GET route
app.get('/', (req, res) => {
  res.send('E-commerce AI Agent is running 🚀');
});

//  Total Sales Query
app.get('/api/total-sales', (req, res) => {
  const query = 'SELECT SUM(`Total Sales`) AS total_sales FROM `totalsalesandmetrics`';
  db.query(query, (err, results) => {
    if (err) return res.status(500).send(err);
    res.json(results[0]);
  });
});

//  RoAS (Return on Ad Spend)
app.get('/api/roas', (req, res) => {
  const query = 'SELECT SUM(`Ad Sales`) / SUM(`Ad Spent`) AS roas FROM `adsalesandmetrics`';
  db.query(query, (err, results) => {
    if (err) return res.status(500).send(err);
    res.json(results[0]);
  });
});

//  Highest CPC
app.get('/api/highest-cpc', (req, res) => {
  const query = `
    SELECT \`item_id\`, MAX(\`ad_spent\` / NULLIF(\`clicks\`, 0)) AS highest_cpc
    FROM \`adsalesandmetrics\`
  `;
  db.query(query, (err, results) => {
    if (err) return res.status(500).send(err);
    res.json(results[0]);
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
