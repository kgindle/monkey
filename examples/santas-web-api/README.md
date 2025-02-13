
# Santa's Web API

This is a simple web API that allows you to interact with Santa's naughty and
nice list. The API provides the following endpoints:

- `POST /naughty` - Add a child to the naughty list.
- `POST /nice` - Add a child to the nice list.
- `GET /check` - Check if a child is on the naughty or nice list.

## Usage

To use the API, you can send HTTP requests to the endpoints using a tool like `curl` or Postman. Here are some examples:

### Add a child

To add a child to the naughty list, send a POST request to `/naughty` with the
child's name as the `name` parameter in the request body.

```bash
curl -X POST http://santa/naughty -d '{"name": "Tom"}'
```

To add a child to the nice list, send a POST request to `/nice` with the child's
name as the `name` parameter in the request body.

```bash
curl -X POST http://santa/nice -d '{"name": "Alice"}'
```

### Check if a child is on the list

To check if a child is on the naughty or nice list, send a GET request to `/check`
with the child's name as the `name` parameter in the query string.

```bash
curl http://santa/check?name=Tom
```

The response will be a JSON object with the child's name and status.
    
```json
{
"name": "Tom",
"status": "naughty"
}
```

## Built With

- [Express.js](https://expressjs.com/) - Web framework for Node.js. Santa's Web
  API uses it to process HTTP requests.