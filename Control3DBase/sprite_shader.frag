
varying vec2 v_uv;
uniform sampler2D u_tex_diffuse;
uniform sampler2D u_tex_specular;
uniform float u_using_alpha_texture;

uniform float u_opacity;



void main(void)
{
	vec4 color = texture2D(u_tex_diffuse, v_uv);
	float opacity = u_opacity;
	if(u_using_alpha_texture==1.0){
		opacity *= texture2D(u_tex_specular, v_uv).r;
	}
	if(opacity < 0.02){
		discard;
	}
	gl_FragColor = color;
	gl_FragColor.a = opacity;

}