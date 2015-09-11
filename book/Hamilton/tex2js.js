// TeX2js.js by don bright http://patreon.com/umachine
// Convert a .tex file to javascript/html + mathjax for math
//
// See also:
//
// Basic TeX guides + reference:
// http://nwalsh.com/tex/texhelp/Plain.html
// http://www.ucs.cam.ac.uk/docs/leaflets/u36
// http://www.tug.org/utilities/plain/cseq.html
//
// Standard TeX Font names + meanings:
// http://ctan.sharelatex.com/tex-archive/fonts/cm/mf/
//
// Javascript + html:
// http://www.w3schools.com
//
// commandline testing:
//    $  node tex2js.js | less

var fs = require('fs');

infile = 'Quatern2.tex';
outfile = infile + '.js';

console.log('outfile:', outfile );
tex2jsheader = '<!-- Generated from ' + infile + ' by tex2js.js -->\n';
tex2jsheader += '<!-- Original file was: '+infile + ' -->\n';

// font map from TeX Metafont Computer Modern to .otf Computer-modern unicode
// TeX slanted = CSS oblique, TeX extended = CSS expanded
// for i in *.mf; do echo $i ; grep "Computer Modern" $i ; done 
// dic = [OTF version, stretch, weight, style, size in pts]
mfdic={}; 
mfdic['cmb10.mf']   = ["cmunbx.otf","normal","bold","normal",10];
mfdic['cmbsy10.mf'] = ["normal","bold","normal",10];
mfdic['cmbxsl10.mf'] = ["cmunbl.otf","expanded","bold","oblique",10];
mfdic['cmbxti10.mf'] = ["cmunbi.otf","expanded","bold","italic",10];
mfdic['cmitt10.mf']  = ["cmunit.otf","normal","normal","italic",10];
mfdic['cmmib10.mf']  = ["cmunbi.otf","normal","normal","italic",10];
mfdic['cmsltt10.mf'] = ["cmunst.otf","normal","normal","oblique",10];
for (i = 5; i<17; i++) { 
 mfdic['cmbx'+i+'.mf'] = ["cmunbx.otf","expanded","bold","normal",i];
 mfdic['cmmi'+i+'.mf'] = ["cmunti.otf","normal","normal","italic",i];
 mfdic['cmr'+i+'.mf'] =  ["cmunrm.otf","normal","normal","normal",i];
 mfdic['cmsl'+i+'.mf'] = ["cmunsl.otf","normal","normal","oblique",i];
 mfdic['cmss'+i+'.mf'] = ["cmunss.afm","normal","normal","normal",i];
}


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
    src: $2 \n\
    font-stretch: $2 \n\
    font-weight: $2 \n\
    font-style: $2 \n\}'
 );
 fs.writeFile(outfile, tmp, function (err) {
  if (err) throw err;
 });
 //console.log(tmp);
});


