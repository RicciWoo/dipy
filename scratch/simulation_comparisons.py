import os
import numpy as np
import dipy as dp
import dipy.io.pickles as pkl
import scipy as sp
from matplotlib.mlab import find
import dipy.core.sphere_plots as splots
import dipy.core.sphere_stats as sphats
import dipy.core.geometry as geometry
import get_vertices as gv

'''
results_SNR030_1fibre
results_SNR030_1fibre+iso
results_SNR030_2fibres_15deg
results_SNR030_2fibres_30deg
results_SNR030_2fibres_60deg
results_SNR030_2fibres_90deg
results_SNR030_2fibres+iso_15deg
results_SNR030_2fibres+iso_30deg
results_SNR030_2fibres+iso_60deg
results_SNR030_2fibres+iso_90deg
results_SNR030_isotropic
'''

fname='/home/ian/Data/SimData/results_SNR030_1fibre'
#fname='/home/eg01/Data_Backup/Data/Marta/DSI/SimData/results_SNR030_isotropic'

sim_data=np.loadtxt(fname)

''' file  has one row for every voxel, every voxel is repeating 1000
times with the same noise level , then we have 100 different
directions. 1000 * 100 is the number of all rows.

The 100 conditions are given by 10 polar angles (in degrees) 0, 20, 40, 60, 80,
80, 60, 40, 20 and 0, and each of these with longitude angle 0, 40, 80,
120, 160, 200, 240, 280, 320, 360. 

'''

marta_table_fname='/home/ian/Data/SimData/Dir_and_bvals_DSI_marta.txt'
#bvalsf='/home/eg01/Data_Backup/Data/Marta/DSI/SimData/bvals101D_float.txt'

b_vals_dirs=np.loadtxt(marta_table_fname)

bvals=b_vals_dirs[:,0]*1000
gradients=b_vals_dirs[:,1:]

#splots.plot_sphere(gradients, 'Marta DSI gradients')

#v = gv.get_vertex_set('dsi102')
#splots.plot_sphere(v, 'dsi102 axes')

gqfile = '/home/ian/Data/SimData/gq_SNR030_1fibre.pkl'
gq = pkl.load_pickle(gqfile)

'''
gq.IN               gq.__doc__          gq.glob_norm_param
gq.QA               gq.__init__         gq.odf              
gq.__class__        gq.__module__       gq.q2odf_params
'''

tnfile = '/home/ian/Data/SimData/tn_SNR030_1fibre.pkl'
tn = pkl.load_pickle(tnfile)

'''
tn.ADC               tn.__init__          tn._getevals
tn.B                 tn.__module__        tn._getevecs
tn.D                 tn.__new__           tn._getndim
tn.FA                tn.__reduce__        tn._getshape
tn.IN                tn.__reduce_ex__     tn._setevals
tn.MD                tn.__repr__          tn._setevecs
tn.__class__         tn.__setattr__       tn.adc
tn.__delattr__       tn.__sizeof__        tn.evals
tn.__dict__          tn.__str__           tn.evecs
tn.__doc__           tn.__subclasshook__  tn.fa
tn.__format__        tn.__weakref__       tn.md
tn.__getattribute__  tn._evals            tn.ndim
tn.__getitem__       tn._evecs            tn.shape
tn.__hash__          tn._getD             
'''

''' file  has one row for every voxel, every voxel is repeating 1000
times with the same noise level , then we have 100 different
directions. 100 * 1000 is the number of all rows.

At the moment this module is hardwired to the use of the EDS362
spherical mesh. I am assumung (needs testing) that directions 181 to 361
are the antipodal partners of directions 0 to 180. So when counting the
number of different vertices that occur as maximal directions we wll map
the indices modulo 181.
'''

def analyze_maxima(indices, max_dirs,subsets):
    '''This calculates the eigenstats for each of the replicated batches
    of the simulation data
    '''

    results = []


    for direction in subsets:

        batch = max_dirs[direction,:,:]

        index_variety = np.array([len(set(np.remainder(indices[direction,:],181)))])

        c,b = sphats.eigenstats(batch)

        results.append(np.concatenate((c,b, index_variety)))

    return results

#dt_first_directions = tn.evecs[:,:,0].reshape((100,1000,3))
# these are the principal directions for the full set of simulations


eds=np.load(os.path.join(os.path.dirname(dp.__file__),'core','matrices','evenly_distributed_sphere_362.npz'))

odf_vertices=eds['vertices']

dt_first_directions_in=odf_vertices[tn.IN]

dt_indices = tn.IN.reshape((100,1000))

dt_results = analyze_maxima(dt_indices, dt_first_directions_in.reshape((100,1000,3)),range(100))

gq_indices = np.array(gq.IN[:,0],dtype='int').reshape((100,1000))

gq_first_directions_in=odf_vertices[np.array(gq.IN[:,0],dtype='int')]

print gq_first_directions_in.shape

gq_results = analyze_maxima(gq_indices, gq_first_directions_in.reshape((100,1000,3)),range(100))

#for gqi see example dicoms_2_tracks gq.IN[:,0]

np.set_printoptions(precision=6, suppress=True, linewidth=200)

out = open('dt_and_gq.txt','w')

results = np.hstack((np.vstack(dt_results), np.vstack(gq_results)))

print >> out, results[[0,1,5,6,4,9,2,3,7,8],:]

out.close()


    #up = dt_batch[:,2]>= 0

    #splots.plot_sphere(dt_batch[up], 'batch '+str(direction))

    #splots.plot_lambert(dt_batch[up],'batch '+str(direction), centre)
    
    #spread = gq.q2odf_params e,v = np.linalg.eigh(np.dot(spread,spread.transpose())) effective_dimension = len(find(np.cumsum(e) > 0.05*np.sum(e))) #95%

    #rotated = np.dot(dt_batch,evecs)

    #rot_evals, rot_evecs =  np.linalg.eig(np.dot(rotated.T,rotated)/rotated.shape[0])

    #eval_order = np.argsort(rot_evals)

    #rotated = rotated[:,eval_order]

    #up = rotated[:,2]>= 0

    #splot.plot_sphere(rotated[up],'first1000')

    #splot.plot_lambert(rotated[up],'batch '+str(direction))

