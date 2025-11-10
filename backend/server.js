const express = require('express');
const { createSale } = require('./salesService');

const app = express();
app.use(express.json());

app.post('/sales', async (req, res) => {
  try {
    const result = await createSale(req.body);
    res.status(201).json({
      message: "Sale created successfully",
      saleId: result.saleId
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app

app.listen(3000, () => {
  console.log('API running on port 3000');
});
