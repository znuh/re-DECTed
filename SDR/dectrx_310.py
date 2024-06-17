#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Dectrx 310
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
import osmosdr
import time
import sip



class dectrx_310(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Dectrx 310", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Dectrx 310")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "dectrx_310")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.rf_gain = rf_gain = 10
        self.range_channel = range_channel = 5
        self.ppm = ppm = 0
        self.if_gain = if_gain = 20
        self.bb_gain = bb_gain = 20
        self.samp_rate = samp_rate = 2.4e6
        self.range_rf_gain = range_rf_gain = rf_gain
        self.range_ppm = range_ppm = ppm
        self.range_if_gain = range_if_gain = if_gain
        self.range_bb_gain = range_bb_gain = bb_gain
        self.freq = freq = 1897.344e6-(range_channel*1.728e6)
        self.dect_rate = dect_rate = 1.152e6

        ##################################################
        # Blocks
        ##################################################

        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=24,
                decimation=25,
                taps=[],
                fractional_bw=0)
        self._range_rf_gain_range = qtgui.Range(0, 100, 1, rf_gain, 200)
        self._range_rf_gain_win = qtgui.RangeWidget(self._range_rf_gain_range, self.set_range_rf_gain, "RF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._range_rf_gain_win)
        self._range_ppm_range = qtgui.Range(-70, 70, 1, ppm, 200)
        self._range_ppm_win = qtgui.RangeWidget(self._range_ppm_range, self.set_range_ppm, "PPM", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._range_ppm_win)
        self._range_if_gain_range = qtgui.Range(0, 100, 1, if_gain, 200)
        self._range_if_gain_win = qtgui.RangeWidget(self._range_if_gain_range, self.set_range_if_gain, "IF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._range_if_gain_win)
        self._range_channel_range = qtgui.Range(0, 9, 1, 5, 200)
        self._range_channel_win = qtgui.RangeWidget(self._range_channel_range, self.set_range_channel, "Channel", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._range_channel_win)
        self._range_bb_gain_range = qtgui.Range(0, 100, 1, bb_gain, 200)
        self._range_bb_gain_win = qtgui.RangeWidget(self._range_bb_gain_range, self.set_range_bb_gain, "BB Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._range_bb_gain_win)
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'After filter', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_0_win)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
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

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'hackrf=0'
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(ppm, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
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
                window.WIN_HAMMING,
                6.76))
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0,
            verbose=False,log=False)
        self.blocks_udp_sink_0 = network.udp_sink(gr.sizeof_char, 1, '127.0.0.1', 2323, 0, 1472, True)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_gmsk_demod_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "dectrx_310")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.set_range_rf_gain(self.rf_gain)
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_range_channel(self):
        return self.range_channel

    def set_range_channel(self, range_channel):
        self.range_channel = range_channel
        self.set_freq(1897.344e6-(self.range_channel*1.728e6))

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm
        self.set_range_ppm(self.ppm)
        self.osmosdr_source_0.set_freq_corr(self.ppm, 0)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.set_range_if_gain(self.if_gain)
        self.osmosdr_source_0.set_if_gain(self.if_gain, 0)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.set_range_bb_gain(self.bb_gain)
        self.osmosdr_source_0.set_bb_gain(self.bb_gain, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.dect_rate, 10e3, window.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(0, self.samp_rate)

    def get_range_rf_gain(self):
        return self.range_rf_gain

    def set_range_rf_gain(self, range_rf_gain):
        self.range_rf_gain = range_rf_gain

    def get_range_ppm(self):
        return self.range_ppm

    def set_range_ppm(self, range_ppm):
        self.range_ppm = range_ppm

    def get_range_if_gain(self):
        return self.range_if_gain

    def set_range_if_gain(self, range_if_gain):
        self.range_if_gain = range_if_gain

    def get_range_bb_gain(self):
        return self.range_bb_gain

    def set_range_bb_gain(self, range_bb_gain):
        self.range_bb_gain = range_bb_gain

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0.set_center_freq(self.freq, 0)

    def get_dect_rate(self):
        return self.dect_rate

    def set_dect_rate(self, dect_rate):
        self.dect_rate = dect_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.dect_rate, 10e3, window.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_bandwidth(self.dect_rate, 0)




def main(top_block_cls=dectrx_310, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
