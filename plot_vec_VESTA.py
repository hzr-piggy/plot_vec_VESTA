
def plot_vec(vesta_file, vec_file,
		cutoff = 0.1,
		radius=0.5, color=[255,0,0], penetrate = True, add_atom_radius = False,
		scale_factor = 1,
		delim = None, vec_type = "Cart", lat = None,
		output_suffix = "_vec"):
    
    # vesta_file:   A *.vesta file
    # vec_file:    A file containing vectors having dimensions of 3N*1 (or 1*3N) 
    # with delimiter=delim i.e.
    
    #                     x1
    #                     y1
    #                     z1
    #                     x2
    #                     y2
    #                     z2
    #                     .
    #                     .
    #                     .
    
    # cutoff (Double):       Angstrom below which vector will not show
    # radius (Double):       Set radius of vector
    # color (Double 0-255):  Set color of vector
    # penetrate (Bool):      Set whether vector penetrate atom
    # add_atom_radius (Bool):Set whether to add atom radius to vector modulus
    # scale_factor (Double): Scale vector in the figure
    
    # delim:                 Delimiter in the vec_file
    # vec_type:              Type of vectors, can be "Cart" (Cartesian), "Lat" (Lattice vector notation [u v w], in reduced coord)
    #                        or "Modulus" (Modulus along crystallographic axis). Default is 'Cart'
    # lat:                   3-by-3 lattice parameter in Angstrom required if vec_type == 'Cart'
    
	import numpy as np
	import re
	import os
	
	# Read input files
	vesta_data = open(vesta_file,'r').read()
	temp = np.loadtxt(vec_file,delimiter=delim)
	N_dim = temp.shape[0]
	temp = temp.reshape((N_dim//3,3))
	
	# Convert to Modulus along crystallographic axis
	if vec_type == 'Lat':
		struct_match=re.findall(r'CELLP\n\s+(\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+)',vesta_data)[0]
		cell = np.array([float(x) for x in struct_match.split()]) # cell lengths in angstrong
		temp *= cell
	elif vec_type == 'Cart':
		assert lat is not None, '3-by-3 lattice parameter in Angstrom required if vec_type == Cart'
		temp = temp@np.linalg.inv(lat)*np.linalg.norm(lat,axis=1)
		
	vectors = np.around(temp*scale_factor,decimals=3) # Round the disp to 3 decimals
	
	# Find unique vectors
	vectors_unique = np.unique(vectors,axis=0)
	
	# Vector penetrate atom or add atomic radius?
	flag = int(penetrate)+int(add_atom_radius)*2
	
	VECTR_str=r"\1"
	VECTT_str=r"\1"
	i = 1
	for v in vectors_unique:
		if np.linalg.norm(v) > cutoff: # only create vector with modules > cutoff

			VECTR_str += "   {0}  {1}  {2}  {3}  0\n".format(i,v[0],v[1],v[2]) # create vectors

			atom_list = np.where((vectors == v).all(axis=1))[0]
			for atom in atom_list:
				VECTR_str += "    {0}  0  0  0  0\n".format(atom+1) # create atom labels start from 1

			VECTR_str += "0 0 0 0 0\n"

			VECTT_str += "   {0}  {1}  {2}  {3}  {4}  {5}\n".format(i,radius, color[0], color[1], color[2], flag)

			i += 1

	output_data = re.sub(r"(VECTR\n)",VECTR_str,vesta_data)
	output_data = re.sub(r"(VECTT\n)",VECTT_str,output_data)
	
	name, ext = os.path.splitext(vesta_file)
	file_out = open(name+output_suffix+ext,'w+')
	file_out.write(output_data)
	file_out.close()
