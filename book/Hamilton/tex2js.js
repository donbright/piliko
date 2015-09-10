// TeX2js.js by don bright http://patreon.com/umachine
// Convert a .tex file to javascript/html + mathjax for math
//
// See also
// http://nwalsh.com/tex/texhelp/Plain.html
// http://www.ucs.cam.ac.uk/docs/leaflets/u36
// http://www.tug.org/utilities/plain/cseq.html
//
// commandline testing:
//    $  node tex2js.js | less

var fs = require('fs');

infile = 'Quatern2.tex';
outfile = infile + '.js';

console.log('outfile:', outfile );
tex2jsheader = '<!-- Generated from ' + infile + ' by tex2js.js -->\n';
tex2jsheader += '<!-- Original file was: '+infile + ' -->\n';

fs.readFile(infile,'utf-8',function(err,text) {
 if (err) throw err;
 var tmp = text;
 // our header
 tmp = tex2jsheader + tmp;
 // comments
 tmp = tmp.replace(/(%.*)/g,"<!-- $1 -->");
 // macros
 macros = tmp.match(/\\def.*/g);
 console.log('macros:'+macros);
 // magnification... only deals with one setting for whole file.
 tmp = tmp.replace(/\\magnification=\\(.*)/g,".TeXmagnifiction { transform: scale($1); }");
 tmp = tmp.replace(/(: scale.*)(magstep0)/g,"$1"+1);
 tmp = tmp.replace(/(: scale.*)(magstephalf)/g,"$1"+1.095);
 tmp = tmp.replace(/(: scale.*)(magstep1)/g,"$1"+1.2);
 tmp = tmp.replace(/(: scale.*)(magstep2)/g,"$1"+1.44);
 tmp = tmp.replace(/(: scale.*)(magstep3)/g,"$1"+1.728);
 tmp = tmp.replace(/(: scale.*)(magstep4)/g,"$1"+2.074);
 tmp = tmp.replace(/(: scale.*)(magstep5)/g,"$1"+2.488);
 // ignore "italics correction", the \/ inside {.it} blocks
 tmp = tmp.replace(/\\\/}/g,'}');
 // italics
 tmp = tmp.replace(/{.it ([\s\S]+?)}/g,'<i>$1</i>');
 // single $ (inline math) to MathJax \( )\, whilst preserving $$ 
 tmp = tmp.replace(/\$\$([\s\S]+?)\$\$/g,'<mathjax>$1</mathjax>');
 tmp = tmp.replace(/\$([\s\S]+?)\$/g,'\\($1\\)');
 tmp = tmp.replace(/<mathjax>([\s\S]+?)<\/mathjax>/g,'$$$$$1$$$');
 // fonts
 tmp = tmp.replace(/\\font\\(.+?)=(.*)/g,
  '@font-face { \n\
    font-family: "$1" \n\
    font-weight: $2 \n\
    font-style: $2 \n\}'
 );
 fs.writeFile(outfile, tmp, function (err) {
  if (err) throw err;
 });
 //console.log(tmp);
});


