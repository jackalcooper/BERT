from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import copy
import json
import math
import re
import six
import tensorflow as tf
from model_io import model_io_utils

class ModelIO(object):
	def __init__(self, config, **kargs):
		print(" initializing ModelIO ")
		self.config = config
		
	def set_saver(self, max_keep=10, **kargs):
		if len(kargs.get("var_lst", [])) >= 1:
			self.saver = tf.train.Saver(var_list=kargs.get("var_lst", []),
			max_to_keep=self.config.get("max_to_keep", 100))
		else:
			self.saver = tf.train.Saver(
			max_to_keep=self.config.get("max_to_keep", 100))

	def init_model(self, sess, **kargs):
		sess.run(tf.global_variables_initializer())

	def save_model(self, sess, checkpoint, **kargs):
		self.saver.save(sess, checkpoint)

	def load_model(self, sess, checkpoint, **kargs):
		self.saver.restore(sess, checkpoint)

	def apply_ema(self, sess, tvars, loss, **kargs):
		decay = self.config.get("ema_decay", 0.999)
		assign_vars = model_io_utils.apply_ema(tvars, loss, 
											decay=decay, **kargs)
		
	def get_params(self, scope, **kargs):
		tvars = model_io_utils.get_params(scope, **kargs)
		return tvars

	def print_params(self, tvars, string):
		model_io_utils.print_params(tvars, string)

	def load_pretrained(self, tvars, init_checkpoint, **kargs):
		print(kargs.get("exclude_scope", ""), "===============")
		[assignment_map, 
		initialized_variable_names] = model_io_utils.get_assigment_map_from_checkpoint(
															tvars, 
															init_checkpoint, 
															**kargs)

		model_io_utils.init_pretrained(assignment_map, 
										initialized_variable_names,
										tvars, init_checkpoint, **kargs)
