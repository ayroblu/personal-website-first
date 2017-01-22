document.getElementsByTagName('body')[0].onclick = function() {
    //clearTimeout(animation)
    //if (runFancy) {
    //    hack.style.width = '';
    //    hack.setAttribute("style","width:");
    //    hack.className = "text explode";
    //    setTimeout('implode()',500);
    //} else {
    //    goHome();
    //}
    hack.className = "text type inter";
    //animation = setTimeout('cssfadep2()',10);
    clearTimeout(animation)
    animation = setTimeout(function(){
        hack.className = "text fade";
        animation = setTimeout(function(){
          window.location.href = "/details";
        }, 2000)
        //animation = setTimeout('animateText()', 2200);
    },10);
}
window.onload = function() {
    hack.style.opacity = '';
    if (runFancy) {
        hack.style.color = 'transparent';
    }
    animateText();
    blink();
}
var index = 0;
var animation;
function animateText() {
    if (index < messages.length) {
        hack.className = "text type";
        hack.innerHTML = '<blinks>\u2588</blinks>';
        var string = messages[index++];
        hiddenhack.innerHTML = string.concat('\u2588');
        hack.style.width = hiddenhack.offsetWidth+1;
        hack.setAttribute("style","width:"+(hiddenhack.offsetWidth+1)+"px");
        hiddenhack.innerHTML = '';
        animation = setTimeout(''.concat('type("',string,'", 0)'),2000);
    }
}
function type(string, i) {
    var cursor = (++i == string.length) ? '<blinks>\u2588</blinks>' : '\u2588';
    hack.innerHTML = string.substring(0,i).concat(cursor);
    if (i < string.length) {
        animation = setTimeout(''.concat("type(\"",string,"\",",i,")"), 100);
    } else if (index < messages.length) {
        if (runFancy) {
            //setTimeout('blurfade(0)',1500);
            animation = setTimeout('cssfade()',1500);
        } else {
            animation = setTimeout('fade(1)',1500);
            //setTimeout('cssfade()',1500);
        }
    }
}
function fade(opacity) {
    hack.style.opacity=opacity;
    hack.style.filter="alpha(opacity="+opacity*100+")";
    opacity -= 0.02;
    if (opacity > 0) {
        animation = setTimeout(''.concat("fade(",opacity,")"), 20);
    } else {
        hack.style.opacity=1;
        hack.style.filter="alpha(opacity=100)";
        animateText();
    }
}
function cssfade() {
    hack.className = "text type inter";
    //animation = setTimeout('cssfadep2()',10);
    animation = setTimeout(function(){
        hack.className = "text fade";
        animation = setTimeout('animateText()', 2200);
    },10);
}
function blink() {
    var blinks = document.getElementsByTagName('blinks');
    for (var i = blinks.length - 1; i >= 0; i--) {
        var s = blinks[i];
        s.style.visibility = (s.style.visibility === 'visible') ? 'hidden' : 'visible';
    }
    setTimeout(blink, 400);
}
function implode() {
    hack.className = "text implode";
    setTimeout('goHome()',700);
}
function goHome() {
    window.location.href = "/home";
}
