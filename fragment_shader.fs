#version 330 core

// Parâmetros da luz
uniform vec3 lightPos;
uniform vec3 viewPos;
vec3 lightColor = vec3(1.0, 1.0, 1.0);

// Parâmetros de iluminação
uniform float ka;
uniform float kd;
uniform float ks;
uniform float ns;

uniform bool isLampada;

// Uniform para alternar entre textura e cor
uniform bool usarTextura;
uniform vec4 color; // cor sólida, enviada do Python

// Recebidos do vertex shader
in vec2 out_texture;
in vec3 out_normal;
in vec3 out_fragPos;

uniform sampler2D samplerTexture;

out vec4 fragColor;

void main() {
    // Iluminação ambiente
    vec3 ambient = ka * lightColor;

    // Iluminação difusa
    vec3 norm = normalize(out_normal);
    vec3 lightDir = normalize(lightPos - out_fragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = kd * diff * lightColor;

    // Iluminação especular
    vec3 viewDir = normalize(viewPos - out_fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
    vec3 specular = ks * spec * lightColor;

    vec3 lighting = ambient + diffuse + specular;

	if (isLampada) {
		vec3 emissiveColor = vec3(1.5, 1.3, 0.9); // tom quente e claro
		lighting += emissiveColor;
	}

    vec4 baseColor = usarTextura ? texture(samplerTexture, out_texture) : color;

    fragColor = vec4(lighting, 1.0) * baseColor;
}