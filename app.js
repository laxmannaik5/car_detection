const express = require("express");
const bodyParser = require("body-parser");
const ejs = require("ejs");
const {spawn} = require('child_process');


const app =  express();

app.use(express.static("public"));
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({extended: true}));


app.get("/", function(req, res) {
  res.render("home");
});

app.get("/python", function(req, res){

  // var data;
  const python = spawn('python', ['script.py']);
  python.stdout.on('data', function (data) {
  data = data.toString();
  res.render("python", {data: data});
 });


});








app.listen(3000, function(){
  console.log("Server started on port 3000.");
});
