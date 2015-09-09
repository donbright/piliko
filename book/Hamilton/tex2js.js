
var fs = require('fs');

infile = 'Quatern2.tex';
outfile = infile + '.js';

console.log('Hello World');

fs.readFile(infile,'utf-8',function(err,text) {
 if (err) throw err;
 var tmp = text;
 // italics
 tmp = tmp.replace(/\\\/}/g,'}');
 tmp = tmp.replace(/{.it ([\s\S]+?)}/g,'<i>$1</i>');
 // single $ (inline math) 
 tmp = tmp.replace(/\$\$([\s\S]+?)\$\$/g,'<mathjax>$1</mathjax>');
 tmp = tmp.replace(/\$([\s\S]+?)\$/g,'\\($1\\)');
 tmp = tmp.replace(/<mathjax>([\s\S]+?)<\/mathjax>/g,'$$$$$1$$$');

 fs.writeFile(outfile, tmp, function (err) {
  if (err) throw err;
 });
 console.log(tmp);
});

