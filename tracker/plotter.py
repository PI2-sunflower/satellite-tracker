import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pymap3d as pm

from tracker import conversions


def plot_az_el(az, el):
    plt.figure(num=1, figsize=(10, 10))

    visible, invisible = split_visible_points(az, el)
    points_color = {
        'b': az_el_to_theta_radius(visible),
        'r': az_el_to_theta_radius(invisible),
    }

    ax = plt.subplot(projection='polar')

    for color, points in points_color.items():
        if not points:
            continue

        x, y = list(zip(*points))
        ax.plot(x, y, marker='o', linestyle='', ms=5, color=color, alpha=0.75)

    ax.set_rticks([30.0, 60.0, 90.0])
    ax.set_xticklabels(['East', '', 'North', '', 'West', '', 'South', ''])
    ax.set_xlabel('x = azimuth [0, 360]', fontsize=15)
    ax.set_ylabel('y = elevation [-90, +90]', fontsize=15, labelpad=20)

    from matplotlib.patches import Circle, PathPatch

    circle = Circle((0, 0), 180, transform=ax.transData._b, color='grey',
                    alpha=0.5)
    ax.add_artist(circle)

    circle = Circle((0, 0), 90, transform=ax.transData._b, color='white')
    ax.add_artist(circle)


    visible_patch = mpatches.Patch(color='b', label='Visible satellites')
    invisible_patch = mpatches.Patch(color='r', label='Invisible satellites')
    invisible_area = mpatches.Patch(color='grey', label='Invisible area')

    plt.legend(handles=[visible_patch, invisible_patch, invisible_area])


def annotate_satellite(ax, az, el, dates):
    for i in range(len(az)):
        x = conversions.azimuth_to_theta(az[i])
        y = conversions.elevation_to_radius(el[i])
        xy = (x, y)

        label = '  {}'.format(i + 1)
        ax.annotate(label, xy, fontsize=12)

    points = list(zip(az, el, dates))
    df = pd.DataFrame(points, index=[i for i in range(1, len(points) + 1)],
                      columns=['Azimuth', 'Elevation', 'Time'])
    return df

def see_satellite(satellite, obs_lat, obs_lon, obs_alt, start, end, count=None, annotate=True, title=''):
    positions_at = satellite.propagate_positions(start, end, count=count)
    azimuth = []
    elevation = []

    for position_at in positions_at:
        eci, date = position_at
        aer = pm.eci2aer(eci, obs_lat, obs_lon, obs_alt, date)
        az = aer[0][0]
        el = aer[1][0]

        azimuth.append(az)
        elevation.append(el)

    plot_az_el(azimuth, elevation)
    dates = [x[1] for x in positions_at]
    ax = plt.gca()

    plt.suptitle(title, size=20)

    if annotate:
        df = annotate_satellite(ax, azimuth, elevation, dates)
        return df


def split_visible_points(x, y):
    visible = []
    invisible = []

    for i, yi in enumerate(y):
        point = (x[i], yi)
        if conversions.is_point_visible(yi):
            visible.append(point)
        else:
            invisible.append(point)
    return visible, invisible


def az_el_to_theta_radius(az_el):
    theta_radius = tuple(
        (conversions.azimuth_to_theta(x), conversions.elevation_to_radius(y)) for x, y in az_el)
    return theta_radius