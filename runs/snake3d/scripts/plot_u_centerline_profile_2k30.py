"""Plot the centerline mean streamwise velocity."""

import pathlib

import numpy
import pyvista
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line(is_slow=True)

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

cases = {
    'both_lips': {'2k': [30]},
    'back_lip': {'2k': [30]},
    'front_lip': {'2k': [30]},
    'no_lips': {'2k': [30]}
}

times = numpy.round(
    numpy.arange(start=100, stop=200 + 1e-3, step=0.05),
    decimals=2
)

data = dict()
body = dict()
for lip_cfg in cases.keys():
    for Re, angles in cases[lip_cfg].items():
        for AoA in angles:
            vel_obj = rodney.UxCenterlineData(
                None, maindir / lip_cfg / f'{Re}{AoA}'
            )

            if args.compute:
                vel_obj.compute(times, from_tarball=True)
                vel_obj.save('u_centerline_profile_100_200.txt')
            else:
                vel_obj.load('u_centerline_profile_100_200.txt')

            data[f'{lip_cfg}_{Re}{AoA}'] = vel_obj

            filepath = (maindir / lip_cfg / f'{Re}{AoA}' /
                        'RANS' / 'constant' / 'triSurface' / 'snake.obj')
            _body = pyvista.get_reader(str(filepath)).read()
            _body = _body.slice(normal='z')
            xb, yb = _body.points[:, 0], _body.points[:, 1]

            body[f'{lip_cfg}_{Re}{AoA}'] = (xb, yb)

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

plt_kwargs = {
    'both_lips_2k30': dict(label='both lips', color='C0', linestyle='-'),
    'back_lip_2k30': dict(label='back lip', color='C1', linestyle='-'),
    'front_lip_2k30': dict(label='front lip', color='C2', linestyle='-'),
    'no_lips_2k30': dict(label='no lips', color='C3', linestyle='-')
}

# Plot profile of the mean streamwise velocity along the centerline.
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('x / D')
ax.set_ylabel(r'$<u> / U_\infty$')
U_inf, D = 1.0, 1.0
ax.axhline(0.0, color='gray', linestyle='--')
for label, vel_obj in data.items():
    ax.plot(vel_obj.x / D, vel_obj.values / U_inf, **plt_kwargs[label])
ax.set_xlim(0.0, 4.0)
inset_ax = fig.add_axes([0.1, 0.7, 0.2, 0.2])
for label, vel_obj in data.items():
    inset_ax.plot(*body[label], **plt_kwargs[label])
    inset_ax.axhline(0.0, xmin=0.6, xmax=1.0, color='gray', linestyle='--')
inset_ax.axis('scaled')
inset_ax.axis('off')
ax.legend(frameon=False, loc='center right')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_centerline_profile_2k30.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
