
import supertest from 'supertest';
import app from '../index.js';

const tester = supertest(app);

tester
    .post('/naughty')
    .send({ name: 'Bobby' })
    .expect(200)
    .set('Accept', 'application/json')
    .expect('Content-Type', /json/)
    .expect({
        name: 'Bobby',
    })
    .end((err, res) => {
        if (err) { console.error(err); }
    });

tester
    .post('/nice')
    .send({ name: 'Timmy' })
    .expect(200)
    .end((err, res) => {
        if (err) { throw err; }
    });

tester
    .get('/check')
    .set('Accept', 'application/json')
    .expect('Content-Type', /json/)
    .expect(200)
    .expect({
        name: 'Bobby',
        status: 'naughty',
    });

tester
    .get('/check')
    .set('Accept', 'application/json')
    .expect('Content-Type', /json/)
    .expect(200)
    .expect({
        name: 'Timmy',
        status: 'nice',
    });