#!/usr/bin/env python

import os

srcdir='.'
blddir='obj'

def set_options(opt):
	opt.tool_options('gcc')
	opt.tool_options('g++')

	opt.sub_options('src')

def configure(conf):
	conf.check_tool('gcc')
	conf.check_tool('g++')

	conf.sub_config('src')

def build(bld):
	bld.add_subdirs('src')
