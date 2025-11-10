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
    ('Vanilla Ice Cream Scoop', 1, 6.50, true),
    ('Chocolate Ice Cream Scoop', 1, 6.50, true),
    ('Strawberry Ice Cream Scoop', 1, 6.50, true),
    ('Mint Ice Cream Scoop', 1, 6.50, true),
-- Premium Ice Cream
    ('Belgian Chocolate Ice Cream Scoop', 2, 8.90, true),
    ('Salted Caramel Ice Cream Scoop', 2, 8.90, true),
    ('Pistachio Ice Cream Scoop', 2, 8.90, true),
-- Gelato
    ('Gelato Fragola', 3, 9.50, true),
    ('Gelato Limone', 3, 9.50, true),
    ('Gelato Nocciola', 3, 9.50, true),
-- Frozen Yogurt
    ('Natural Frozen Yogurt Cup', 4, 12.00, true),
    ('Berry Frozen Yogurt Cup', 4, 12.00, true),
-- Popsicle
    ('Fruit Popsicle - Mango', 5, 5.00, true),
    ('Fruit Popsicle - Strawberry', 5, 5.00, true),
    ('Chocolate Covered Popsicle', 5, 6.50, true),
-- Cone
    ('Classic Cone', 6, 2.00, true),
    ('Chocolate Dipped Cone', 6, 3.50, true),
    ('Waffle Cone', 6, 4.00, true),
-- Toppings
    ('Hot Fudge Topping', 7, 2.50, true),
    ('Caramel Syrup', 7, 2.50, true),
    ('Rainbow Sprinkles', 7, 1.50, true),
    ('Chopped Nuts', 7, 2.00, true),
    ('Whipped Cream', 7, 1.50, true),
-- Milkshake
    ('Vanilla Milkshake', 8, 15.00, true),
    ('Chocolate Milkshake', 8, 15.00, true),
    ('Strawberry Milkshake', 8, 15.00, true),
    ('Oreo Milkshake', 8, 18.00, true),
-- Dessert Cups
    ('Brownie Ice Cream Cup', 9, 18.00, true),
    ('Cookie Dough Ice Cream Cup', 9, 18.00, true),
-- Sundaes
    ('Classic Hot Fudge Sundae', 10, 16.00, true),
    ('Strawberry Sundae', 10, 16.00, true),
    ('Caramel Nut Sundae', 10, 17.50, true);

-- To Check if inserts succeeded
SELECT 
    P.ProductName,
    PC.CategoryName,
    P.UnitPrice
FROM Product P
INNER JOIN ProductCategory PC ON PC.CategoryId = P.CategoryId
LIMIT 10;