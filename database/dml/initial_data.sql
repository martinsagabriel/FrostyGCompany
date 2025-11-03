INSERT INTO ProductCategory (CategoryName)
VALUES
    ('Ice Cream'),
    ('Premium Ice Cream'),
    ('Gelato'),
    ('Frozen Yogurt'),
    ('Popsicle'),
    ('Cone'),
    ('Topping'),
    ('Milkshake'),
    ('Dessert Cup'),
    ('Sundae');

INSERT INTO Product (ProductName, CategoryId, UnitPrice, IsActive)
VALUES
    -- Ice Cream
    ('Vanilla Ice Cream Scoop', 1, 6.50, 1),
    ('Chocolate Ice Cream Scoop', 1, 6.50, 1),
    ('Strawberry Ice Cream Scoop', 1, 6.50, 1),
    ('Mint Ice Cream Scoop', 1, 6.50, 1),

    -- Premium Ice Cream
    ('Belgian Chocolate Ice Cream Scoop', 2, 8.90, 1),
    ('Salted Caramel Ice Cream Scoop', 2, 8.90, 1),
    ('Pistachio Ice Cream Scoop', 2, 8.90, 1),

    -- Gelato
    ('Gelato Fragola', 3, 9.50, 1),
    ('Gelato Limone', 3, 9.50, 1),
    ('Gelato Nocciola', 3, 9.50, 1),

    -- Frozen Yogurt
    ('Natural Frozen Yogurt Cup', 4, 12.00, 1),
    ('Berry Frozen Yogurt Cup', 4, 12.00, 1),

    -- Popsicle
    ('Fruit Popsicle - Mango', 5, 5.00, 1),
    ('Fruit Popsicle - Strawberry', 5, 5.00, 1),
    ('Chocolate Covered Popsicle', 5, 6.50, 1),

    -- Cone
    ('Classic Cone', 6, 2.00, 1),
    ('Chocolate Dipped Cone', 6, 3.50, 1),
    ('Waffle Cone', 6, 4.00, 1),

    -- Toppings
    ('Hot Fudge Topping', 7, 2.50, 1),
    ('Caramel Syrup', 7, 2.50, 1),
    ('Rainbow Sprinkles', 7, 1.50, 1),
    ('Chopped Nuts', 7, 2.00, 1),
    ('Whipped Cream', 7, 1.50, 1),

    -- Milkshake
    ('Vanilla Milkshake', 8, 15.00, 1),
    ('Chocolate Milkshake', 8, 15.00, 1),
    ('Strawberry Milkshake', 8, 15.00, 1),
    ('Oreo Milkshake', 8, 18.00, 1),

    -- Dessert Cups
    ('Brownie Ice Cream Cup', 9, 18.00, 1),
    ('Cookie Dough Ice Cream Cup', 9, 18.00, 1),

    -- Sundaes
    ('Classic Hot Fudge Sundae', 10, 16.00, 1),
    ('Strawberry Sundae', 10, 16.00, 1),
    ('Caramel Nut Sundae', 10, 17.50, 1);

-- To Check if inserts is sucessed
SELECT TOP 10 
	P.PRODUCTNAME,
	PC.CATEGORYNAME,
	P.UNITPRICE
FROM Product P
INNER JOIN ProductCategory PC ON PC.CATEGORYID = P.CATEGORYID