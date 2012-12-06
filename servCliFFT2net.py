#!/usr/bin/env python

"""a quick hack to demonstrate getting data between python and
   marsyas. """

import sys
import numpy
import pylab

import marsyas
import marsyas_util

#PLOT = True
PLOT = False

def make_input(filename_input):
    series = ["Series/input", ["SoundFileSource/src", 
        "Spectrum/spec"]]
    this_net = marsyas_util.create(series)
    this_net.updControl(
        "SoundFileSource/src/mrs_string/filename",
        filename_input)
    return this_net

def make_output(filename_output):
    series = ["Series/output", ["RealvecSource/real_src",
        "InvSpectrum/ispec",
        "SoundFileSink/dest"]]
    this_net = marsyas_util.create(series)
    this_net.updControl("mrs_natural/inSamples", 1)
    this_net.updControl("mrs_natural/inObservation", 512)
#    this_net.updControl("mrs_real/israte", 44100.0)
    this_net.updControl(
        "SoundFileSink/dest/mrs_string/filename",
        filename_output)
    return this_net



def main():
    try:    
        filename_input = sys.argv[1]
        filename_output = sys.argv[2]
    except:
        print "USAGE: ./in_out.py input_filename.wav output_filename.wav"
        exit(1)
    
    input_net = make_input(filename_input)
    output_net = make_output(filename_output)

    notempty = input_net.getControl("SoundFileSource/src/mrs_bool/hasData")
    #net1outCtrl = input_net.getControl("Spectrum/spec/mrs_realvec/processedData")
    net1outCtrl = input_net.getControl("mrs_realvec/processedData")
    net2inCtrl = output_net.getControl(
        "RealvecSource/real_src/mrs_realvec/data")
    #second = output_net.getControl(
    #    "RealvecSource/real_src/mrs_realvec/processedData")
    #new_vec = marsyas.realvec( 512, 1)
    while notempty.to_bool():
        ### get input data
        input_net.tick()
        net1_out = net1outCtrl.to_realvec()
        #print net1_out.getRows(), net1_out.getCols()

        ### do something with it
        #for i in range(net1_out.getSize()):
        #    new_vec[i] = net1_out[i]
        #print new_vec
        net2inCtrl.setValue_realvec(net1_out)
        #net2inCtrl.setValue_realvec(new_vec)
        #print net1_out
        if PLOT:
            pylab.plot(net1_out, label="input")
#            pylab.plot(output_net_begi, label="output")
            pylab.legend()
            pylab.show()

        ### set output data
        output_net.tick()

        #foo = second.to_realvec()
        #print foo


main()

