const n_classes = 3

const classAvgHue = [150, 250, 350];
const stdHue = 50;

const classAvgOrients = [0.55, 0.45, 0.50];
const stdOrient = 0.05;

const classAvgNoiseScales = [5, 17.5, 30];
const stdNoiseScale = 5;


function randomRange(min, max) { 
    return min + Math.random() * (max - min);
}

function decideScene(gl) {
    // Number and class
    gl.balls = parseInt(randomRange(1, 20));
    gl.ballClass = [];

    // Scale, placement
    gl.ballScales = [];
    gl.ballX = [];
    gl.ballY = [];

    // Light
    gl.ballKd = [];
    gl.ballKs = [];
    gl.ballS = [];

    for (let i=0; i<gl.balls; i+=1) {
        // Round down to class int
        gl.ballClass.push(parseInt(randomRange(0, n_classes-0.0001)));

        // Scene variables are uniformly distributed
        gl.ballScales.push(randomRange(0.1, 0.7));
        gl.ballX.push(randomRange(-1.5, 1.5));
        gl.ballY.push(randomRange(-1.5, 1.5));
        gl.ballKd.push(randomRange(0.25, 0.75));
        gl.ballKs.push(randomRange(0.0, 0.5));
        gl.ballS.push(randomRange(10.0, 100.0));
    }
    gl.bgScale = randomRange(1, 20);
    // String of random numbers used to output the image as png
    gl.sceneName = (Math.random() + 1).toString(36).substring(2);
}

// Below function is taken from
// https://stackoverflow.com/questions/2353211/hsl-to-rgb-color-conversion/64090995#64090995
// input: h as an angle in [0,360] and s,l in [0,1] - output: r,g,b in [0,1]
function hsl2rgb(h,s,l)
{
   let a=s*Math.min(l,1-l);
   let f= (n,k=(n+h/30)%12) => l - a*Math.max(Math.min(k-3,9-k,1),-1);
   return [f(0),f(8),f(4)];
}

// Below function is taken from
// https://stackoverflow.com/questions/25582882/javascript-math-random-normal-distribution-gaussian-bell-curve
// Standard Normal variate using Box-Muller transform.
function gaussianRandom(mean=0, stdev=1) {
    let u = 1 - Math.random(); //Converting [0,1) to (0,1)
    let v = Math.random();
    let z = Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
    // Transform to the desired mean and standard deviation:
    return z * stdev + mean;
}

function decideBallAttributes(gl, avg=false) {
    gl.ballColor = [];
    gl.ballOrient = [];
    gl.ballNoiseScale = [];
    gl.ballLabel = [];

    for (let i=0; i<gl.balls; i+=1) {
        cla = gl.ballClass[i];

        let avgHue = classAvgHue[cla];
        let hue = avg ? avgHue: gaussianRandom(classAvgHue[cla], stdHue);
        hue = hue % 360;
        let rgbCol = vec3(hsl2rgb(hue, 1.0, 0.5));
        gl.ballColor.push(rgbCol);

        let labelCol = vec3(hsl2rgb(avgHue, 1.0, 0.5));
        gl.ballLabel.push(labelCol);

        let orient = avg ? classAvgOrients[cla] : gaussianRandom(classAvgOrients[cla], stdOrient)
        orient = Math.max(Math.min(1.0, orient), 0.0);
        gl.ballOrient.push(orient);

        let noiseScale = avg ? classAvgNoiseScales[cla] : gaussianRandom(classAvgNoiseScales[cla], stdNoiseScale)
        noiseScale = Math.max(noiseScale, 0.0);
        gl.ballNoiseScale.push(noiseScale);
    }
}
