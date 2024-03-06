#version 330

uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;
in vec3 vertexPosition;
in vec2 vertexUV;
in vec3 vertexNormal;
out vec3 position;
out vec2 UV;
out vec3 normal;

void main() {
    vec4 vertexTransformed = modelMatrix * vec4(vertexPosition, 1.0);
    gl_Position = projectionMatrix * viewMatrix * vertexTransformed;
    position = vec3(vertexTransformed);
    normal = normalize(mat3(modelMatrix) * vertexNormal);
    UV = vertexUV;
}