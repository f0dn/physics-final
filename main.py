from vpython import *

t = 0
dt = 0.1

images = {
    "BABY_DANIEL": ["https://i.ibb.co/pjkg62st/baby-daniel.jpg", 134, 170, 0.1],
    "BABY_FLINT": ["https://i.ibb.co/b43jm6f/baby-flint.jpg", 0.1],
    "MOM_DANIEL": ["https://i.ibb.co/psXhSLX/mom-daniel.jpg", 0.1],
    "MOM_FLINT": ["https://i.ibb.co/V0cyPxV6/mom-flint.jpg", 0.1],
}

length = 10
mass = 5
ang_velo = 0
ang = 0.2
friction_coefficient = 0.3
external_force_amplitude = 393
external_force_frequency = 0.51111
push_angle = 0.15
effective_angle_diff = 0.1

def update_length(slider):
    global length
    length = slider.value

def update_mass(slider):
    global mass
    mass = slider.value

def update_ang_velo(slider):
    global ang_velo
    ang_velo = slider.value

def update_ang(slider):
    global ang
    ang = slider.value

def update_friction(slider):
    global friction_coefficient
    friction_coefficient = slider.value

def update_external_force_amplitude(slider):
    global external_force_amplitude
    external_force_amplitude = slider.value

def update_external_force_frequency(slider):
    global external_force_frequency
    external_force_frequency = slider.value

def update_push_angle(slider):
    global push_angle
    push_angle = slider.value

def update_effective_angle_diff(slider):
    global effective_angle_diff
    effective_angle_diff = slider.value

# control_scene = canvas(title='Parameters', width=400, height=600, range=1)
# slider_x = 250
# slider_y_start = 550
# slider_spacing = 40

# slider_length = slider(scene=control_scene, min=1, max=50, value=length, length=150, bind=update_length, pos=vector(slider_x, slider_y_start, 0), label='Length')
# slider_mass = slider(scene=control_scene, min=1, max=20, value=mass, length=150, bind=update_mass, pos=vector(slider_x, slider_y_start - slider_spacing, 0), label='Mass')
# slider_ang_velo = slider(scene=control_scene, min=-2, max=2, value=ang_velo, length=150, bind=update_ang_velo, pos=vector(slider_x, slider_y_start - 2*slider_spacing, 0), label='Angular Vel')
# slider_ang = slider(scene=control_scene, min=0, max=3.14, value=ang, length=150, bind=update_ang, pos=vector(slider_x, slider_y_start - 3*slider_spacing, 0), label='Angle')
# slider_friction = slider(scene=control_scene, min=0, max=1, value=friction_coefficient, length=150, bind=update_friction, pos=vector(slider_x, slider_y_start - 4*slider_spacing, 0), label='Friction Coef')
# slider_external_force_amp = slider(scene=control_scene, min=0, max=1000, value=external_force_amplitude, length=150, bind=update_external_force_amplitude, pos=vector(slider_x, slider_y_start - 5*slider_spacing, 0), label='External Force Amp')
# slider_external_force_freq = slider(scene=control_scene, min=0, max=10, value=external_force_frequency, length=150, bind=update_external_force_frequency, pos=vector(slider_x, slider_y_start - 6*slider_spacing, 0), label='External Force Freq')
# slider_push_angle = slider(scene=control_scene, min=0, max=1, value=push_angle, length=150, bind=update_push_angle, pos=vector(slider_x, slider_y_start - 7*slider_spacing, 0), label='Push Angle')
# slider_effective_angle_diff = slider(scene=control_scene, min=0, max=1, value=effective_angle_diff, length=150, bind=update_effective_angle_diff, pos=vector(slider_x, slider_y_start - 8*slider_spacing, 0), label='Eff. Angle Diff')

class Swing:
    def __init__(
        self,
        v_color,
        ps_color,
        length,
        mass,
        ang_velo,
        ang,
        friction_coefficient,
        external_force_amplitude,
        external_force_frequency,
        push_angle,
        effective_angle_diff,
        texture_mom,
        texture_baby,
    ):
        self.ang_velocity_graph = graph(
            title="Pendulum Angular Velocity",
            xtitle="Time (s)",
            ytitle="Velocity (m/s)",
            scroll=True,
            xmin=0,
            xmax=100,
        )
        self.pendulum_graph = gcurve(color=v_color, graph=self.ang_velocity_graph)
        self.phase_space_graph = graph(
            title="Pendulum Phase Space",
            xtitle="Angle (rad)",
            ytitle="Angular Velocity (rad/s)",
        )
        self.pendulum_phase_space = gcurve(color=ps_color, graph=self.phase_space_graph)

        self.pendulum_length = length
        self.baby_image = images[texture_baby]
        self.mom_image = images[texture_mom]
        self.pendulum = sphere(
            pos=vector(0, -self.pendulum_length, 0),
            radius=5,
            texture=self.baby_image[0],
        )
        self.pendulum_mass = mass
        self.pendulum_ang_velocity = ang_velo
        self.pendulum_ang = ang
        self.pendulum_moment = self.pendulum_mass * self.pendulum_length**2 / 2
        self.gravity = vector(0, -9.81, 0)

        self.friction_coefficient = friction_coefficient

        self.external_force_amplitude = external_force_amplitude
        self.external_force_frequency = external_force_frequency

        self.push_angle = push_angle
        self.effective_angle_diff = effective_angle_diff

    def update(self):
        self.friction_force = -self.friction_coefficient * self.pendulum_ang_velocity
        external_force = (
            self.external_force_amplitude * cos(self.external_force_frequency * t)
            if abs(self.pendulum_ang) < self.push_angle
            else 0
        )
        torque = (
            (self.pendulum_mass * self.gravity).cross(self.pendulum.pos)
            + self.friction_force * self.pendulum_length * vector(0, 0, -1)
            + external_force
            * abs(cos(self.pendulum_ang + self.effective_angle_diff))
            * vector(0, 0, -1)
        )
        ang_accel = -(torque.mag * sign(torque.z)) / self.pendulum_moment
        self.pendulum_ang_velocity += ang_accel * dt
        self.pendulum_ang += self.pendulum_ang_velocity * dt
        self.pendulum.pos = vector(
            self.pendulum_length * sin(self.pendulum_ang),
            -self.pendulum_length * cos(self.pendulum_ang),
            0,
        )

        self.pendulum_graph.plot(t, self.pendulum_ang_velocity)
        self.pendulum_phase_space.plot(self.pendulum_ang, self.pendulum_ang_velocity)

swing1 = Swing(
    color.red,
    color.blue,
    length,
    mass,
    ang_velo,
    ang,
    friction_coefficient,
    external_force_amplitude,
    external_force_frequency,
    push_angle,
    effective_angle_diff,
    "MOM_FLINT",
    "BABY_DANIEL",
)

swing2 = Swing(
    color.green,
    color.orange,
    10,
    11,
    0.1111,
    0.11111,
    0.11111,
    111,
    0.11111,
    0.11111,
    0.1111,
    "MOM_DANIEL",
    "BABY_FLINT",
)

scene.visible = False
scene.waitfor("textures")
scene.visible = True

while True:
    rate(60)
    swing1.update()
    swing2.update()
    t += dt