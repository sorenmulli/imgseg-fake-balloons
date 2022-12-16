var gl;
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
    exampleScene(gl)
    decideBallAttributes(gl);

    document.getElementById("recomputeButton").onclick = function(){
        decideScene(gl);
        exampleScene(gl)
    };

    document.getElementById("randomButton").onclick = function(){
        decideBallAttributes(gl);
    };

    document.getElementById("avgButton").onclick = function(){
        decideBallAttributes(gl, true);
    };
    document.getElementById("ipButton").onclick = function(){
        doSc = false;
    };
    document.getElementById("scButton").onclick = function(){
        doSc = true;
    };

    render();
}

function exampleScene(gl) {
    // Hardcode to show example
    gl.balls = 3;

    gl.ballScales = [0.5, 0.5, 0.5];
    gl.ballX = [-1.2, 0, 1.2];
    gl.ballY = [0, 0, 0];

    gl.ballClass = [0, 1, 2];
    gl.ballKd = [0.5, 0.5, 0.5];
    gl.ballKs = [0.25, 0.25, 0.25];
    gl.ballS = [50, 50, 50];
}


function render()
{
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    gl.uniform1i(gl.getUniformLocation(gl.program, "do_sc"), doSc);

    gl.uniform1f(gl.getUniformLocation(gl.program, "noiseScale"), gl.bgScale);
    gl.uniform1i(gl.getUniformLocation(gl.program, "background"), true);
    gl.drawArrays(gl.TRIANGLE_FAN, 0, 4);

    gl.uniform1i(gl.getUniformLocation(gl.program, "background"), false);

    for (let i=0; i<gl.balls; i+=1) {
        let M = getModel(gl.ballOrient[i], gl.ballScales[i], gl.ballX[i], gl.ballY[i])
        let N = normalMatrix(mult(gl.viewMat, M), true);

        gl.uniform1f(gl.getUniformLocation(gl.program, "noiseScale"), gl.ballNoiseScale[i]);
        gl.uniform3fv(gl.getUniformLocation(gl.program, "Le"), flatten(gl.ballColor[i]));
        gl.uniformMatrix4fv(gl.getUniformLocation(gl.program, "M"), false, flatten(M));

        gl.uniformMatrix3fv(gl.getUniformLocation(gl.program, "N"), false, flatten(N));

        gl.uniform1f(gl.getUniformLocation(gl.program, "kd"), gl.ballKd[i]);
        gl.uniform1f(gl.getUniformLocation(gl.program, "ks"), gl.ballKs[i]);
        gl.uniform1f(gl.getUniformLocation(gl.program, "s"), gl.ballS[i]);

        drawSphere(gl);
    }

    requestAnimationFrame(render)
}
