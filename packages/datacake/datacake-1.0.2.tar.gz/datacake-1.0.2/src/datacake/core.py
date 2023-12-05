from typing import Iterable, NamedTuple, Any
from collections import defaultdict
from functools import partial
import random
import torch
import json

__all__ = [
  "shuffle", "randidxs", "stir",
  "estimate", "enum", "fill",
  "XYData", "TVTData", "multidict"
]

def shuffle(X: Iterable): random.shuffle(X); return X
def randidx(X: Iterable): return shuffle([i for i in range(len(X))])
def stir(X: Iterable, idxs: Iterable[int]): return [X[idx] for idx in idxs]
def estimate(X: Iterable[float], prc: int): return {k: round(v, prc) for k, v in X.items()} if type(X) is dict \
  else [round(x, prc) for x in X] if type(X) in (tuple, list) else round(X, prc)
def enum(X: Iterable, inv = False): return {x: i for i, x in enumerate(X)} \
  if inv else dict(enumerate(X))
def fill(F: Iterable[int | str], val): return {f: v for f, v in zip(F, val)} if type(val) in (tuple, list) \
  else {f: val[f] for f in F} if type(val) is dict else {f: val for f in F}

class XYData(NamedTuple):
  X: torch.Tensor
  Y: torch.Tensor
  size: int

class TVTData(NamedTuple):
  train: XYData
  valid: XYData
  test: XYData

class multidict:
  def __init__(self, depth: int = 1, default: type = None):
    multi = default
    for _ in range(depth):
      multi = partial(defaultdict, multi)
    self.multi = multi()
    self.default = default
    self.depth = depth
  def __getitem__(self, name: str):
    if type(name) is tuple:
      results = [self.multi]
      for i in enum(name, False):
        temps = []
        for result in results:
          if type(name[i]) is list:
            temp = []
            for n in name[i]:
              temp += [result[n]]
            temps += temp
          else: temps += [result[name[i]]]
        results = temps
      if len(results) == 1:
        result = results[0]
        if type(result) is defaultdict:
          result = dict(result)
        return result
      for i in enum(results):
        if type(results[i]) is defaultdict:
          results[i] = dict(results[i])
      return results
    elif type(name) is list:
      results = []
      for i in name:
        result = self.multi[i]
        if type(result) is defaultdict:
          result = dict(result)
        results += [result]
      return results
    result = self.multi[name]
    if type(result) is defaultdict:
      result = dict(result)
    return result
  def __setitem__(self, name: str, value: Any):
    if type(name) is tuple:
      results = [self.multi]
      for i in enum(name, False):
        if i + 1 == len(name):
          break
        temps = []
        for result in results:
          if type(name[i]) is list:
            temp = []
            for n in name[i]:
              temp += [result[n]]
            temps += temp
          else: temps += [result[name[i]]]
        results = temps
      for result in results:
        if type(name[-1]) is list:
          for n in name[-1]:
            result[n] = value
        else: result[name[-1]] = value
    elif type(name) is list:
      for n in name:
        self.multi[n] = value
    else: self.multi[name] = value
  def __delitem__(self, name: str):
    if type(name) is tuple:
      results = [self.multi]
      for i in enum(name, False):
        if i + 1 == len(name):
          break
        temps = []
        for result in results:
          if type(name[i]) is list:
            temp = []
            for n in name[i]:
              temp += [result[n]]
            temps += temp
          else: temps += [result[name[i]]]
        results = temps
      for result in results:
        if type(name[-1]) is list:
          for n in name[-1]:
            del results[n]
        else: del results[name[-1]]
      if len(results) == 1:
        return results[0]
      else: return results
    elif type(name) is list:
      for n in name:
        del self.multi[name[n]]
    else: del self.multi[name]
  def __getattr__(self, __name: str):
    attrs = ("multi", "default", "depth", "json", "dict")
    if __name in attrs: return super().__getattr__(__name)
    else: return getattr(self.multi, __name, None)
  def __setattr__(self, __name: str, __value: Any):
    attrs = ("multi", "default", "depth")
    if __name in attrs: super().__setattr__(__name, __value)
    else: setattr(self.multi, __name, __value)
  def __delattr__(self, __name: str):
    attrs = ("multi", "default", "depth")
    if __name in attrs: super().__delattr__(__name)
    else: delattr(self.multi, __name)
  def __repr__(self):
    dflt = self.default; dpth = self.depth; mdct = self.multi
    return f"multi({dflt}, {dpth}).multidict={repr(mdct)}"
  def __enter__(self): return self
  def __exit__(self, *args): del self
  def __del__(self):
    del self.multi
    del self.default
    del self.depth
    del self
  @property
  def json(self): return json.dumps(self.multi, indent = 2)
  @property
  def dict(self) -> dict: return json.loads(json.dumps(self.multi))
  def deepen(self, deep: int):
    multi = self.multi.copy()
    multi = multi.copy
    for _ in range(deep):
      multi = partial(defaultdict, multi)
    self.multi = multi()
    self.depth += deep
