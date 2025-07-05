require('dotenv').config();
const express = require('express');
const cors = require('cors');
const geminiRouter = require('./routes/gemini');

const app = express();
app.use(cors());
app.use('/api/gemini', geminiRouter);

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`🚀 contract-compare API listening on http://localhost:${port}`);
});
