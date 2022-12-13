var gl;

var LeVarying = vec3(1.0, 0.0, 0.0);
var orientVal = 0.5;
var noiseVal = 25;

window.onload = function init()
{
    let canvas = document.getElementById("canvas");
    gl = setup(canvas)

    initBackground(gl);
    initSphere(gl, numTimesToSubdivide);
    light(gl);
    view(gl, canvas);

    let parent = document.querySelector('#color-parent');
    let picker = new Picker({parent: parent, color: 'red', alpha: false, editor: false});
    picker.onChange = function(color) {
        parent.style.background = color.rgbaString;
        LeVarying = vec3(color.rgba[0]/255, color.rgba[1]/255, color.rgba[2]/255);
    };

    document.getElementById("orient-slider").oninput = function() {
        orientVal = event.srcElement.value;
    };

    document.getElementById("noise-slider").oninput = function() {
        noiseVal = event.srcElement.value;
    };

    render();
}


function render()
{
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    gl.uniform3fv(gl.getUniformLocation(gl.program, "Le"), flatten(LeVarying));
    gl.uniform1f(gl.getUniformLocation(gl.program, "noiseScale"), noiseVal);

    gl.uniform1i(gl.getUniformLocation(gl.program, "background"), true);
    gl.drawArrays(gl.TRIANGLE_FAN, 0, 4);

    gl.uniform1i(gl.getUniformLocation(gl.program, "background"), false);
    let M = getModel(orientVal, 1.0, 0.0, 0.0);
    let N = normalMatrix(mult(gl.viewMat, M), true);
    gl.uniformMatrix4fv(gl.getUniformLocation(gl.program, "M"), false, flatten(M));
    gl.uniformMatrix3fv(gl.getUniformLocation(gl.program, "N"), false, flatten(N));

    drawSphere(gl);

    requestAnimationFrame(render)
}
