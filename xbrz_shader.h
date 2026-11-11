/*
 * SOFIA-Pure xBRZ-inspired GPU scaler
 *
 * This is an original, compact xBR-style edge-aware shader inspired by
 * xBRZ concepts. It is not Zenju's original xBRZ implementation.
 * The surrounding project is distributed under GPL-2.0-or-later.
 */
#ifndef SOFIA_XBRZ_SHADER_H
#define SOFIA_XBRZ_SHADER_H

static const char fragment_shader_xbrz_src[] = ZL_SHADER_SOURCE_HEADER(ZL_GLES_PRECISION_MEDIUM) R"GLSL(
uniform sampler2D u_texture;
varying vec2 v_texcoord;
uniform float TextureSize_x;
uniform float TextureSize_y;
uniform float InputSize_x;
uniform float InputSize_y;
uniform float OutputSize_x;
uniform float OutputSize_y;

vec3 xbrz_sample(vec2 p)
{
    vec2 limit = vec2(InputSize_x, InputSize_y) - vec2(1.0);
    vec2 uv = (clamp(p, vec2(0.0), limit) + vec2(0.5)) /
              vec2(TextureSize_x, TextureSize_y);
    return texture2D(u_texture, uv).rgb;
}

float xbrz_dist(vec3 a, vec3 b)
{
    vec3 d = a - b;
    float y  = dot(d, vec3(0.2627, 0.6780, 0.0593));
    float cb = 0.5 * (d.b - y) / (1.0 - 0.0593);
    float cr = 0.5 * (d.r - y) / (1.0 - 0.2627);
    return sqrt(y*y + cb*cb + cr*cr);
}

void main()
{
    vec2 inputSize = vec2(InputSize_x, InputSize_y);
    vec2 outputSize = vec2(OutputSize_x, OutputSize_y);
    vec2 scale = outputSize / max(inputSize, vec2(1.0));

    vec2 p = v_texcoord * vec2(TextureSize_x, TextureSize_y);
    vec2 ip = floor(p);
    vec2 f = fract(p);

    vec3 A = xbrz_sample(ip + vec2(-1.0, -1.0));
    vec3 B = xbrz_sample(ip + vec2( 0.0, -1.0));
    vec3 C = xbrz_sample(ip + vec2( 1.0, -1.0));
    vec3 D = xbrz_sample(ip + vec2(-1.0,  0.0));
    vec3 E = xbrz_sample(ip);
    vec3 F = xbrz_sample(ip + vec2( 1.0,  0.0));
    vec3 G = xbrz_sample(ip + vec2(-1.0,  1.0));
    vec3 H = xbrz_sample(ip + vec2( 0.0,  1.0));
    vec3 I = xbrz_sample(ip + vec2( 1.0,  1.0));

    vec3 color = E;
    float threshold = 0.035;
    float edgeWidth = clamp(0.45 / max(min(scale.x, scale.y), 1.0), 0.08, 0.24);

    // Detect a coherent E-I diagonal against its two crossing neighbors.
    float mainDiagonal = xbrz_dist(E, I) + xbrz_dist(F, H);
    float mainCross = xbrz_dist(E, F) + xbrz_dist(E, H);
    if (mainDiagonal + threshold < mainCross &&
        xbrz_dist(E, I) < 0.12 && xbrz_dist(F, H) > 0.08)
    {
        float side = f.x - f.y;
        float blend = smoothstep(-edgeWidth, edgeWidth, side);
        color = mix(H, F, blend);
    }

    // Detect the opposite F-H diagonal.
    float antiDiagonal = xbrz_dist(F, H);
    float antiCross = xbrz_dist(E, I);
    if (antiDiagonal < 0.12 && antiCross > 0.08)
    {
        float side = f.x + f.y - 1.0;
        float blend = smoothstep(-edgeWidth, edgeWidth, side);
        color = mix(E, I, blend);
    }

    // Preserve crisp corners where the surrounding neighborhood is uniform.
    float localEdge = min(min(xbrz_dist(E, B), xbrz_dist(E, D)),
                          min(xbrz_dist(E, F), xbrz_dist(E, H)));
    float cornerWeight = 1.0 - smoothstep(0.02, 0.16, localEdge);
    color = mix(color, E, cornerWeight * 0.35);

    gl_FragColor = vec4(color, 1.0);
}
)GLSL";

#endif
