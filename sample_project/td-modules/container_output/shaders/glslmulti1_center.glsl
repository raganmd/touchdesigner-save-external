
// Example Pixel Shader

// uniform float exampleUniform;

out vec4 fragColor;
void main()
{
	//vec2 newUV	= (vUV.st * 2) - 1;
	vec2 newUV 	= vUV.st;
	vec4 color 	= vec4(newUV, vec2(1.0));
	fragColor 	= TDOutputSwizzle(color);
}
