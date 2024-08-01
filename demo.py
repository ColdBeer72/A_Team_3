from inc.config import *
from inc.state_machine import *
# l1 = [0, 0]
# l2 = [100, 100]
# l3 = [200, 200]
# print(Pose_Calculator.calcular_angulo(l1, l2, l3))

# p1 = [200, 120]
# p2 = [320, 240]
# p3 = [0, 240]
# print(Pose_Calculator.calcular_angulo(p1, p2, p3))

# p1 = [200, 120]
# p2 = [320, 240]
# p3 = [200, 360]
# print(Pose_Calculator.calcular_angulo(p1, p2, p3))

# p1 = [200, 120]
# p2 = [320, 240]
# p3 = [430, 360]
# print(Pose_Calculator.calcular_angulo(p1, p2, p3))

# pose = UserPose()

# pose.postura('Tadasana')

dict_pose_tips = {
    'Tadasana': [['Tip1', 'Tip2', 'Tip3'], ['posible_clip_audio1', 'posible_clip_audio2']],
    'Urdhva Hastasana': [['Manten Culo apretado', 'Consejo 2', 'Consejo 3', 'Consejo 4']['Clips_audios']]
}

postura = 'Tadasana'

print("\n Tips.txt:")
for tip in dict_pose_tips[postura][0]:
    print(tip)
print("\n Clips_Audio.mp4:")
for clip_audio in dict_pose_tips[postura][1]:
    print(clip_audio)