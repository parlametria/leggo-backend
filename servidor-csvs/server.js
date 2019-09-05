var cookieParser = require('cookie-parser');
var logger = require('morgan');
const helmet = require('helmet');
const express = require('express');
const serveIndex = require('serve-index');
require('dotenv-safe').config();
var jwt = require('jsonwebtoken');
const app = express();
const PORT = process.env.PORT = 8080;

app.use(logger('dev'));
app.use(helmet());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

function verifyJWT(req, res, next){
  var token = req.headers['x-access-token'];
  if (!token) return res.status(401).send({ auth: false, message: 'No token provided.' });
  
  jwt.verify(token, process.env.SECRET, function(err, decoded) {
    if (err) return res.status(500).send({ auth: false, message: 'Failed to authenticate token.' });
    
    // se tudo estiver ok, salva no request para uso posterior
    req.userId = decoded.id;
    next();
  });
}

app.use('/csvs',verifyJWT, express.static('./agora-digital/exported'), serveIndex('./agora-digital/exported', {'icons': true}))

app.listen(PORT, () => {
  console.log('Server is running at:',PORT);
});

app.post('/login', (req, res, next) => {
  if(req.body.user === 'luiz' && req.body.pwd === '123'){
    //auth ok
    const id = 1; //esse id viria do banco de dados
    var token = jwt.sign({ id }, process.env.SECRET, {
      expiresIn: 300 // expires in 5min
    });
    res.status(200).send({ auth: true, token: token });
  }else {
    res.status(500).send('Login inválido!'); 
  }
});

app.get('/logout', function(req, res) {
  res.status(200).send({ auth: false, token: null });
});
