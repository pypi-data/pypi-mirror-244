import numpy as np


class TimingRun:
    def __init__(self, data):
        self.data = data

    def get_names(self):
        """!
        Return the names of the available timing fields
        """
        return self.data.dtype.names

    def get_data(self):
        """!
        Return the raw numpy data for this run
        """
        return self.data

    def plot(self, save=None, acc=False, fields=None, ls="-", c=None, prepend=""):
        """!
        Plot the timing information for a given run and set of fields.

        @param save If given, the figure is saved to that file, otherwise is shown
        @param acc Plot the accumulated times
        @param fields If not none, select a subsample of timing information to plot
        @param ls Line styles for the plots. It can either be an array of the same
                size as fields or a single style to be applied to all fields.
                This is directly passed to matplotlib.
        @param c Save as ls, but for the color information.
                This is directly passed to matplotlib.
        @param prepend String to prepend to the variable names in the legend
        """

        import matplotlib.pyplot as plt
        from matplotlib import cm

        if fields is None:
            names = self.data.dtype.names[1:]
        else:
            names = fields

        if acc:
            for name in names:
                self.data[name] = np.cumsum(self.data[name])

        # Use some colormaps to avoid cycling over the default matplotlib colors,
        # which are, in general, not enough
        if c == None:
            c_space = np.linspace(0, 0.9, len(names))
            colors = [cm.gist_ncar(x) for x in c_space]
        else:
            if type(c) == str:
                colors = [c] * len(names)
            elif len(c) == len(names):
                colors = c
            else:
                raise ValueError("c does not have the correct type and/or length")

        if type(ls) == str:
            linestyles = [ls] * len(names)
        elif len(ls) == len(names):
            linestyles = ls
        else:
            raise ValueError("ls does not have the correct type and/or length")

        # Add a last space to prepend if it does not have one
        if len(prepend) > 1 and prepend[-1] != " ":
            prepend += " "

        for name, ci, lsi in zip(names, colors, linestyles):
            plt.plot(
                self.data["Step"],
                self.data[name],
                alpha=0.8,
                label=prepend + name,
                c=ci,
                ls=lsi,
            )

        plt.legend(fontsize=7, bbox_to_anchor=(1.04, 1), loc="upper left")

        plt.xlabel("Step")

        prepend = ""
        unit = "s"
        if acc:
            prepend += "Accumulated "

        plt.ylabel(prepend + "Time [" + unit + "]")

        plt.xlim(self.data["Step"][0], self.data["Step"][-1])
        plt.tight_layout()
        plt.semilogy()

        if save is not None:
            plt.savefig(save)
            plt.clf()
        else:
            plt.show()


class Timing:
    """!
    Class to read and plot .timing files produced by PKDGRAV3.
    The data can be easily plotted and navigated with the plot() method,
    or can be accessed to further analysis using the [] syntax.

    This class can handle multiple runs in the same .timing file, and by
    defaults uses the last one.

    A typical example would be:
    >>> t = Timing("yourrun.timing")
    >>> len(t)
    >>> t.plot() #or t[-1].plot()
    >>> t.plot(acc=True, save="an_image.png")

    You can also get some information about the available fields:
    >>> t[0].get_names()
    >>> t[0].plot(fields=["Gravity","Flux"])
    """

    def __init__(self, filename):
        self.filename = filename

        # Parse to check how many runs are stored in this file
        self.nruns = 0
        self.nlines = {}
        with open(self.filename) as f:
            l = 0
            for line in f:
                if line[0] == "#":
                    self.nlines[self.nruns] = l
                    self.nruns += 1
                l += 1

    def __getitem__(self, index=-1):
        if index < 0:
            index = self.nruns + index

        if index == self.nruns - 1:
            nrows = None
        else:
            nrows = self.nlines[index + 1] - self.nlines[index] - 1

        if nrows is None or nrows > 0:
            return TimingRun(
                np.genfromtxt(
                    self.filename,
                    skip_header=self.nlines[index],
                    max_rows=nrows,
                    names=True,
                )
            )
        else:
            raise Exception("Trying to load an empty run!")

    def __len__(self):
        return self.nruns

    def get_names(self):
        """!
        Return the names of the available timing fields (of the last element)
        """
        return self.__getitem__().get_names()

    def plot(self, **kwargs):
        """!
        By default just plot the last run available in the file.
        """
        self.__getitem__().plot(**kwargs)
