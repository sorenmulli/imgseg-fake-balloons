var gl;
var LeVarying = vec3(1.0, 0.0, 0.0);
var orientVal = 0.5;
var noiseVal = 25;

window.onload = function init()
{
    let canvas = document.getElementById("canvas");
    gl = setup(canvas)

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

function getModel(orient) {
    let sx = orient * 2.0;
    let sy = (1 - orient) * 2.0;
    let norm = 2 ** 0.5 / (sx**2 + sy**2)**0.5;
    return scalem(sx*norm, sy*norm, 1.0);
}


function render()
{
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    gl.uniform3fv(gl.getUniformLocation(gl.program, "Le"), flatten(LeVarying));
    gl.uniform1f(gl.getUniformLocation(gl.program, "noiseScale"), noiseVal);

    for(let i=0; i<gl.pointsArray.length; i+=3)
        gl.drawArrays(gl.TRIANGLES, i, 3);

    gl.uniformMatrix4fv(gl.getUniformLocation(gl.program, "M"), false, flatten(getModel(orientVal)));

    requestAnimationFrame(render)
}
