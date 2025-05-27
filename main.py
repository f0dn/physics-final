from math import cos, sin
from vpython import sign, sphere, vector, color, rate, graph, gcurve

ang_velocity_graph = graph(
    title="Pendulum Angular Velocity",
    xtitle="Time (s)",
    ytitle="Velocity (m/s)",
    scroll=True,
    xmin=0,
    xmax=1000,
)
pendulum_graph = gcurve(color=color.red, graph=ang_velocity_graph)
phase_space_graph = graph(
    title="Pendulum Phase Space",
    xtitle="Angle (rad)",
    ytitle="Angular Velocity (rad/s)",
)
pendulum_phase_space = gcurve(color=color.blue, graph=phase_space_graph)

pendulum_length = 20
pendulum = sphere(pos=vector(0, -pendulum_length, 0), radius=1, color=color.red)
pendulum_mass = 20
pendulum_ang_velocity = 1
pendulum_ang = -0.2
pendulum_moment = pendulum_mass * pendulum_length**2 / 2
gravity = vector(0, -9.81, 0)

friction_coefficient = 0.3

external_force_amplitude = 85
external_force_frequency = 1

push_angle = 0.15
effective_angle_diff = 0.1

t = 0
dt = 0.1

while True:
    rate(1000)
    friction_force = -friction_coefficient * pendulum_ang_velocity
    external_force = external_force_amplitude * cos(external_force_frequency * t) if abs(pendulum_ang) < push_angle else 0
    torque = (
        (pendulum_mass * gravity).cross(pendulum.pos)
        + friction_force * pendulum_length * vector(0, 0, -1)
        + external_force * abs(cos(pendulum_ang + effective_angle_diff)) * vector(0, 0, -1)
    )
    ang_accel = -(torque.mag * sign(torque.z)) / pendulum_moment
    pendulum_ang_velocity += ang_accel * dt
    pendulum_ang += pendulum_ang_velocity * dt
    pendulum.pos = vector(
        pendulum_length * sin(pendulum_ang), -pendulum_length * cos(pendulum_ang), 0
    )

    pendulum_graph.plot(t, pendulum_ang_velocity)
    pendulum_phase_space.plot(pendulum_ang, pendulum_ang_velocity)

    t += dt
