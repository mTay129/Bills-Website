const https = require('https');
const fs = require('fs');
const express = require('express');
const sql = require('mssql');
const cors = require('cors');

// Create Express app
const app = express();
const port = 3000; // Change port to avoid conflict with SQL Server's port

const helmet = require('helmet');

// Use helmet for security headers
app.use(helmet());
app.use(helmet.contentSecurityPolicy({
    directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "https://www.googletagmanager.com"],
        styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
        fontSrc: ["'self'", "https://fonts.gstatic.com"],
        imgSrc: ["'self'", "data:"],
        mediaSrc: ["'self'", "https://vimeo.com"],
        connectSrc: ["'self'", "https://www.googletagmanager.com"],
        formAction: ["'self'", "https://formspree.io"],
        objectSrc: ["'none'"],
        baseUri: ["'self'"]
    }
}));

// Enable CORS
app.use(cors());
app.options('*', cors());

// Parse incoming request bodies as JSON
app.use(express.json());

// Debug to test GET response
app.get('/', (req, res) => {
    res.send('Server is running!'); // Basic response for GET /
});

// Database configuration
const dbConfig = {
    server: '100-33-109-208\\SQLEXPRESS', // Server 
    user: 'test', // Replace with your username
    password: 'T#$7P@$$toor', // Replace with your password
    database: 'test_cust',
    options: {
        encrypt: true, // Use encryption if needed
        trustServerCertificate: true // For self-signed certificates
    },
    port: 53671, // Ensure the correct port number is used
};

// Initialize a single connection pool for the server
let poolPromise = sql.connect(dbConfig)
    .then(pool => {
        console.log('Connected to the database successfully!');
        return pool;
    })
    .catch(err => {
        console.error('Database connection error:', err.message);
        process.exit(1); // Exit process if connection fails
    });

// Endpoint for form submission
app.post('/submit', async (req, res) => {
    console.log('Endpoint /submit hit');
    console.log('Request Body:', req.body);

    const { firstName, lastName, phoneNumber, email, birthDate, country, state, city, birthPlace } = req.body;

    try {
        // Ensure birthDate is valid
        const parsedDate = new Date(birthDate);
        if (isNaN(parsedDate.getTime())) {
            return res.status(400).send('Invalid birthDate format.');
        }
        const formattedDate = parsedDate.toISOString().split('T')[0]; // Format to YYYY-MM-DD

        const pool = await poolPromise;

        // Insert into Customers table
        const customerQuery = `
            INSERT INTO Customers (FirstName, LastName, Email, PhoneNumber)
            OUTPUT INSERTED.CustomerID AS CustomerID
            SELECT
                ENCRYPTBYPASSPHRASE('encryption_key', @FirstName), 
                ENCRYPTBYPASSPHRASE('encryption_key', @LastName), 
                @Email, 
                @PhoneNumber
        `;

        const customerResult = await pool.request()
            .input('FirstName', sql.NVarChar, firstName)
            .input('LastName', sql.NVarChar, lastName)
            .input('Email', sql.NVarChar, email)
            .input('PhoneNumber', sql.NVarChar, phoneNumber)
            .query(customerQuery);

        const customerId = customerResult.recordset[0]?.CustomerID;
        if (!customerId) {
            throw new Error('Failed to retrieve Customer ID.');
        }

        // Insert into BirthDetails table
        const birthDetailsQuery = `
            INSERT INTO BirthDetails (CustomerID, BirthDate, BirthCountry, BirthState, BirthCity, BirthPlace)
            VALUES (@CustomerID, @BirthDate, @BirthCountry, @BirthState, @BirthCity, @BirthPlace);
        `;

        await pool.request()
            .input('CustomerID', sql.Int, customerId)
            .input('BirthDate', sql.Date, formattedDate)
            .input('BirthCountry', sql.NVarChar, country)
            .input('BirthState', sql.NVarChar, state)
            .input('BirthCity', sql.NVarChar, city)
            .input('BirthPlace', sql.NVarChar, birthPlace)
            .query(birthDetailsQuery);

        res.json({ customerId });


    } catch (err) {
        console.error('Error details:', err);
        res.status(500).send('An error occurred: ' + err.message);
    }
});

// Load SSL certificate and key for HTTPS
const privateKey  = fs.readFileSync('C:/inetpub/wwwroot/Website-Remake-main/certs/generated-private-key.txt', 'utf8');
const certificate  = fs.readFileSync('C:/inetpub/wwwroot/Website-Remake-main/certs/a497c345d24683ba.crt', 'utf8');
const ca = fs.readFileSync('C:/inetpub/wwwroot/Website-Remake-main/certs/gd-g2_iis_intermediates.pem', 'utf8');

// Create HTTPS server using the SSL credentials
const credentials = { 
    key: privateKey, 
    cert: certificate, 
    ca: ca 
};

// Create HTTPS server and link it to the Express app
https.createServer(credentials, app)
    .listen(8443, '0.0.0.0',() => {
        console.log(`Server running at https://208.109.33.100:8443`);
    });
