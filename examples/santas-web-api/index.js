
import express from 'express';

const app = express();

app.post('/naughty', (req, res) => {
    // TODO - Implement the /naughty endpoint
    res.json({});
});

app.post('/nice', (req, res) => {
    // TODO - Implement the /nice endpoint
    res.json({});
});

app.get('/check', (req, res) => {
    // TODO - Implement the /check endpoint
    res.json({});
});

export default app;