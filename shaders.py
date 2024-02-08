from OpenGL.GL import *
import os

def load_shader(shader_file):
    with open(shader_file, 'r') as file:
        shader_source = file.read()
    return str.encode(shader_source)

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        error = glGetShaderInfoLog(shader).decode('utf-8')
        print(f"Shader compilation error: {error}")  # Print the compilation error
        return None
    return shader

def create_shader_program(vertex_shader_path, fragment_shader_path):
    vertex_source = load_shader(vertex_shader_path)
    fragment_source = load_shader(fragment_shader_path)
    
    vertex_shader = compile_shader(vertex_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_source, GL_FRAGMENT_SHADER)
    
    if vertex_shader is None or fragment_shader is None:
        print("Failed to compile one or more shaders.")
        return None

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    if glGetProgramiv(shader_program, GL_LINK_STATUS) != GL_TRUE:
        error = glGetProgramInfoLog(shader_program).decode('utf-8')
        print(f"Shader linking error: {error}")  # Print the linking error
        return None

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program
