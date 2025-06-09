#version 330 core
out vec4 FragColor;

// --- ESTRUTURAS (STRUCTS) ---
struct Material {
    // Para texturas
    sampler2D diffuseMap;
    float shininess;

    // Flags para alternar
    bool useDiffuseMap;
    
    // Fallback para cores s�lidas
    vec3 solidDiffuse;
    vec3 solidSpecular;
}; 

struct DirLight {
    vec3 direction;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

struct PointLight {
    vec3 position;
    bool on;
    
    float constant;
    float linear;
    float quadratic;
	
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

// --- UNIFORMS GLOBAIS ---
#define NR_POINT_LIGHTS 4

in vec3 out_fragPos;
in vec3 out_normal;
in vec2 out_texture;

uniform vec3 viewPos;
uniform DirLight dirLight;
uniform PointLight pointLights[NR_POINT_LIGHTS];
uniform Material material;

// calculates the color when using a directional light.
vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir, vec3 diffuseColor, vec3 specularColor)
{
    vec3 lightDir = normalize(-light.direction);
    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);
    // specular shading
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    // combine results
    vec3 ambient = light.ambient * diffuseColor;
    vec3 diffuse = light.diffuse * diff * diffuseColor;
    vec3 specular = light.specular * spec * specularColor;
    return (ambient + diffuse + specular);
}

// calculates the color when using a point light.
vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir, vec3 diffuseColor, vec3 specularColor)
{
    vec3 lightDir = normalize(light.position - fragPos);
    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);
    // specular shading
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    // attenuation
    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));    
    // combine results
    vec3 ambient = light.ambient * diffuseColor;
    vec3 diffuse = light.diffuse * diff * diffuseColor;
    vec3 specular = light.specular * spec * specularColor;
    ambient *= attenuation;
    diffuse *= attenuation;
    specular *= attenuation;
    return (ambient + diffuse + specular);
}

// --- FUNÇÃO PRINCIPAL ---
void main()
{
    // Decide qual cor usar para o objeto (da textura ou s�lida)
    vec3 diffuseColor = material.useDiffuseMap ? texture(material.diffuseMap, out_texture).rgb : material.solidDiffuse;
    // Para o brilho, sempre usaremos a cor s�lida
    vec3 specularColor = material.solidSpecular;

    vec3 norm = normalize(out_normal);
    vec3 viewDir = normalize(viewPos - out_fragPos);
    
    // Come�a com a luz direcional
    vec3 result = CalcDirLight(dirLight, norm, viewDir, diffuseColor, specularColor);
    
    // Adiciona o efeito das luzes pontuais
    for(int i = 0; i < NR_POINT_LIGHTS; i++)
    {
        if(pointLights[i].on)
            result += CalcPointLight(pointLights[i], norm, out_fragPos, viewDir, diffuseColor, specularColor);
    }
  
    FragColor = vec4(result, 1.0);
}