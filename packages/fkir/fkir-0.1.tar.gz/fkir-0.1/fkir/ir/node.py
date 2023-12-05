from .base import FkBase
from .var import FkVar

class FkNode(FkBase):
  def __init__(self, unqn = None, isolation = False) -> None:
    if unqn is None:
      unqn = self.get_default_unqn('node')

    super().__init__(unqn=unqn)

    self._inputs = []
    self._outputs = []
    
    self._isolation = isolation
    
  @property
  def isolation(self):
    return self._isolation

  def add_input(self, v):
    if isinstance(v, str):
      v = FkVar(unqn = v)
    elif not isinstance(v, FkVar):
      raise RuntimeError
    self._inputs.append(v)
    if not self._isolation:
      v._add_dst(self)

  @property
  def inputs(self):
    return self._inputs[:]

  @inputs.setter
  def inputs(self, value):
    for i in self._inputs:
      self._remove_input(i)
    for v in value:
      self.add_input(v)
      
  def add_output(self, v):
    if isinstance(v, str):
      v = FkVar(unqn = v)
    elif not isinstance(v, FkVar):
      raise RuntimeError
    self._outputs.append(v)
    if not self._isolation:
      v._add_src(self)

  @property
  def outputs(self):
    return self._outputs[:]
  
  @outputs.setter
  def outputs(self, value):
    for i in self._outputs:
      self._remove_output(i)
    for v in value:
      self.add_output(v)
    
  @property
  def prev(self):
    ret = []
    for i in self.inputs:
      ret.extend(i.srcs)
    return ret

  @property
  def next(self):
    ret = []
    for i in self.outputs:
      ret.extend(i.dsts)
    return ret

  def _remove_input(self, var):
    self._inputs = [i for i in self._inputs if i != var]
    if not self._isolation:
      var._remove_dst(self)

  def _remove_output(self, var):
    self._outputs = [i for i in self._outputs if i != var]
    if not self._isolation:
      var._remove_src(self)
