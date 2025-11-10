CREATE DATABASE IceCreamShop;

-- No PostgreSQL, conecte-se ao database antes de criar as tabelas
-- \c IceCreamShop

CREATE TABLE Store (
    StoreId SERIAL PRIMARY KEY,
    StoreName VARCHAR(150) NOT NULL,
    AddressLine VARCHAR(255) NOT NULL,
    City VARCHAR(120) NOT NULL,
    State VARCHAR(80) NOT NULL,
    ZipCode VARCHAR(20),
    Latitude DECIMAL(9,6),
    Longitude DECIMAL(9,6),
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Seller (
    SellerId SERIAL PRIMARY KEY,
    FirstName VARCHAR(120) NOT NULL,
    LastName VARCHAR(120) NOT NULL,
    BirthDate DATE NOT NULL,
    EmployeeCode VARCHAR(50) UNIQUE NOT NULL,
    PhoneNumber VARCHAR(30),
    DocumentNumber VARCHAR(50),
    StoreId INT NOT NULL,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (StoreId) REFERENCES Store(StoreId)
);

CREATE TABLE ProductCategory (
    CategoryId SERIAL PRIMARY KEY,
    CategoryName VARCHAR(150) NOT NULL,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Product (
    ProductId SERIAL PRIMARY KEY,
    ProductName VARCHAR(200) NOT NULL,
    CategoryId INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    IsActive BOOLEAN NOT NULL DEFAULT true,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CategoryId) REFERENCES ProductCategory(CategoryId)
);

CREATE TABLE Sale (
    SaleId BIGSERIAL PRIMARY KEY,
    StoreId INT NOT NULL,
    SellerId INT NOT NULL,
    SaleDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(12,2) NOT NULL,
    PaymentMethod VARCHAR(50),
    FOREIGN KEY (StoreId) REFERENCES Store(StoreId),
    FOREIGN KEY (SellerId) REFERENCES Seller(SellerId)
);

CREATE TABLE SaleItem (
    SaleItemId BIGSERIAL PRIMARY KEY,
    SaleId BIGINT NOT NULL,
    ProductId INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    LineTotal DECIMAL(12,2) GENERATED ALWAYS AS (Quantity * UnitPrice) STORED,
    FOREIGN KEY (SaleId) REFERENCES Sale(SaleId),
    FOREIGN KEY (ProductId) REFERENCES Product(ProductId)
);