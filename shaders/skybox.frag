#version 330 core
out vec4 FragColor;

in vec3 TexCoords;

uniform sampler2D equirectangularMap;

const float PI = 3.14159265359;

void main()
{   
    vec2 uv = vec2(atan(TexCoords.z, TexCoords.x) / (2.0 * PI) + 0.5, asin(TexCoords.y) / PI + 0.5);
    vec3 color = texture(equirectangularMap, uv).rgb;
    
    FragColor = vec4(color, 1.0);
}
