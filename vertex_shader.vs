#version 330 core

attribute vec3 position;
attribute vec2 texture_coord;
varying vec2 coordenadasTextura;
                
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;        

void main(){
	gl_Position = projection * view * model * vec4(position,1.0);
	coordenadasTextura = vec2(texture_coord);
}