attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;



uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec4 v_position;
varying vec2 v_uv;




void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	position = u_model_matrix * position;
	normal = u_model_matrix * normal;
	//float light_factor_1 = max(dot(normalize(normal), normalize(vec4(1, 2, 3, 0))), 0.0);
	//float light_factor_2 = max(dot(normalize(normal), normalize(vec4(-3, -2, -1, 0))), 0.0);
	v_normal = normalize(normal);
	v_position = position;
	v_uv = a_uv;
	position = u_view_matrix * position;
	//eye coordinates
	position = u_projection_matrix * position;
	//clip coordinates
	gl_Position = position;
}