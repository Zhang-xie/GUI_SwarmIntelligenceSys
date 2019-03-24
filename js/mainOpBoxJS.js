/*
    This program allows user to draw line on the webpage
    Everytime a new line is drawn, the webpage will automatically draw a rectangle that record the range of the path of the line
*/


window.onerror = function() {
    // alert(error.message);
    alert("error");
}


// Initialize canvas
var mainCanvas = document.getElementById("mainCanvas"),
    mainCanvasContext = mainCanvas.getContext("2d");

var frontCanvas = document.getElementById("frontCanvas"),
    frontCanvasContext = frontCanvas.getContext("2d");

//Set the size of the canvas to the size of the window
var errorWidth = 30;    //For some reason, when dragging the scroll bar, the coordinate will change
var windowWidth = mainCanvas.width = window.innerWidth - errorWidth,
    windowHeight = mainCanvas.height = window.innerHeight - errorWidth;

frontCanvas.width = windowWidth;
frontCanvas.height = windowHeight;


//Record the range of the path of the mouse
var maxX = 0, maxY = 0, minX = windowWidth, minY = windowHeight;

var drawLineWidth = 3.0,
    drawLineColor = "rgb(0,128,255)";
var rectLineWidth = 3.0,
    rectLineColor = "rgb(255,127,0)";


var initColor = "rgb(255, 255, 255)";
mainCanvasContext.fillStyle = initColor;
mainCanvasContext.fillRect(0, 0, windowWidth, windowHeight);


var grayColor = "rgb(128, 128, 128, 0.4)";



//Trigger the function if the mouse is clicked
frontCanvas.onmousedown = function(e) {
    //Clear the previously drawn line
    mainCanvas.width = window.innerWidth - errorWidth;
    mainCanvas.height = window.innerHeight - errorWidth;
   	mainCanvasContext.fillStyle = initColor;
	mainCanvasContext.fillRect(0, 0, windowWidth, windowHeight);

    var e = e || event;

    //Make sure the two lines are seperated
    var ox = e.clientX - mainCanvas.offsetLeft;
    var oy = e.clientY - mainCanvas.offsetTop;
    mainCanvasContext.moveTo(ox,oy);

    minX = maxX = ox;
    minY = maxY = oy;

    //Trigger the function if the mouse is moving while being clicked
    document.onmousemove = function(e){
        var ox2 = e.clientX - mainCanvas.offsetLeft;
        var oy2 = e.clientY - mainCanvas.offsetTop;

        //Record the range of the path of the mouse
        minX = (ox2 < minX) ? ox2 : minX;
        maxX = (ox2 > maxX) ? ox2 : maxX;
        minY = (oy2 < minY) ? oy2 : minY;
        maxY = (oy2 > maxY) ? oy2 : maxY;

        mainCanvasContext.lineTo(ox2,oy2);  //Draw the line between previous and present coordinate
        mainCanvasContext.strokeStyle = drawLineColor;    //Set the color of the following point
        mainCanvasContext.lineWidth = drawLineWidth;    //Set the width of the following point
        mainCanvasContext.stroke();
    }

    document.onmouseup  = function(e){
        //Make sure the line is ended
        document.onmousemove = null;
        document.onmouseup = null;

        //Draw the rectangle displaying the range of the path of the mouse
        if(minX != maxX || minY != maxY) {
            minX = (minX - rectLineWidth < 0) ? minX : minX - rectLineWidth;
            maxX = (maxX + rectLineWidth >= windowWidth) ? maxX : maxX + rectLineWidth;
            minY = (minY - rectLineWidth < 0) ? minY : minY - rectLineWidth;
            maxY = (maxY + rectLineWidth >= windowHeight) ? maxY : maxY + rectLineWidth;
            // mainCanvasContext.strokeStyle = rectLineColor;
            // mainCanvasContext.lineWidth = rectLineWidth;
            // mainCanvasContext.strokeRect(minX, minY, maxX-minX, maxY-minY);
            // mainCanvasContext.fillRect(minX, minY, maxX-minX, maxY-minY);    //This line will draw a solid rectangle



            var mainCanvasImg = mainCanvasContext.getImageData(minX, minY, maxX - minX, maxY - minY);

            for(var i = 0; i < mainCanvasImg.width; ++i)
            	recurseChangeColor(mainCanvasImg, 1, i);
            for(var i = 0; i < mainCanvasImg.width; ++i)
            	recurseChangeColor(mainCanvasImg, mainCanvasImg.height - 2, i);
            for(var i = 0; i < mainCanvasImg.height; ++i)
            	recurseChangeColor(mainCanvasImg, i, 1);
            for(var i = 0; i < mainCanvasImg.height; ++i)
            	recurseChangeColor(mainCanvasImg, i, mainCanvasImg.width - 2);

            getInsideArea(mainCanvasImg);

            mainCanvasContext.putImageData(mainCanvasImg, minX, minY);
        }
    }
}







//This function antiOverflow can avoid overflow by transferring recursion to loop
function antiOverflow(f) {
    var value;
    var active = false;
    var accumulated = [];
    return function accumulator() {
        accumulated.push(arguments);    //Push a new element and return the length
        if (!active) {
            active = true;
            while (accumulated.length)
                value = f.apply(this, accumulated.shift()); //Function shift() delete the first element and return it
            active = false;
            return value;
        }
    };
}

//Change the external color using depth-first search
var recurseChangeColor = antiOverflow(function(canvasImg, corX, corY) {
    for(var i = -1; i < 2; ++i) {
        if(corX + i < 0 || corX + i >= canvasImg.height)
            break;
        for(var j = -1; j < 2; ++j) {
            if(i == 0 && j == 0)
                break;
            if(corY + j < 0 || corY + j >= canvasImg.width)
                break;
            var x = (corX+i)*4*canvasImg.width + 4*(corY+j);
            if(canvasImg.data[x] == 255 && canvasImg.data[x+1] == 255 && canvasImg.data[x+2] == 255) {
                canvasImg.data[x+2] = 254;
                recurseChangeColor(canvasImg, corX+i, corY+j);
            }
        }
    }
});

function getInsideArea(canvasImg) {
	for(var i = 1; i < canvasImg.height - 1; ++i) {
		for(var j = 1; j < canvasImg.width - 1; ++j) {
			 var x = i*4*canvasImg.width + 4*j;
            if(canvasImg.data[x] == 255 && canvasImg.data[x+1] == 255) {
            	if(canvasImg.data[x+2] == 255) {
	                canvasImg.data[x] = 128;
	                canvasImg.data[x+1] = 128;
	                canvasImg.data[x+2] = 128;
	            }
	            else
	            	canvasImg.data[x+2] = 255;
            }
		}
	}
}




// mainCanvas.onmousemove = function(e) {
//     var ox = e.clientX - mainCanvas.offsetLeft;
//     var oy = e.clientY - mainCanvas.offsetTop;
//     // document.getElementById("colorPara").innerHTML = ox + ' ' + oy;

//     var x = 4*(ox*windowWidth + oy);
//     var canImg = mainCanvasContext.getImageData(0, 0, windowWidth, windowHeight);
//     document.getElementById("colorPara").innerHTML = canImg.data[x] + ' ' + canImg.data[x+1] + ' ' + canImg.data[x+2];
// }


// mainCanvas.onmousemove = function(e) {
//     var ox = e.clientX - mainCanvas.offsetLeft;
//     var oy = e.clientY - mainCanvas.offsetTop;
//     if(ox >= minX && ox <= maxX && oy >= minY && oy <= maxY) {
//         var canImg = mainCanvasContext.getImageData(minX, minY, maxX - minX, maxY - minY);
//         var x = 4*(ox*canImg.width + oy);
//         document.getElementById("colorPara").innerHTML = canImg.data[x];
//     }
// }