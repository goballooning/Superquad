"""
Superquadrics in Python
=======================
Script to create an Interactive Superquadric drawing
tool.

Author: Pratik Mallya (December 2011)
"""
import numpy as np

def fexp(x,p):
    """a different kind of exponentiation"""
    return (np.sign(x)*(np.abs(x)**p))

def tens_fld(A,B,C,P,Q):
    """this module plots superquadratic surfaces with the given parameters"""
    phi, theta = np.mgrid[0:np.pi:80j, 0:2*np.pi:80j]
    x       =A*(fexp(np.sin(phi),P)) *(fexp(np.cos(theta),Q))
    y       =B*(fexp(np.sin(phi),P)) *(fexp(np.sin(theta),Q))
    z       =C*(fexp(np.cos(phi),P))
    return x , y , z 


from traits.api import HasTraits, Range, Instance, \
                    on_trait_change
from traitsui.api import View, Item, HGroup
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import \
                    MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene


class Visualization(HasTraits):
    alpha = Range(0.0, 4.0,  1.0/4)
    beta  = Range(0.0, 4.0,  1.0/4)
    scene      = Instance(MlabSceneModel, ())

    def __init__(self):
        # Do not forget to call the parent's __init__
        HasTraits.__init__(self)
        x, y, z, = tens_fld(1,1,1,self.beta, self.alpha)
        self.plot = self.scene.mlab.mesh(x, y, z, colormap='copper', representation='surface')

    @on_trait_change('beta,alpha')
    def update_plot(self):
        x, y, z, = tens_fld(1,1,1,self.beta, self.alpha)
        self.plot.mlab_source.set(x=x, y=y, z=z)


    # the layout of the dialog created
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                    height=550, width=550, show_label=False),
                HGroup(
                        '_', 'beta', 'alpha',
                    ),
                )

visualization = Visualization()
visualization.configure_traits()


