# Use this query to build the SQL Database
-- Create the database and switch to it
CREATE DATABASE ForBill;
GO
USE ForBill;
GO

-- Create a table to store customer personal details
CREATE TABLE Customers (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,   -- Automatically assigned customer number
    FirstName VARBINARY(255),                   -- Encrypted FirstName
    LastName VARBINARY(255),                    -- Encrypted LastName
    Email VARCHAR(255) UNIQUE NOT NULL,         -- Unique email as a secondary key
    PhoneNumber VARCHAR(15) UNIQUE NOT NULL     -- Unique phone number
);

-- Create a table to store customer birth details
CREATE TABLE BirthDetails (
    BirthDetailID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID INT NOT NULL,
    BirthDate DATE NOT NULL,
    BirthCountry VARCHAR(100),
    BirthState VARCHAR(100),
    BirthCity VARCHAR(100),
    BirthPlace VARCHAR(255),                    -- Hospital or midwife information
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE
);

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Sale Tax' AND TABLE_SCHEMA = 'dbo') 
BEGIN
    CREATE TABLE [dbo].[Sale Tax] (
        StateID INT PRIMARY KEY,
        StateName VARCHAR(50),
        SalesTaxRate DECIMAL(5, 2) -- Percentage
    );
END;

INSERT INTO [Sale Tax]
Values
(1, 'Alabama', 4.00),
(2, 'Alaska',0.00),
(3,'Arizona',5.60),
(4,'Arkansas',6.50),
(5,'California',7.25),
(6,'Colorado',2.90),
(7,'Connecticut',6.35),
(8,'Delaware',0.00),
(9,'Florida',6.00),
(10,'Georgia',4.00),
(11,'Hawaii',4.00),
(12,'Idaho',6.00),
(13,'Illinois',6.25),
(14,'Indiana',7.00),
(15,'Iowa',6.00),
(16,'Kansas',6.50),
(17,'Kentucky',6.00),
(18,'Louisiana',4.45),
(19,'Maine',5.50),
(20,'Maryland',6.00),
(21,'Massachusetts',6.25),
(22,'Michigan',6.00),
(23,'Minnesota',6.88),
(24,'Mississippi',7.00),
(25,'Missouri',4.23),
(26,'Montana',0.00),
(27,'Nebraska',5.50),
(28,'Nevada',6.85),
(29,'New Hampshire',0.00),
(30,'New Jersey',6.63),
(31, 'New Mexico',5.13),
(32,'New York', 4.00),
(33,'North Carolina',4.75),
(34,'North Dakota',5.00),
(35,'Ohio',5.75),
(36,'Oklahoma',4.50),
(37,'Oregon',0.00),
(38,'Pennsylvania',6.00),
(39,'Rhode Island',7.00),
(40,'South Carolina',6.00),
(41,'South Dakota',4.50),
(42,'Tennessee',7.00),
(43,'Texas',6.25),
(44,'Utah',4.85),
(45,'Vermont',6.00),
(46, 'Virginia',5.30),
(47,'Washington',6.50),
(48,'West Virginia',6.00),
(49,'Wisconsin',5.00),
(50, 'Wyoming',4.00),
(51,'District of Columbia',6.00)
