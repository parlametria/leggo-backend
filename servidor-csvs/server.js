const express = require('express');
const serveIndex = require('serve-index');


const app = express();
const PORT = process.env.PORT = 8080;

app.use('/csvs', express.static('./agora-digital/exported'), serveIndex('./agora-digital/exported', {'icons': true}))

app.listen(PORT, () => {
  console.log('Server is running at:',PORT);
});