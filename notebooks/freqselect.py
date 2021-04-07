import emg3d
import empymod
import numpy as np
import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display


class InteractiveFrequency(emg3d.utils.Fourier):
    """App to create required frequencies for Fourier Transform."""

    def __init__(self, src_z, rec_z, depth, res, time, signal=0, ab=11,
                 aniso=None, **kwargs):
        """App to create required frequencies for Fourier Transform.

        No thorough input checks are carried out. Rubbish in, rubbish out.

        See empymod.model.dipole for details regarding the modelling.


        Parameters
        ----------
        src_z, rec_z : floats
            Source and receiver depths and offset. The source is located at
            src=(0, 0, src_z), the receiver at rec=(off, 0, rec_z).

        depth : list
            Absolute layer interfaces z (m); #depth = #res - 1
            (excluding +/- infinity).

        res : array_like
            Horizontal resistivities rho_h (Ohm.m); #res = #depth + 1.

        time : array_like
            Times t (s).

        signal : {0, 1, -1}, optional
            Source signal, default is 0:
                - -1 : Switch-off time-domain response
                - 0 : Impulse time-domain response
                - +1 : Switch-on time-domain response

        ab : int, optional
            Source-receiver configuration, defaults to 11. (See
            empymod.model.dipole for all possibilities.)

        aniso : array_like, optional
            Anisotropies lambda = sqrt(rho_v/rho_h) (-); #aniso = #res.
            Defaults to ones.

        **kwargs : Optional parameters:

            - ``fmin`` : float
              Initial minimum frequency. Default is 1e-3.

            - ``fmax`` : float
              Initial maximum frequency. Default is 1e1.

            - ``off`` : float
              Initial offset. Default is 500.

            - ``ft`` : str {'dlf', 'fftlog'}
              Initial Fourier transform method. Default is 'dlf'.

            - ``ftarg`` : dict
              Initial Fourier transform arguments corresponding to ``ft``.
              Default is None.

            - ``pts_per_dec`` : int
              Initial points per decade. Default is 5.

            - ``linlog`` : str {'linear', 'log'}
              Initial display scaling. Default is 'linear'.

            - ``xtfact`` : float
              Factor for linear x-dimension: t_max = xtfact*offset/1000.

            - ``verb`` : int
              Verbosity. Only for debugging purposes.

        """
        # Get initial values or set to default.
        fmin = kwargs.pop('fmin', 1e-3)
        fmax = kwargs.pop('fmax', 1e1)
        off = kwargs.pop('off', 5000)
        ft = kwargs.pop('ft', 'dlf')
        ftarg = kwargs.pop('ftarg', None)
        self.pts_per_dec = kwargs.pop('pts_per_dec', 5)
        self.linlog = kwargs.pop('linlog', 'linear')
        self.xtfact = kwargs.pop('xtfact', 1)
        self.verb = kwargs.pop('verb', 1)

        # Ensure no kwargs left.
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)

        # Collect model from input.
        self.model = {
            'src': [0, 0, src_z],
            'rec': [off, 0, rec_z],
            'depth': depth,
            'res': res,
            'aniso': aniso,
            'ab': ab,
            'verb': self.verb,
        }

        # Initiate a Fourier instance.
        super().__init__(time, fmin, fmax, signal, ft, ftarg, verb=self.verb)

        # Create the figure.
        self.initiate_figure()

    def initiate_figure(self):
        """Create the figure."""

        # Create figure and all axes
        fig = plt.figure("Interactive frequency selection for the Fourier "
                         "Transform.", figsize=(9, 4))
        plt.subplots_adjust(hspace=0.03, wspace=0.04, bottom=0.15, top=0.9)
        # plt.tight_layout(rect=[0, 0, 1, 0.95])  # Leave space for suptitle.
        ax1 = plt.subplot2grid((3, 2), (0, 0), rowspan=2)
        plt.grid('on', alpha=0.4)
        ax2 = plt.subplot2grid((3, 2), (0, 1), rowspan=2)
        plt.grid('on', alpha=0.4)
        ax3 = plt.subplot2grid((3, 2), (2, 0))
        plt.grid('on', alpha=0.4)
        ax4 = plt.subplot2grid((3, 2), (2, 1))
        plt.grid('on', alpha=0.4)

        # Synchronize x-axis, switch upper labels off
        ax1.get_shared_x_axes().join(ax1, ax3)
        ax2.get_shared_x_axes().join(ax2, ax4)
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)

        # Move labels of t-domain to the right
        ax2.yaxis.set_ticks_position('right')
        ax4.yaxis.set_ticks_position('right')

        # Set fixed limits
        ax1.set_xscale('log')
        ax3.set_yscale('log')
        ax3.set_yscale('log')
        ax3.set_ylim([0.007, 141])
        ax3.set_yticks([0.01, 0.1, 1, 10, 100])
        ax3.set_yticklabels(('0.01', '0.1', '1', '10', '100'))
        ax4.set_yscale('log')
        ax4.set_yscale('log')
        ax4.set_ylim([0.007, 141])
        ax4.set_yticks([0.01, 0.1, 1, 10, 100])
        ax4.set_yticklabels(('0.01', '0.1', '1', '10', '100'))

        # Labels etc
        ax1.set_ylabel('Amplitude (V/m)')
        ax3.set_ylabel('Rel. Error (%)')
        ax3.set_xlabel('Frequency (Hz)')
        ax4.set_xlabel('Time (s)')
        ax3.axhline(1, c='0.4')
        ax4.axhline(1, c='0.4')

        # Add instances
        self.fig = fig
        self.axs = [ax1, ax2, ax3, ax4]

        # Plot initial base model
        self.update_ftfilt(self.ftarg)
        self.plot_base_model()

        # Initiate the widgets
        self.create_widget()

    def reim(self, inp):
        """Return real or imaginary part as a function of signal."""
        if self.signal < 0:
            return inp.real
        else:
            return inp.imag

    def create_widget(self):
        """Create widgets and their layout."""

        # Offset slider.
        off = widgets.interactive(
            self.update_off,
            off=widgets.IntSlider(
                min=500,
                max=10000,
                description='Offset (m)',
                value=self.model['rec'][0],
                step=250,
                continuous_update=False,
                style={'description_width': '60px'},
                layout={'width': '260px'},
            ),
        )

        # Pts/dec slider.
        pts_per_dec = widgets.interactive(
            self.update_pts_per_dec,
            pts_per_dec=widgets.IntSlider(
                min=1,
                max=10,
                description='pts/dec',
                value=self.pts_per_dec,
                step=1,
                continuous_update=False,
                style={'description_width': '60px'},
                layout={'width': '260px'},
            ),
        )

        # Linear/logarithmic selection.
        linlog = widgets.interactive(
            self.update_linlog,
            linlog=widgets.ToggleButtons(
                value=self.linlog,
                options=['linear', 'log'],
                description='Display',
                style={'description_width': '60px', 'button_width': '100px'},
            ),
        )

        # Frequency-range slider.
        freq_range = widgets.interactive(
            self.update_freq_range,
            freq_range=widgets.FloatRangeSlider(
                value=[np.log10(self.fmin), np.log10(self.fmax)],
                description='f-range',
                min=-4,
                max=3,
                step=0.1,
                continuous_update=False,
                style={'description_width': '60px'},
                layout={'width': '260px'},
            ),
        )

        # Signal selection (-1, 0, 1).
        signal = widgets.interactive(
            self.update_signal,
            signal=widgets.ToggleButtons(
                value=self.signal,
                options=[-1, 0, 1],
                description='Signal',
                style={'description_width': '60px', 'button_width': '65px'},
            ),
        )

        # Fourier transform method selection.
        def _get_init():
            """Return initial choice of Fourier Transform."""
            if self.ft == 'fftlog':
                return self.ft
            else:
                return self.ftarg['dlf'].savename

        ftfilt = widgets.interactive(
            self.update_ftfilt,
            ftfilt=widgets.Dropdown(
                options=['fftlog', 'key_81_CosSin_2009',
                         'key_241_CosSin_2009', 'key_601_CosSin_2009',
                         'key_101_CosSin_2012', 'key_201_CosSin_2012'],
                description='Fourier',
                value=_get_init(),  # Initial value
                style={'description_width': '60px'},
                layout={'width': 'max-content'},
            ),
        )

        # Group them together.
        t1col1 = widgets.VBox(children=[pts_per_dec, freq_range],
                              layout={'width': '310px'})
        t1col2 = widgets.VBox(children=[off, ftfilt],
                              layout={'width': '310px'})
        t1col3 = widgets.VBox(children=[signal, linlog],
                              layout={'width': '310px'})

        # Group them together.
        display(widgets.HBox(children=[t1col1, t1col2, t1col3]))

    # Plotting and calculation routines.
    def clear_handle(self, handles):
        """Clear `handles` from figure."""
        for hndl in handles:
            if hasattr(self, 'h_'+hndl):
                getattr(self, 'h_'+hndl).remove()

    def adjust_lim(self):
        """Adjust axes limits."""

        # Adjust y-limits f-domain
        if self.linlog == 'linear':
            self.axs[0].set_ylim([1.1*min(self.reim(self.f_dense)),
                                  1.5*max(self.reim(self.f_dense))])
        else:
            self.axs[0].set_ylim([5*min(self.reim(self.f_dense)),
                                  5*max(self.reim(self.f_dense))])

        # Adjust x-limits f-domain
        self.axs[0].set_xlim([min(self.freq_req), max(self.freq_req)])

        # Adjust y-limits t-domain
        if self.linlog == 'linear':
            self.axs[1].set_ylim(
                    [min(-max(self.t_base)/20, 0.9*min(self.t_base)),
                     max(-min(self.t_base)/20, 1.1*max(self.t_base))])
        else:
            self.axs[1].set_ylim([10**(np.log10(max(self.t_base))-5),
                                  1.5*max(self.t_base)])

        # Adjust x-limits t-domain
        if self.linlog == 'linear':
            if self.signal == 0:
                self.axs[1].set_xlim(
                        [0, self.xtfact*self.model['rec'][0]/1000])
            else:
                self.axs[1].set_xlim([0, max(self.time)])
        else:
            self.axs[1].set_xlim([min(self.time), max(self.time)])

    def print_legend(self):
        """Update suptitle."""
        # plt.suptitle(
        #     f"Offset = {np.squeeze(self.model['rec'][0])/1000} km;    "
        #     f"No. freq. coarse: {self.freq_calc.size};    No. freq. full: "
        #     f"{self.freq_req.size}  ({self.freq_req.min():.1e} $-$ "
        #     f"{self.freq_req.max():.1e} Hz)")
        self.clear_handle(['f_legend', ])
        self.h_f_legend = self.axs[0].legend(
            handles=[self.h_f_inti, self.h_f_int],
            labels=[f"required ({self.freq_req.size})",
                    f"computed ({self.freq_calc.size})"]
        )

    def plot_base_model(self):
        """Update smooth, 'correct' model."""

        # Calculate responses
        self.f_dense = empymod.dipole(freqtime=self.freq_dense, **self.model)
        self.t_base = empymod.dipole(
            freqtime=self.time, signal=self.signal, **self.model)

        # Clear existing handles
        self.clear_handle(['f_base', 't_base'])

        # Plot new result
        self.h_f_base, = self.axs[0].plot(
                self.freq_dense, self.reim(self.f_dense), 'C3')
        self.h_t_base, = self.axs[1].plot(self.time, self.t_base, 'C3')

        self.adjust_lim()

    def plot_coarse_model(self):
        """Update coarse model."""

        # Calculate the f-responses for required and the calculation range.
        f_req = empymod.dipole(freqtime=self.freq_req, **self.model)
        f_calc = empymod.dipole(freqtime=self.freq_calc, **self.model)

        # Interpolate from calculated to required frequencies and transform.
        f_int = self.interpolate(f_calc)
        t_int = self.freq2time(f_calc, self.model['rec'][0])

        # Calculate the errors.
        f_error = 100*abs((self.reim(f_int)-self.reim(f_req)) /
                          self.reim(f_req))
        t_error = 100*abs((t_int-self.t_base)/self.t_base)

        # Clear existing handles
        self.clear_handle(['f_int', 't_int', 'f_inti', 'f_inte', 't_inte'])

        # Plot frequency-domain result
        self.h_f_inti, = self.axs[0].plot(
                self.freq_req, self.reim(f_int), 'k.', ms=4)
        self.h_f_int, = self.axs[0].plot(
                self.freq_calc, self.reim(f_calc), 'C0.', ms=8)
        self.h_f_inte, = self.axs[2].plot(self.freq_req, f_error, 'k')

        # Plot time-domain result
        self.h_t_int, = self.axs[1].plot(self.time, t_int, 'k--')
        self.h_t_inte, = self.axs[3].plot(self.time, t_error, 'k')

        # Update legend
        self.print_legend()

    # Interactive routines
    def update_off(self, off):
        """Offset-slider"""

        # Update model
        self.model['rec'] = [off, self.model['rec'][1], self.model['rec'][2]]

        # Redraw models
        self.plot_base_model()
        self.plot_coarse_model()

    def update_pts_per_dec(self, pts_per_dec):
        """pts_per_dec-slider."""

        # Store pts_per_dec.
        self.pts_per_dec = pts_per_dec

        # Redraw through update_ftfilt.
        self.update_ftfilt(self.ftarg)

    def update_freq_range(self, freq_range):
        """Freq-range slider."""

        # Update values
        self.fmin = 10**freq_range[0]
        self.fmax = 10**freq_range[1]

        # Redraw models
        self.plot_coarse_model()

    def update_ftfilt(self, ftfilt):
        """Ftfilt dropdown."""

        # Check if FFTLog or DLF; git DLF filter.
        if isinstance(ftfilt, str):
            fftlog = ftfilt == 'fftlog'
        else:
            if 'dlf' in ftfilt:
                fftlog = False
                ftfilt = ftfilt['dlf'].savename
            else:
                fftlog = True

        # Update Fourier arguments.
        if fftlog:
            self.fourier_arguments('fftlog', {'pts_per_dec': self.pts_per_dec})
            self.freq_inp = None

        else:
            # Calculate input frequency from min to max with pts_per_dec.
            lmin = np.log10(self.freq_req.min())
            lmax = np.log10(self.freq_req.max())
            self.freq_inp = np.logspace(
                    lmin, lmax, int(self.pts_per_dec*np.ceil(lmax-lmin)))

            self.fourier_arguments(
                    'dlf', {'dlf': ftfilt, 'pts_per_dec': -1})

        # Dense frequencies for comparison reasons
        self.freq_dense = np.logspace(np.log10(self.freq_req.min()),
                                      np.log10(self.freq_req.max()), 301)

        # Redraw models
        self.plot_base_model()
        self.plot_coarse_model()

    def update_linlog(self, linlog):
        """Adjust x- and y-scaling of both frequency- and time-domain."""

        # Store linlog
        self.linlog = linlog

        # f-domain: x-axis always log; y-axis linear or symlog.
        if linlog == 'log':
            sym_dec = 10  # Number of decades to show on symlog
            lty = int(max(np.log10(abs(self.reim(self.f_dense))))-sym_dec)
            self.axs[0].set_yscale('symlog', linthresh=10**lty, linscale=0.7)

            # Remove the zero line becouse of the overlapping ticklabels.
            nticks = len(self.axs[0].get_yticks())//2
            iticks = np.arange(nticks)
            iticks = np.r_[iticks, iticks+nticks+1]
            self.axs[0].set_yticks(self.axs[0].get_yticks()[iticks])

        else:
            self.axs[0].set_yscale(linlog)

        # t-domain: either linear or loglog
        self.axs[1].set_yscale(linlog)
        self.axs[1].set_xscale(linlog)

        # Adjust limits
        self.adjust_lim()

    def update_signal(self, signal):
        """Use signal."""

        # Store signal.
        self.signal = signal

        # Redraw through update_ftfilt.
        self.update_ftfilt(self.ftarg)
