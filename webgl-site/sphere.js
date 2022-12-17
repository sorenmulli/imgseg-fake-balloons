const numTimesToSubdivide = 5;
const va = vec4(0.0, 0.0, 1.0, 1.0);
const vb = vec4(0.0, 0.942809, -0.333333, 1.0);
const vc = vec4(-0.816497, -0.471405, -0.333333, 1.0);
const vd = vec4(0.816497, -0.471405, -0.333333, 1.0);


function triangle(a, b, c) {
    gl.pointsArray.push(a);
    gl.pointsArray.push(b);
    gl.pointsArray.push(c);
    gl.normalsArray.push( vec4(a[0], a[1], a[2], 0.0) );
    gl.normalsArray.push( vec4(b[0], b[1], b[2], 0.0) );
    gl.normalsArray.push( vec4(c[0], c[1], c[2], 0.0) );
}

function divideTriangle(a, b, c, count, gl)
{
    if (count > 0) {
        let ab = normalize(mix(a, b, 0.5), true);
        let ac = normalize(mix(a, c, 0.5), true);
        let bc = normalize(mix(b, c, 0.5), true);
        divideTriangle(a, ab, ac, count - 1, gl);
        divideTriangle(ab, b, bc, count - 1, gl);
        divideTriangle(bc, c, ac, count - 1, gl);
        divideTriangle(ab, bc, ac, count - 1, gl);
    }
    else {
        triangle(a, b, c, gl);
    }
}


function tetrahedron(a, b, c, d, n, gl)
{
    divideTriangle(a, b, c, n, gl);
    divideTriangle(d, c, b, n, gl);
    divideTriangle(a, d, b, n, gl);
    divideTriangle(a, c, d, n, gl);
}

function initSphere(gl, numSubdivs) {
    tetrahedron(va, vb, vc, vd, numSubdivs, gl);

    gl.deleteBuffer(gl.nBuffer);
    gl.nBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, gl.nBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(gl.normalsArray), gl.STATIC_DRAW );

    let vNormal = gl.getAttribLocation( gl.program, "a_Normal" );
    gl.vertexAttribPointer( vNormal, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray( vNormal);

    gl.deleteBuffer(gl.vBuffer);
    gl.vBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(gl.pointsArray), gl.STATIC_DRAW);

    let vPosition = gl.getAttribLocation( gl.program, "a_Position" );
    gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray( vPosition );
}

function getModel(rho, scale, posx, posy) {
let sx = rho;
let sy = (1 - rho);
// Make sure that rho=0.5 corresponds to no scaling
let norm = 2 ** 0.5 / (sx**2 + sy**2)**0.5;
// Only scale parallel to x or y axis to avoid more free parameters
let elongationTransform = scalem(sx*norm, sy*norm, 1.0);
    let scaleTransform = scalem(scale, scale, scale);
    let transTransform = translate(posx, posy, 0.0);
    return mult(transTransform, mult(scaleTransform, elongationTransform));
}

function drawSphere(gl) {
    gl.drawArrays(gl.TRIANGLES, 4, gl.pointsArray.length-4);
}
