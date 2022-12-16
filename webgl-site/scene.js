const lightPosVal = vec4(0.0, 0.0, 2.0, 1.0)
const LeRadiance = 1.0;
const LeVal = vec3(LeRadiance, 0.0, 0.0);
const kaVal = 0.1;
const kdVal = 0.8;
const ksVal = 0.3;
const sVal = 50;

const alpha = 90.0;
const n = 1.0;
const f = 100.0;

const bgcolor = vec4(0.0, 0.0, 0.0, 1.0)

const bgArray = [
    vec4(-1.0, -1.0, 0.999, 1.0),
    vec4( 1.0, -1.0, 0.999, 1.0),
    vec4( 1.0,  1.0, 0.999, 1.0),
    vec4(-1.0, 1.0, 0.999, 1.0),
];

function setup(canvas) {
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor(bgcolor[0], bgcolor[1], bgcolor[2], bgcolor[3]);
    gl.enable(gl.DEPTH_TEST);
    gl.enable(gl.CULL_FACE);
    gl.program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(gl.program);
    gl.vBuffer = null;
    gl.nBuffer = null;
    gl.pointsArray = [];
    gl.normalsArray = [];

    return gl;
}

function light(gl) {
    gl.uniform4fv(gl.getUniformLocation(gl.program, "lightPos"), flatten(lightPosVal));
    gl.uniform3fv(gl.getUniformLocation(gl.program, "Le"), flatten(LeVal));
    gl.uniform1f(gl.getUniformLocation(gl.program, "ka"), kaVal);
    gl.uniform1f(gl.getUniformLocation(gl.program, "kd"), kdVal);
    gl.uniform1f(gl.getUniformLocation(gl.program, "ks"), ksVal);
    gl.uniform1f(gl.getUniformLocation(gl.program, "s"), sVal);
}

function view(gl, canvas) {
    let A = canvas.width / canvas.height;

    let projectionTransform = perspective(alpha, A, n, f);
    gl.uniformMatrix4fv(gl.getUniformLocation(gl.program, "P"), false, flatten(projectionTransform));

    eye = vec3(0.0, 0.0, 2.0);
    up = vec3(0.0, 1.0, 0.0);
    at = vec3(0.0, 0.0, 0.0);

    gl.viewMat = lookAt(eye, at, up);
    gl.uniformMatrix4fv(gl.getUniformLocation(gl.program, "V"), false, flatten(gl.viewMat));

    let N = normalMatrix(gl.viewMat, true);
    gl.uniformMatrix3fv(gl.getUniformLocation(gl.program, "N"), false, flatten(N));
}

function initBackground(gl) {
    gl.pointsArray = gl.pointsArray.concat(bgArray);
    gl.normalsArray = gl.normalsArray.concat(bgArray);
}
