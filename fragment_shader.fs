#version 330 core

// parametro com a cor da(s) fonte(s) de iluminacao
uniform vec3 lightPos; // define coordenadas de posicao da luz
vec3 lightColor = vec3(1.0, 1.0, 1.0);

// parametros da iluminacao ambiente e difusa
uniform float ka; // coeficiente de reflexao ambiente
uniform float kd; // coeficiente de reflexao difusa

// parametros da iluminacao especular
uniform vec3 viewPos; // define coordenadas com a posicao da camera/observador
uniform float ks; // coeficiente de reflexao especular
uniform float ns; // expoente de reflexao especular


// parametros recebidos do vertex shader
varying vec2 out_texture; // recebido do vertex shader
varying vec3 out_normal; // recebido do vertex shader
varying vec3 out_fragPos; // recebido do vertex shader
uniform sampler2D samplerTexture;



void main(){

	// calculando reflexao ambiente
	vec3 ambient = ka * lightColor;             

	// calculando reflexao difusa
	vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares
	vec3 lightDir = normalize(lightPos - out_fragPos); // direcao da luz
	float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90)
	vec3 diffuse = kd * diff * lightColor; // iluminacao difusa
	
	// calculando reflexao especular
	vec3 viewDir = normalize(viewPos - out_fragPos); // direcao do observador/camera
	vec3 reflectDir = normalize(reflect(-lightDir, norm)); // direcao da reflexao
	float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
	
	vec3 specular = ks * spec * lightColor;             
	
	// aplicando o modelo de iluminacao
	vec4 texture = texture2D(samplerTexture, out_texture);
	vec4 result = vec4((ambient + diffuse + specular),1.0) * texture; // aplica iluminacao
	gl_FragColor = result;

}