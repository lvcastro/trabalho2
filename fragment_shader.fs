#version 330 core

uniform vec4 color;
varying vec2 coordenadasTextura;
uniform sampler2D imagem;

void main(){
	vec4 texture = texture2D(imagem, coordenadasTextura);
	gl_FragColor = texture;
}