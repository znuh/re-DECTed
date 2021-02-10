#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Dect Multirx
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
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
import osmosdr
import time
from gnuradio import qtgui

class dect_multirx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Dect Multirx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Dect Multirx")
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

        self.settings = Qt.QSettings("GNU Radio", "dect_multirx")

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
        self.symbol_rate = symbol_rate = 1.152e6
        self.samp_rate = samp_rate = 20e6
        self.rf_gain = rf_gain = 10
        self.ppm = ppm = 0
        self.if_gain = if_gain = 20
        self.channels = channels = 11
        self.ch_tb = ch_tb = 1.728e6-symbol_rate
        self.ch_bw = ch_bw = 1.728e6
        self.bb_gain = bb_gain = 20
        self.atten = atten = 60
        self.total_bw = total_bw = ch_bw*channels
        self.range_rf_gain = range_rf_gain = rf_gain
        self.range_ppm = range_ppm = ppm
        self.range_if_gain = range_if_gain = if_gain
        self.range_bb_gain = range_bb_gain = bb_gain
        self.pfb_taps = pfb_taps = firdes.low_pass_2(1, samp_rate, ch_bw, ch_tb, atten, firdes.WIN_HANN)
        self.bb_freq = bb_freq = 1897.344e6-(5*1.728e6)

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_1_1_0 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=3,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_1_1 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=3,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_1_0_1_0 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=3,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_1_0_1 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=3,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_1_0_0_1 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=3,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_1_0_0_0_0 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=3,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_1_0_0_0 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=3,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_1_0_0 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=3,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_1_0 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=3,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=3,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=594,
                decimation=625,
                taps=None,
                fractional_bw=None)
        self._range_rf_gain_range = Range(0, 100, 1, rf_gain, 200)
        self._range_rf_gain_win = RangeWidget(self._range_rf_gain_range, self.set_range_rf_gain, 'RF Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._range_rf_gain_win)
        self._range_ppm_range = Range(-70, 70, 1, ppm, 200)
        self._range_ppm_win = RangeWidget(self._range_ppm_range, self.set_range_ppm, 'PPM', "counter_slider", float)
        self.top_grid_layout.addWidget(self._range_ppm_win)
        self._range_if_gain_range = Range(0, 100, 1, if_gain, 200)
        self._range_if_gain_win = RangeWidget(self._range_if_gain_range, self.set_range_if_gain, 'IF Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._range_if_gain_win)
        self._range_bb_gain_range = Range(0, 100, 1, bb_gain, 200)
        self._range_bb_gain_win = RangeWidget(self._range_bb_gain_range, self.set_range_bb_gain, 'BB Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._range_bb_gain_win)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
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
        self.pfb_channelizer_ccf_0 = pfb.channelizer_ccf(
            11,
            pfb_taps,
            1.0,
            100)
        self.pfb_channelizer_ccf_0.set_channel_map([])
        self.pfb_channelizer_ccf_0.declare_sample_delay(0)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ''
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(bb_freq, 0)
        self.osmosdr_source_0.set_freq_corr(ppm, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(20e6, 0)
        self.digital_gmsk_demod_0_1_0 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0,
            verbose=False,log=False)
        self.digital_gmsk_demod_0_1 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0,
            verbose=False,log=False)
        self.digital_gmsk_demod_0_0_1_0 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0,
            verbose=False,log=False)
        self.digital_gmsk_demod_0_0_1 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0,
            verbose=False,log=False)
        self.digital_gmsk_demod_0_0_0_1 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0,
            verbose=False,log=False)
        self.digital_gmsk_demod_0_0_0_0_0 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0,
            verbose=False,log=False)
        self.digital_gmsk_demod_0_0_0_0 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0,
            verbose=False,log=False)
        self.digital_gmsk_demod_0_0_0 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0,
            verbose=False,log=False)
        self.digital_gmsk_demod_0_0 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0,
            verbose=False,log=False)
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0,
            verbose=False,log=False)
        self.blocks_udp_sink_0_1_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 2330, 1472, True)
        self.blocks_udp_sink_0_1 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 2326, 1472, True)
        self.blocks_udp_sink_0_0_1_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 2331, 1472, True)
        self.blocks_udp_sink_0_0_1 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 2327, 1472, True)
        self.blocks_udp_sink_0_0_0_1 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 2329, 1472, True)
        self.blocks_udp_sink_0_0_0_0_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 2332, 1472, True)
        self.blocks_udp_sink_0_0_0_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 2328, 1472, True)
        self.blocks_udp_sink_0_0_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 2325, 1472, True)
        self.blocks_udp_sink_0_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 2324, 1472, True)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 2323, 1472, True)
        self.blocks_pack_k_bits_bb_0_1_0 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0_1 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0_0_1_0 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0_0_1 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0_0_0_1 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0_0_0_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0_0_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0, 0), (self.blocks_udp_sink_0_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0_0, 0), (self.blocks_udp_sink_0_0_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0_0_0, 0), (self.blocks_udp_sink_0_0_0_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0_0_0_0, 0), (self.blocks_udp_sink_0_0_0_0_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0_0_1, 0), (self.blocks_udp_sink_0_0_0_1, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0_1, 0), (self.blocks_udp_sink_0_0_1, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0_1_0, 0), (self.blocks_udp_sink_0_0_1_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_1, 0), (self.blocks_udp_sink_0_1, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_1_0, 0), (self.blocks_udp_sink_0_1_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.digital_gmsk_demod_0_0, 0), (self.blocks_pack_k_bits_bb_0_0, 0))
        self.connect((self.digital_gmsk_demod_0_0_0, 0), (self.blocks_pack_k_bits_bb_0_0_0, 0))
        self.connect((self.digital_gmsk_demod_0_0_0_0, 0), (self.blocks_pack_k_bits_bb_0_0_0_0, 0))
        self.connect((self.digital_gmsk_demod_0_0_0_0_0, 0), (self.blocks_pack_k_bits_bb_0_0_0_0_0, 0))
        self.connect((self.digital_gmsk_demod_0_0_0_1, 0), (self.blocks_pack_k_bits_bb_0_0_0_1, 0))
        self.connect((self.digital_gmsk_demod_0_0_1, 0), (self.blocks_pack_k_bits_bb_0_0_1, 0))
        self.connect((self.digital_gmsk_demod_0_0_1_0, 0), (self.blocks_pack_k_bits_bb_0_0_1_0, 0))
        self.connect((self.digital_gmsk_demod_0_1, 0), (self.blocks_pack_k_bits_bb_0_1, 0))
        self.connect((self.digital_gmsk_demod_0_1_0, 0), (self.blocks_pack_k_bits_bb_0_1_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 1), (self.rational_resampler_xxx_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.rational_resampler_xxx_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.rational_resampler_xxx_1_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 6), (self.rational_resampler_xxx_1_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 10), (self.rational_resampler_xxx_1_0_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 7), (self.rational_resampler_xxx_1_0_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.rational_resampler_xxx_1_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 9), (self.rational_resampler_xxx_1_0_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.rational_resampler_xxx_1_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 8), (self.rational_resampler_xxx_1_1_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.pfb_channelizer_ccf_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.digital_gmsk_demod_0, 0))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.digital_gmsk_demod_0_0, 0))
        self.connect((self.rational_resampler_xxx_1_0_0, 0), (self.digital_gmsk_demod_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_1_0_0_0, 0), (self.digital_gmsk_demod_0_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_1_0_0_0_0, 0), (self.digital_gmsk_demod_0_0_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_1_0_0_1, 0), (self.digital_gmsk_demod_0_0_0_1, 0))
        self.connect((self.rational_resampler_xxx_1_0_1, 0), (self.digital_gmsk_demod_0_0_1, 0))
        self.connect((self.rational_resampler_xxx_1_0_1_0, 0), (self.digital_gmsk_demod_0_0_1_0, 0))
        self.connect((self.rational_resampler_xxx_1_1, 0), (self.digital_gmsk_demod_0_1, 0))
        self.connect((self.rational_resampler_xxx_1_1_0, 0), (self.digital_gmsk_demod_0_1_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "dect_multirx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_ch_tb(1.728e6-self.symbol_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_pfb_taps(firdes.low_pass_2(1, self.samp_rate, self.ch_bw, self.ch_tb, self.atten, firdes.WIN_HANN))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.set_range_rf_gain(self.rf_gain)
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

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

    def get_channels(self):
        return self.channels

    def set_channels(self, channels):
        self.channels = channels
        self.set_total_bw(self.ch_bw*self.channels)

    def get_ch_tb(self):
        return self.ch_tb

    def set_ch_tb(self, ch_tb):
        self.ch_tb = ch_tb
        self.set_pfb_taps(firdes.low_pass_2(1, self.samp_rate, self.ch_bw, self.ch_tb, self.atten, firdes.WIN_HANN))

    def get_ch_bw(self):
        return self.ch_bw

    def set_ch_bw(self, ch_bw):
        self.ch_bw = ch_bw
        self.set_pfb_taps(firdes.low_pass_2(1, self.samp_rate, self.ch_bw, self.ch_tb, self.atten, firdes.WIN_HANN))
        self.set_total_bw(self.ch_bw*self.channels)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.set_range_bb_gain(self.bb_gain)
        self.osmosdr_source_0.set_bb_gain(self.bb_gain, 0)

    def get_atten(self):
        return self.atten

    def set_atten(self, atten):
        self.atten = atten
        self.set_pfb_taps(firdes.low_pass_2(1, self.samp_rate, self.ch_bw, self.ch_tb, self.atten, firdes.WIN_HANN))

    def get_total_bw(self):
        return self.total_bw

    def set_total_bw(self, total_bw):
        self.total_bw = total_bw

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

    def get_pfb_taps(self):
        return self.pfb_taps

    def set_pfb_taps(self, pfb_taps):
        self.pfb_taps = pfb_taps
        self.pfb_channelizer_ccf_0.set_taps(self.pfb_taps)

    def get_bb_freq(self):
        return self.bb_freq

    def set_bb_freq(self, bb_freq):
        self.bb_freq = bb_freq
        self.osmosdr_source_0.set_center_freq(self.bb_freq, 0)



def main(top_block_cls=dect_multirx, options=None):

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
