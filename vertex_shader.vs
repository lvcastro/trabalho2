#version 330 core

attribute vec3 position;
attribute vec2 texture_coord;
attribute vec3 normals;


varying vec2 out_texture;
varying vec3 out_fragPos; //posicao do fragmento (i.e., posicao na superficie onde a iluminacao sera calculada)
varying vec3 out_normal;
		
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;        

void main(){
	gl_Position = projection * view * model * vec4(position,1.0);
	out_texture = vec2(texture_coord);
	out_fragPos = vec3(  model * vec4(position, 1.0));
	out_normal = vec3( model *vec4(normals, 1.0));            
}