#!/usr/bin/env python

import os

def print_env(env):
	keys=env.m_table.keys()
	keys.sort()
	for k in keys:
		print k,env[k]

def append_up_dirs(dirs,num):
	return [('..'+os.sep)*num+dir for dir in dirs];

def create_obj_common(bld,source,target,depth):
	env=bld.env_of_name('default')
	obj=bld.create_obj('cpp','staticlib')
	obj.source=source
	obj.target=target
	obj.uselib=env['uselib_common']
	obj.includes=append_up_dirs(env['includes_common'],depth)
	obj.obj_ext='.o'
	obj.inst_var=0
	obj.inst_dir=0
	return obj

def create_shlib_common(bld,source,target,local,inst_dir,depth):
	env=bld.env_of_name('default')
	shlib=bld.create_obj('cpp','shlib')
	shlib.source=source
	shlib.target=target
	shlib.uselib_local=local
	shlib.uselib=env['uselib_common']
#	shlib.includes=append_up_dirs(env['includes_common'],depth)
	shlib.env['shlib_PATTERN']='_%s.so'
	shlib.obj_ext='.o'
	shlib.inst_var='PREFIX'
	shlib.inst_dir=inst_dir
	return shlib
