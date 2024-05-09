import numpy as np

# 벡터 연산 함수
def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm else v

def dot(v1, v2):
    return np.dot(v1, v2)

def reflect(ray, normal):
    return ray - 2 * dot(ray, normal) * normal

# def refract(ray, normal, eta):
#     cos_i = -dot(normal, ray)
#     sin_t2 = eta * eta * (1.0 - cos_i * cos_i)
#     if sin_t2 > 1.0:
#         return None  # 전반사 조건
#     cos_t = np.sqrt(1.0 - sin_t2)
#     return eta * ray + (eta * cos_i - cos_t) * normal

# 교차 계산 함수
def intersect_sphere(ray_origin, ray_dir, sphere_center, sphere_radius):
    b = 2 * dot(ray_dir, ray_origin - sphere_center)
    c = dot(ray_origin - sphere_center, ray_origin - sphere_center) - sphere_radius**2
    delta = b**2 - 4 * c
    if delta >= 0:
        sqrt_delta = np.sqrt(delta)
        dist1 = (-b - sqrt_delta) / 2
        dist2 = (-b + sqrt_delta) / 2
        if dist1 > 0 or dist2 > 0:
            return sorted([d for d in [dist1, dist2] if d > 0])
    return None

# 색상 계산
def trace_ray(ray_origin, ray_dir, depth=0):
    if depth > 3:  # 광선의 최대 깊이를 제한
        return np.array([0, 0, 0])
    
    sphere_center = np.array([0, 0, 1])
    sphere_radius = 0.5
    light_dir = normalize(np.array([1, 4, -1]))
    ambient = 0.05  # 환경광

    dists = intersect_sphere(ray_origin, ray_dir, sphere_center, sphere_radius)
    if dists:
        hit_point = ray_origin + ray_dir * dists[0]
        normal = normalize(hit_point - sphere_center)
        outside = dot(ray_dir, normal) < 0
        bias = 0.001 * normal if outside else -0.001 * normal

        # 조명 계산
        light_intensity = max(0, dot(light_dir, normal))
        color = np.array([1, 1, 1]) * light_intensity + np.array([1, 1, 1]) * ambient
        
        # 굴절 계산
        # eta = 1.5 if outside else 1/1.5
        # refracted_ray = refract(ray_dir, normal, eta)
        # if refracted_ray is not None:
        #     refracted_color = trace_ray(hit_point + bias, refracted_ray, depth + 1)
        #     color = color * 0.1 + refracted_color * 0.9
        
        return color
    return np.array([0, 0, 0])  # 배경색

# 이미지 생성
width, height = 600, 600
image = np.zeros((height, width, 3))

camera_origin = np.array([0, 0, -1])
camera_dir = np.array([0, 0, 1])
camera_width = 1
camera_height = camera_width * height / width
pixel_width = camera_width / width
pixel_height = camera_height / height

for i in range(height):
    for j in range(width):
        x = (j - width / 2) * pixel_width
        y = (height / 2 - i) * pixel_height
        ray_dir = normalize(np.array([x, y, 1]) - camera_origin)
        image[i, j] = trace_ray(camera_origin, ray_dir)

# 이미지 저장 및 출력
from PIL import Image
img = Image.fromarray((image * 255).astype('uint8'), 'RGB')
img.save('raytracing.png')
print("complete save image")
img.show()
