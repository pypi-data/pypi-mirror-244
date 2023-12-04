from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
if __name__ == "__main__":
    from hydrogibs import constants as cst
else:
    from .. import constants as cst

rho_s = 2650
rho = cst.rho
g = cst.g
nu_k = cst.nu_k


def adimensional_diameter(di, solid_density, nu=nu_k):
    return di*((solid_density/rho-1)*g/nu_k**2)**(1/3)


def reynolds(u_star, d, nu=nu_k):
    return u_star * d / nu


def adimensional_shear(shear, d, solid_density, g=g):
    return shear/((solid_density - rho)*g*d)


def smart_jaeggi(h, i, s, theta_cr, Dm):
    return 4.2/(s - 1) * i**1.6 * (1 - theta_cr*(s-1)*Dm/h/i)


DIR = Path(__file__).parent
shields = pd.read_csv(DIR / "shields.csv")
vanrijn = pd.read_csv(DIR / "shields-vanrijn.csv")


class ShieldsDiagram:

    def __init__(self,
                 figure=None,
                 axShields=None,
                 axVanRijn=None,
                 subplots_dict=None,
                 plot_kw=None,
                 *figure_args,
                 **figure_kwargs) -> None:

        if subplots_dict is None:
            subplots_dict = dict()
        subplots_dict = dict(ncols=2, gridspec_kw=dict(wspace=0)) | subplots_dict

        if axShields is None and axVanRijn is None:
            figure = plt.figure(*figure_args, **figure_kwargs)
            axShields, axVanRijn = figure.subplots(**subplots_dict)

        if plot_kw is None:
            plot_kw = dict()
        axShields.loglog(shields.reynolds, shields.shear, **plot_kw)
        axVanRijn.loglog(vanrijn.diameter, vanrijn.shear, **plot_kw)

        axShields.set_title("Diagramme de Shields")
        axShields.set_xlabel(r"Reynolds $R=u_\ast d/\nu$")
        axShields.set_ylabel(r"$\Theta=\tau/(\rho g[s-1]d)$""\nCisaillement critique adimensionnel")

        axVanRijn.set_title("Selon Van Rijn")
        axVanRijn.yaxis.tick_right()
        axVanRijn.yaxis.set_label_position('right')
        axVanRijn.set_xlabel(r"Diamètre adimentionnel $d_\ast=d\cdot\sqrt[3]{(s-1)g/\nu^2}$")
        axVanRijn.set_ylabel("Cisaillement critique adimensionnel\n"r"$\Theta=\tau/(\rho g[s-1]d)$")

        self.figure = figure
        self.axShields = axShields
        self.axVanRijn = axVanRijn

    def plot(self, adim_shear, reynolds=None, adim_diam=None, *plot_args, **plot_kwargs):

        if reynolds is not None:
            self.axShields.plot(reynolds, adim_shear, *plot_args, **plot_kwargs)
        if adim_diam is not None:
            self.axVanRijn.plot(adim_diam, adim_shear, *plot_args, **plot_kwargs)

    def scatter(self, adim_shear, reynolds=None, adim_diam=None, *scatter_args, **scatter_kwargs):

        if reynolds is not None:
            self.axShields.scatter(reynolds, adim_shear, *scatter_args, **scatter_kwargs)
        if adim_diam is not None:
            self.axVanRijn.scatter(adim_diam, adim_shear, *scatter_args, **scatter_kwargs)
    
    def get_subplots(self):
        return self.fig, self.ax1, self.ax2


def main():

    from canal import Section

    df = pd.read_csv(DIR / 'profile.csv')
    section = Section(
        df['Dist. cumulée [m]'],
        df['Altitude [m s.m.]'],
    ).compute_GMS_data(33, 0.12/100)

    grains = pd.read_csv("hydrogibs/fluvial/grains.csv")
    granulometry = interp1d(grains["Tamisats [%]"], grains["Diamètre des grains [cm]"])
    d16, d50, d90 = granulometry((16, 50, 90))
    sd = ShieldsDiagram()
    S, P = section.data.query("300 <= Q <= 1600")[["S", "P"]].to_numpy().T
    for d in (d16, d50, d90):
        Rh = S/P
        shear = rho*g*Rh*0.12/100
        diam = np.full_like(Rh, fill_value=d/100)
        r = reynolds(np.sqrt(shear/rho), diam)
        s = adimensional_shear(shear, diam, rho_s)
        d = adimensional_diameter(diam, rho_s)
        sd.plot(s, r, d)
    sd.figure.show()
    plt.show()


if __name__ == "__main__":
    main()
