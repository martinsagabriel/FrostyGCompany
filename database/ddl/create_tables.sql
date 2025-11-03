CREATE DATABASE IceCreamShop;
GO

USE IceCreamShop;

CREATE TABLE Store (
    StoreId INT IDENTITY(1,1) PRIMARY KEY,
    StoreName VARCHAR(150) NOT NULL,
    AddressLine VARCHAR(255) NOT NULL,
    City VARCHAR(120) NOT NULL,
    State VARCHAR(80) NOT NULL,
    ZipCode VARCHAR(20),
    Latitude DECIMAL(9,6),
    Longitude DECIMAL(9,6),
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);

CREATE TABLE Seller (
    SellerId INT IDENTITY(1,1) PRIMARY KEY,
    FirstName VARCHAR(120) NOT NULL,
    LastName VARCHAR(120) NOT NULL,
    BirthDate DATE NOT NULL,
    EmployeeCode VARCHAR(50) UNIQUE NOT NULL,
    PhoneNumber VARCHAR(30),
    DocumentNumber VARCHAR(50),
    StoreId INT NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    FOREIGN KEY (StoreId) REFERENCES Store(StoreId)
);

CREATE TABLE ProductCategory (
    CategoryId INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName VARCHAR(150) NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);

CREATE TABLE Product (
    ProductId INT IDENTITY(1,1) PRIMARY KEY,
    ProductName VARCHAR(200) NOT NULL,
    CategoryId INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    FOREIGN KEY (CategoryId) REFERENCES ProductCategory(CategoryId)
);

CREATE TABLE Sale (
    SaleId BIGINT IDENTITY(1,1) PRIMARY KEY,
    StoreId INT NOT NULL,
    SellerId INT NOT NULL,
    SaleDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    TotalAmount DECIMAL(12,2) NOT NULL,
    PaymentMethod VARCHAR(50),
    FOREIGN KEY (StoreId) REFERENCES Store(StoreId),
    FOREIGN KEY (SellerId) REFERENCES Seller(SellerId)
);

CREATE TABLE SaleItem (
    SaleItemId BIGINT IDENTITY(1,1) PRIMARY KEY,
    SaleId BIGINT NOT NULL,
    ProductId INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    LineTotal AS (Quantity * UnitPrice) PERSISTED,
    FOREIGN KEY (SaleId) REFERENCES Sale(SaleId),
    FOREIGN KEY (ProductId) REFERENCES Product(ProductId)
);
