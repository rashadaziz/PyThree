#version 330

struct Light {
    int type;
    vec3 color;
    vec3 direction;
    vec3 position;
    vec3 attenuation;
};

uniform Light light0;
uniform Light light1;
uniform Light light2;
uniform Light light3;

vec3 lightCalc(Light light, vec3 pointPosition, vec3 pointNormal) {
    float ambient = 0;
    float diffuse = 0;
    float specular = 0;
    float attenuation = 0;
    vec3 lightDirection = vec3(0, 0, 0);

    if(light.type == 1) {
        ambient = 1;
    } else if(light.type == 2) {
        lightDirection = normalize(light.direction);
    } else if(light.type == 3) {
        lightDirection = normalize(pointPosition - light.position);
        float distance = length(light.position - pointPosition);
        float a = light.attenuation[0];
        float b = light.attenuation[1];
        float c = light.attenuation[2];
        float d = distance;
        attenuation = 1.0 / (a + b * d + c * d * d);
    }

    if(light.type > 1) {
        pointNormal = normalize(pointNormal);
        diffuse = max(dot(pointNormal, -lightDirection), 0);
        diffuse *= attenuation;
    }

    return light.color * (ambient + diffuse + specular);
}

uniform vec3 baseColor;
uniform bool useTexture;
uniform sampler2D texture;
in vec3 position;
in vec2 UV;
in vec3 normal;
out vec4 fragColor;
void main() {
    vec4 color = vec4(baseColor, 1.0);
    
    if(useTexture) {
        color *= texture2D(texture, UV);
    }

    vec3 total = vec3(0, 0, 0);
    total += lightCalc(light0, position, normal);
    total += lightCalc(light1, position, normal);
    total += lightCalc(light2, position, normal);
    total += lightCalc(light3, position, normal);
    color *= vec4(total, 1);
    fragColor = color;
}