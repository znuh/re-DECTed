#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Dectrx
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import osmosdr
import time
from gnuradio import qtgui

class Dectrx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Dectrx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Dectrx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Dectrx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.rf_gain = rf_gain = 10
        self.ppm = ppm = 0
        self.if_gain = if_gain = 20
        self.channel = channel = 3
        self.bb_gain = bb_gain = 20
        self.variable_qtgui_range_1_0 = variable_qtgui_range_1_0 = channel
        self.variable_qtgui_range_1 = variable_qtgui_range_1 = ppm
        self.variable_qtgui_range_0_1 = variable_qtgui_range_0_1 = bb_gain
        self.variable_qtgui_range_0_0 = variable_qtgui_range_0_0 = if_gain
        self.variable_qtgui_range_0 = variable_qtgui_range_0 = rf_gain
        self.samp_rate = samp_rate = 2.4e6
        self.freq = freq = 1897.344e6-(channel*1.728e6)
        self.dect_rate = dect_rate = 1.152e6

        ##################################################
        # Blocks
        ##################################################
        self._variable_qtgui_range_1_0_range = Range(1, 12, 1, channel, 200)
        self._variable_qtgui_range_1_0_win = RangeWidget(self._variable_qtgui_range_1_0_range, self.set_variable_qtgui_range_1_0, 'Channel', "counter_slider", int)
        self.top_grid_layout.addWidget(self._variable_qtgui_range_1_0_win)
        self._variable_qtgui_range_1_range = Range(-70, 70, 1, ppm, 200)
        self._variable_qtgui_range_1_win = RangeWidget(self._variable_qtgui_range_1_range, self.set_variable_qtgui_range_1, 'PPM', "counter_slider", int)
        self.top_grid_layout.addWidget(self._variable_qtgui_range_1_win)
        self._variable_qtgui_range_0_1_range = Range(0, 100, 1, bb_gain, 200)
        self._variable_qtgui_range_0_1_win = RangeWidget(self._variable_qtgui_range_0_1_range, self.set_variable_qtgui_range_0_1, 'BB Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._variable_qtgui_range_0_1_win)
        self._variable_qtgui_range_0_0_range = Range(0, 100, 1, if_gain, 200)
        self._variable_qtgui_range_0_0_win = RangeWidget(self._variable_qtgui_range_0_0_range, self.set_variable_qtgui_range_0_0, 'IF Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._variable_qtgui_range_0_0_win)
        self._variable_qtgui_range_0_range = Range(0, 100, 1, rf_gain, 200)
        self._variable_qtgui_range_0_win = RangeWidget(self._variable_qtgui_range_0_range, self.set_variable_qtgui_range_0, 'RF Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._variable_qtgui_range_0_win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=24,
                decimation=25,
                taps=None,
                fractional_bw=None)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            52, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            freq, #bw
            'Waterfall Plot', #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'numchan=1 '
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(ppm, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(dect_rate, 0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                dect_rate,
                10e3,
                firdes.WIN_HAMMING,
                6.76))
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0.0,
            verbose=False,log=False)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 2323, 1472, True)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_gmsk_demod_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Dectrx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.set_variable_qtgui_range_0(self.rf_gain)
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm
        self.set_variable_qtgui_range_1(self.ppm)
        self.osmosdr_source_0.set_freq_corr(self.ppm, 0)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.set_variable_qtgui_range_0_0(self.if_gain)
        self.osmosdr_source_0.set_if_gain(self.if_gain, 0)

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self.set_freq(1897.344e6-(self.channel*1.728e6))
        self.set_variable_qtgui_range_1_0(self.channel)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.set_variable_qtgui_range_0_1(self.bb_gain)
        self.osmosdr_source_0.set_bb_gain(self.bb_gain, 0)

    def get_variable_qtgui_range_1_0(self):
        return self.variable_qtgui_range_1_0

    def set_variable_qtgui_range_1_0(self, variable_qtgui_range_1_0):
        self.variable_qtgui_range_1_0 = variable_qtgui_range_1_0

    def get_variable_qtgui_range_1(self):
        return self.variable_qtgui_range_1

    def set_variable_qtgui_range_1(self, variable_qtgui_range_1):
        self.variable_qtgui_range_1 = variable_qtgui_range_1

    def get_variable_qtgui_range_0_1(self):
        return self.variable_qtgui_range_0_1

    def set_variable_qtgui_range_0_1(self, variable_qtgui_range_0_1):
        self.variable_qtgui_range_0_1 = variable_qtgui_range_0_1

    def get_variable_qtgui_range_0_0(self):
        return self.variable_qtgui_range_0_0

    def set_variable_qtgui_range_0_0(self, variable_qtgui_range_0_0):
        self.variable_qtgui_range_0_0 = variable_qtgui_range_0_0

    def get_variable_qtgui_range_0(self):
        return self.variable_qtgui_range_0

    def set_variable_qtgui_range_0(self, variable_qtgui_range_0):
        self.variable_qtgui_range_0 = variable_qtgui_range_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.dect_rate, 10e3, firdes.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0.set_center_freq(self.freq, 0)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.freq)

    def get_dect_rate(self):
        return self.dect_rate

    def set_dect_rate(self, dect_rate):
        self.dect_rate = dect_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.dect_rate, 10e3, firdes.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_bandwidth(self.dect_rate, 0)



def main(top_block_cls=Dectrx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
