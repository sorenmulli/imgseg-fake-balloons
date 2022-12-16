var gl;

var save = false;
var labelmap = false;
var doSc = false;

window.onload = function init()
{
    let canvas = document.getElementById("canvas");
    gl = setup(canvas)

    initBackground(gl);
    initSphere(gl, numTimesToSubdivide);
    light(gl);
    view(gl, canvas);

    decideScene(gl);
    decideBallAttributes(gl);

    document.getElementById("recomputeButton").onclick = function(){
        labelmap = false;
        doSc = false;
        decideScene(gl);
        decideBallAttributes(gl);
    };

    document.getElementById("saveButton").onclick = function(){
        save = true;
    };

    document.getElementById("labelMapButton").onclick = function(){
        labelmap = !labelmap;
    };

    document.getElementById("ipButton").onclick = function(){
        doSc = false;
    };
    document.getElementById("scButton").onclick = function(){
        doSc = true;
    };
    render();
}


function render()
{
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    gl.uniform1i(gl.getUniformLocation(gl.program, "do_sc"), doSc);
    gl.uniform1i(gl.getUniformLocation(gl.program, "labelmap"), labelmap);

    gl.uniform1f(gl.getUniformLocation(gl.program, "noiseScale"), gl.bgScale);
    gl.uniform1i(gl.getUniformLocation(gl.program, "background"), true);
    gl.drawArrays(gl.TRIANGLE_FAN, 0, 4);

    gl.uniform1i(gl.getUniformLocation(gl.program, "background"), false);

    for (let i=0; i<gl.balls; i+=1) {
        let M = getModel(gl.ballOrient[i], gl.ballScales[i], gl.ballX[i], gl.ballY[i])
        let N = normalMatrix(mult(gl.viewMat, M), true);

        gl.uniform1f(gl.getUniformLocation(gl.program, "noiseScale"), gl.ballNoiseScale[i]);
        let col = labelmap ? gl.ballLabel[i] : gl.ballColor[i];
        gl.uniform3fv(gl.getUniformLocation(gl.program, "Le"), flatten(col));
        gl.uniformMatrix4fv(gl.getUniformLocation(gl.program, "M"), false, flatten(M));

        gl.uniformMatrix3fv(gl.getUniformLocation(gl.program, "N"), false, flatten(N));

        gl.uniform1f(gl.getUniformLocation(gl.program, "kd"), gl.ballKd[i]);
        gl.uniform1f(gl.getUniformLocation(gl.program, "ks"), gl.ballKs[i]);
        gl.uniform1f(gl.getUniformLocation(gl.program, "s"), gl.ballS[i]);

        drawSphere(gl);
    }

    if (save) {
        save = false;
        let image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
        let link = document.getElementById("imgLink");
        let extension = labelmap ? ".label.png" : ".png";
        link.setAttribute("download", gl.sceneName + extension);
        link.setAttribute("href", image);
        link.click();
    }

    requestAnimationFrame(render)
}
