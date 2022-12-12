
function randomRange(min, max) { 
    return Math.random() * (max - min) + min;
}

function decideScene(gl) {
    gl.balls = parseInt(randomRange(1, 8));
    gl.ballScales = [];

    gl.ballX = [];
    gl.ballY = [];

    gl.ballKd = [];
    gl.ballKs = [];
    gl.ballS = [];

    for (let i=0; i<gl.balls; i+=1) {
        gl.ballScales.push(randomRange(0.1, 0.5));
        gl.ballX.push(randomRange(-1.0, 1.0));
        gl.ballY.push(randomRange(-1.0, 1.0));
        gl.ballKd.push(randomRange(0.25, 0.75));
        gl.ballKs.push(randomRange(0.0, 0.5));
        gl.ballS.push(randomRange(10.0, 100.0));
    }

    gl.bgScale = randomRange(1, 20);

}
