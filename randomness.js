const n_classes = 3

const classAvgHue = [100, 200, 300];
const stdHue = 50;

const classAvgOrients = [0.65, 0.35, 0.5];
const stdOrient = 0.1;

const classAvgNoiseScales = [5, 17.5, 30];
const stdNoiseScale = 5;

// https://stackoverflow.com/questions/2353211/hsl-to-rgb-color-conversion/64090995#64090995
// input: h as an angle in [0,360] and s,l in [0,1] - output: r,g,b in [0,1]
function hsl2rgb(h,s,l)
{
   let a=s*Math.min(l,1-l);
   let f= (n,k=(n+h/30)%12) => l - a*Math.max(Math.min(k-3,9-k,1),-1);
   return [f(0),f(8),f(4)];
}

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

function decideBallAttributes(gl) {
    gl.ballClass = [];
    gl.ballColor = [];
    gl.ballOrient = [];
    gl.ballNoiseScale = [];
    for (let i=0; i<gl.balls; i+=1) {
        gl.ballClass.push();
        gl.ballOrient.push();
        gl.ballNoiseScale.push();
        gl.ballColor.push();
    }
}
