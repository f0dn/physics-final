from math import cos, sin
from vpython import sign, sphere, vector, color, rate, graph, gcurve

ang_velocity_graph = graph(
    title="Pendulum Angular Velocity", xtitle="Time (s)", ytitle="Velocity (m/s)"
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
pendulum_mass = 5
pendulum_ang_velocity = 1
pendulum_ang = 0
pendulum_moment = pendulum_mass * pendulum_length**2 / 2
gravity = vector(0, -9.81, 0)

friction_coefficient = 0.5

external_force_amplitude = 30
external_force_frequency = 1

t = 0
dt = 0.01

while True:
    rate(1000)
    friction_force = -friction_coefficient * pendulum_ang_velocity
    external_force = external_force_amplitude * cos(external_force_frequency * t)
    torque = (
        (pendulum_mass * gravity).cross(pendulum.pos)
        + friction_force * pendulum_length * vector(0, 0, -1)
        + external_force * vector(0, 0, -1)
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
