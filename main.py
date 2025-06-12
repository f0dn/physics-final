from vpython import *

t = 0
dt = 0.1

images = {
    "BABY_DANIEL": ["https://i.ibb.co/pjkg62st/baby-daniel.jpg", 134, 170, 0.1],
    "BABY_FLINT": ["https://i.ibb.co/b43jm6f/baby-flint.jpg", 0.1],
    "MOM_DANIEL": ["https://i.ibb.co/psXhSLX/mom-daniel.jpg", 0.1],
    "MOM_FLINT": ["https://i.ibb.co/V0cyPxV6/mom-flint.jpg", 0.1],
}

length = 0

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


def set_length(evt):
    length = evt.value

length_slider = slider(bind=set_length, min=0, max=50)

swing1 = Swing(
    color.red,
    color.blue,
    20,
    15,
    0,
    0.2,
    0.3,
    393,
    0.51111,
    0.15,
    0.1,
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
