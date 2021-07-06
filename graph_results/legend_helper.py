import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection

# define an object that will be used by the legend
class MulticolorPatch(object):
    def __init__(self, colors, obj):
        self.colors = colors
        self.object = obj
        
# define a handler for the MulticolorPatch object
class MulticolorPatchHandler(object):

    def legend_artist(self, legend, orig_handle, fontsize, handlebox):


        width, height = handlebox.width, handlebox.height
        patches = []
        up_to = len(orig_handle.colors)
        if up_to > 3:
            up_to = 3
        if orig_handle.object == 'circle':
            up_to = 5
        for i, c in enumerate(orig_handle.colors[:up_to]):
            if orig_handle.object == 'rect':
                patches.append(plt.Rectangle([0, (height/up_to)*i],
                               width,
                               height/up_to, 
                               facecolor=c, 
                               edgecolor='none'))
            elif orig_handle.object == 'circle':
                x_placement = (height/up_to + 3)*i
                cir = plt.Circle((x_placement, 2), 1, color=c)
                patches.append(cir)

        patch = PatchCollection(patches,match_original=True)

        handlebox.add_artist(patch)
        # import pdb
        # pdb.set_trace()
        # handlebox.set_height(200)
        return patch







# class LabelPatch(object):
#     def __init__(self, colors_before):
#         self.colors_before = colors_before

# class LabelPatchHandler(object):
#     def legend_artist(self, legend, orig_handle, fontsize, handlebox):
