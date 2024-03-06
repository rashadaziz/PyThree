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

    if (light.type == 1) {
        ambient = 1;
    } else if (light.type == 2) {
        lightDirection = normalize(light.direction);
    } else if (light.type == 3) {
        lightDirection = normalize(pointPosition - light.position);
        float distance = length(light.position - pointPosition);
        float a = light.attenuation[0];
        float b = light.attenuation[1];
        float c = light.attenuation[2];
        float d = distance;
        attenuation = 1.0 / (a + b*d + c*d*d);
    }

    if (light.type > 1) {
        pointNormal = normalize(pointNormal);
        diffuse = max(dot(pointNormal, -lightDirection), 0);
        diffuse *= attenuation;
    }

    return light.color * (ambient + diffuse + specular);
}


uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;
in vec3 vertexPosition;
in vec2 vertexUV;
in vec3 faceNormal;
out vec2 UV;
out vec3 light;

void main() {
    vec4 vertexTransformed = modelMatrix * vec4(vertexPosition, 1.0);
    gl_Position = projectionMatrix * viewMatrix * vertexTransformed;
    vec3 position = vec3(vertexTransformed);
    vec3 normal = vec3(mat3(modelMatrix) * faceNormal);
    light = vec3(0, 0, 0);
    light += lightCalc(light0, position, normal);
    light += lightCalc(light1, position, normal);
    light += lightCalc(light2, position, normal);
    light += lightCalc(light3, position, normal);
}