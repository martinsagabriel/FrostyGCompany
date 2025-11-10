const pool = require('./db');

async function createSale(saleData) {
  const client = await pool.connect();

  try {
    await client.query('BEGIN');
    
    const saleResult = await client.query(
        `
        INSERT INTO "sale" 
        ("sellerid", "paymentmethod", "saledate")
      VALUES ($1, $2, NOW())
      RETURNING "saleid";
      `,
      [
          saleData.sellerId,
          saleData.paymentMethod.toUpperCase()
        ]
    );
    
    const saleId = saleResult.rows[0].saleid;

    console.log('Created sale with ID:', saleId);

    for (const item of saleData.items) {
      await client.query(
        `
        INSERT INTO "saleitem"
          ("saleid", "productid", "quantity")
        VALUES ($1, $2, $3);
        `,
        [saleId, item.productId, item.quantity]
      );
    }

    await client.query('COMMIT');
    return { saleId };

  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}

module.exports = { createSale };
