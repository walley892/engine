VERTEX_STANDARD = '''
void main(){
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
'''

FRAGMENT_STANDARD = '''
#version 440 core
out vec4 vertex_color;
void main(){
    vertex_color=vec4(1,0,0, 1);
}
'''

FRAGMENT_TEXTURE = '''
#version 440 core
in vec2 uv;
out vec4 vertex_color;

uniform sampler2D tex;

void main(){
    vec4 t = texture(tex, uv).rgba;
    if(t.r == 0 && t.g == 0 && t.b == 0){
        t.a = 0.0;
    }
    vertex_color= t.rgba;
}
'''

FRAGMENT_COLOR = '''
#version 440 core
in vec3 fragmentColor;
out vec4 vertex_color;
void main(){
    vertex_color=vec4(fragmentColor, 1);
}
'''

VERTEX_COLOR = '''
#version 440 core
layout(location=0) in vec3 vertex_buffer;
layout(location=1) in vec3 color_buffer;

out vec3 fragmentColor;
uniform mat4x4 rotMat;
void main(){
    gl_Position = rotMat * vec4(vertex_buffer.xyz, 1);
    fragmentColor = color_buffer;
}

'''

VERTEX_POINT = '''
#version 440 core
layout(location=0) in vec3 vertex_buffer;

uniform mat4x4 rotMat;
void main(){
    gl_Position = rotMat * vec4(vertex_buffer.xyz, 1);
}
'''

VERTEX_TEXTURE = '''
#version 440 core
layout(location=0) in vec3 vertex_buffer;
layout(location=1) in vec2 vertex_uvs;

out vec2 uv;

uniform mat4x4 rotMat;
void main(){
    gl_Position = rotMat * vec4(vertex_buffer.xyz, 1);
    uv = vertex_uvs;
}
'''


VERTEX_MULTI_TEXTURE = '''
#version 440 core
layout(location=0) in vec3 vertex_buffer;
layout(location=1) in vec2 vertex_uvs;
layout(location=2) in uint vertex_material_id;

out vec3 uvw;

uniform mat4x4 rotMat;
uniform int n_materials;

void main(){
    gl_Position = rotMat * vec4(vertex_buffer.xyz, 1);
    float fn_materials = n_materials/1.0f;
    float fvertex_material_id = vertex_material_id/1.0f;
    /*
    if(fvertex_material_id == 1){
        uvw = vec3(vertex_uvs, 0);
    }
    else{
        uvw = vec3(vertex_uvs, 0.6f);
    }
    */
    uvw = vec3(vertex_uvs, ((fvertex_material_id-1)/fn_materials) + (0.5f/fn_materials));
}
'''


FRAGMENT_MULTI_TEXTURE = '''
#version 440 core
in vec3 uvw;
out vec4 vertex_color;

uniform sampler3D tex;

void main(){
    vertex_color= vec4(texture(tex, uvw).rgb, 1);
}
'''
