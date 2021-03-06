import tensorflow as tf
import numpy as np


def get_bbox_from_segmentation_mask(mask):
  object_locations = tf.cast(tf.where(tf.equal(mask, 1))[:, :2], tf.int32)
  y0 = tf.reduce_min(object_locations[:, 0])
  x0 = tf.reduce_min(object_locations[:, 1])
  y1 = tf.reduce_max(object_locations[:, 0]) + 1
  x1 = tf.reduce_max(object_locations[:, 1]) + 1
  bbox = tf.stack([y0, x0, y1, x1])
  return bbox


def encode_bbox_as_mask_np(bbox, shape):
  encoded = np.zeros(tuple(shape[:2]) + (1,), np.uint8)
  y0, x0, y1, x1 = np.round(bbox).astype(np.int)
  encoded[y0:y1, x0:x1] = 1
  return encoded


def encode_bbox_as_mask(bbox, shape):
  encoded = tf.py_func(encode_bbox_as_mask_np, [bbox, shape], tf.uint8, name="encode_bbox_as_mask")
  encoded.set_shape((None, None, 1))
  return encoded
