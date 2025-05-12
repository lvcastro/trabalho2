#version 330 core

uniform vec4 color;
varying vec2 coordenadasTextura;
uniform sampler2D imagem;
uniform bool usarTextura;  // novo uniform booleano

void main() {
    if (usarTextura) {
        // Usar textura quando usarTextura for true
        vec4 texture = texture2D(imagem, coordenadasTextura);
        gl_FragColor = texture;
    } else {
        // Usar cor sólida quando usarTextura for false
        gl_FragColor = color;
    }
}